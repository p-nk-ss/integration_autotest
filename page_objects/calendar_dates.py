
class CalendarDates:

    def __init__(self, page):
        self.page = page

    def set_date(self, date: list):
        match date:
            case [day]:
                self.page.locator(".p-datepicker-calendar td"). \
                    filter(has_not=self.page.locator(".p-disabled")).get_by_text(str(day), exact=True).click()
            case [day, month]:
                self.page.locator(".p-datepicker-month").click()
                self.page.get_by_text(str(month), exact=True).click()
                self.page.locator(".p-datepicker-calendar td"). \
                    filter(has_not=self.page.locator(".p-disabled")).get_by_text(str(day), exact=True).click()
            case [day, month, year]:
                self.page.locator(".p-datepicker-year").click()
                while self.page.get_by_text(str(year), exact=True).is_hidden():
                    self.page.locator(".p-datepicker-next-icon").click()
                self.page.get_by_text(str(year), exact=True).click()
                self.page.get_by_text(str(month), exact=True).click()
                self.page.locator(".p-datepicker-calendar td"). \
                    filter(has_not=self.page.locator(".p-disabled")).get_by_text(str(day), exact=True).click()

