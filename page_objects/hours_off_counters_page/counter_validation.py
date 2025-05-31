import datetime

from page_objects.calendar_dates import CalendarDates


class CounterValidation:

    def __init__(self, page):
        self.page = page
        self.calendar = CalendarDates(page)

    def get_list_of_dates_used_hours(self, counter, hours) -> list[str]:
        self.page.get_by_role("row", name=f"{counter} {hours}").locator(".w-8.h-8").click()
        self.page.get_by_role("menuitem", name="View").click()
        table = self.page.locator(".p-dialog-content .p-element.p-datatable-tbody").all()
        for date in table:
            return [s.inner_text() for s in date.locator("td").all() if len(s.inner_text()) > 2]

    def get_person_available_counters(self) -> list[str]:
        day = datetime.datetime.now().day
        self.page.locator("app-blockable-target").get_by_role("button", name="Add").click()
        self.page.get_by_label("Date Add").click()
        self.page.locator(".p-datepicker-calendar td"). \
            filter(has_not=self.page.locator(".p-disabled")).get_by_text(f"{day}", exact=True).click()
        self.page.locator("p-dropdown").filter(has_text="Choose Hours-Off type") \
            .get_by_role("button", name="dropdown trigger").click()
        counters = [s.inner_text() for s in self.page.locator(".p-dropdown-items li span").all()]
        self.page.locator("p-dropdown").filter(has_text="Choose Hours-Off type") \
            .get_by_role("button", name="dropdown trigger").click()
        self.page.get_by_role("button", name="Cancel").click()
        return counters
