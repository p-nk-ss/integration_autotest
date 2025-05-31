class Waitings:

    def __init__(self, page):
        self.page = page

    def progressbar_waiting(self):
        progressbar = self.page.locator(".p-progressbar.p-component.p-progressbar-indeterminate")
        [alert.wait_for(state="hidden") for alert in progressbar.all()]

    def skeleton_waiting(self):
        [alert.wait_for(state="hidden") for alert in self.page.locator(".p-skeleton").all()]

    def load_state_waiting(self):
        self.page.wait_for_load_state(state="networkidle", timeout=50000)
