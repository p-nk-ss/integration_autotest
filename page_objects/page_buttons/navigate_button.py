class NavigateButton:

    def __init__(self, page):
        self.page = page

    def open_personal_view(self):
        self.page.locator(".week-period-loader").wait_for(state="hidden")
        self.page.get_by_role("link", name="Personal View").click()
        self.page.locator(".week-period-loader").wait_for(state="hidden")

    def open_management_view(self):
        self.page.locator(".week-period-loader").wait_for(state="hidden")
        self.page.get_by_role("link", name="Management View").click()
        self.page.locator(".week-name").filter(has_text="Loading..").wait_for(state="detached")
        self.page.locator(".week-period-loader").wait_for(state="hidden")

    def open_work_description_view(self):
        self.page.get_by_role("link", name="Work Description").click()
        self.page.locator(".week-period-loader").wait_for(state="hidden")

    def open_company_view(self):
        self.page.get_by_role("link", name="Company View").click()
        self.page.locator(".week-name").filter(has_text="Loading..").wait_for(state="detached")
        self.page.locator(".week-period-loader").wait_for(state="hidden")

    def open_export_to_excel_view(self):
        self.page.get_by_role("link", name="Export to Excel").click()
        self.page.locator(".week-period-loader").wait_for(state="hidden")

    def goto_next_week(self):
        self.page.locator(".period-next").click()
        self.page.locator(".week-period-loader").wait_for(state="hidden")

    def goto_previous_week(self):
        self.page.locator(".period-previous").click()
        self.page.locator(".week-period-loader").wait_for(state="hidden")
