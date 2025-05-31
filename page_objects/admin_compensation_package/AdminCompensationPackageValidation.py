class AdminCompensationPackageValidation:

    def __init__(self, page):
        self.page = page

    def get_list_displaying_counters(self) -> list[str]:
        counters = self.page.locator("app-compensation-package-mark-values[name='Hours off'] .p-listbox-item div").all()
        return [counter.inner_text() for counter in counters]

    def get_list_displaying_work_types(self) -> list[str]:
        counters = self.page.locator("app-compensation-package-mark-values[name='Work Types'] .p-listbox-item div").all()
        return [counter.inner_text() for counter in counters]
