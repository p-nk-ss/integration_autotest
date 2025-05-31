class AdminCompensationPackage:

    def __init__(self, page):
        self.page = page

    def select_compensation_package(self, package_name):
        self.page.get_by_role("cell", name=f"{package_name}").click()
