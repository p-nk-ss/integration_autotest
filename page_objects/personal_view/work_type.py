class WorkType:

    def __init__(self, page):
        self.page = page

    def add_work_type(self, project_name, worktype_name):
        row_content = self.page.locator(".content-projects")
        row_content.locator(":scope", has_text=f"{project_name}") \
            .locator("i.mdi.mdi-playlist-plus").first.click()
        self.page.locator(".project-name").filter(has_text=f"{project_name}") \
            .locator(".select-list").get_by_role("link", name=f"{worktype_name}").click()

    def add_hierarchy(self, project_name, worktype_name, hierarchy_name):
        self.page.locator(".content-projects").filter(has_text=f"{project_name}"). \
            get_by_role("cell", name=f"{worktype_name}") \
            .locator("i.mdi.mdi-playlist-plus").click()
        self.page.get_by_role("link", name=f"{hierarchy_name}").click()
