import time
from page_objects.calendar_dates import CalendarDates


class PersonCounters:

    def __init__(self, page):
        self.page = page
        self.calendar = CalendarDates(page)

    def add_hours_off(self, day, counter_name):
        self.page.locator("app-blockable-target").get_by_role("button", name="Add").click()
        self.page.get_by_label("Date Add").click()
        self.page.locator(".p-datepicker-group").wait_for(state="visible")

        self.page.locator(".p-datepicker-calendar td"). \
            filter(has_not=self.page.locator(".p-disabled")).get_by_text(day, exact=True).click()
        self.page.locator("p-dropdown").filter(has_text="Choose Hours-Off type")\
            .get_by_role("button", name="dropdown trigger").click()
        self.page.get_by_role("option", name=f"{counter_name}").click()
        time.sleep(2)
