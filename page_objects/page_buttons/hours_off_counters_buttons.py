class CountersButtons:

    def __init__(self, page):
        self.page = page

    def press_add_counter(self):
        self.page.get_by_role("button", name="Add").click()

    def press_popup_add_item(self):
        self.page.get_by_role("button", name="Add Item").click()
        waits = self.page.locator(".p-progress-spinner-circle").all()
        for wait in waits:
            wait.wait_for(state="hidden")

    def press_popup_save(self):
        self.page.get_by_role("button", name="Save").click()
        waits = self.page.locator(".p-progress-spinner-circle").all()
        for wait in waits:
            wait.wait_for(state="hidden")
