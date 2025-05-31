import time


class CBPCompackages:

    def __init__(self, page):
        self.page = page

    def add_compackage(self, package_name):
        self.page.get_by_role("columnheader").filter(has_text="add").click()
        self.page.get_by_role("combobox", name="Country").click()
        self.page.get_by_role("option", name="UA").click()
        self.page.get_by_role("combobox", name="Package group").click()
        self.page.get_by_role("option", name="AI").click()
        self.page.get_by_label("Name").fill(package_name)
        self.page.get_by_role("button", name="Create").click()
        time.sleep(3)

    def change_package_state(self, package_name, state):
        self.page.get_by_role("row", name=f"UA-AI-{package_name}").get_by_role("button").click()
        self.page.get_by_role("combobox", name="State").click()
        self.page.get_by_role("option", name=f"{state}").click()
        self.page.get_by_role("button", name="Edit").click()
        time.sleep(2)