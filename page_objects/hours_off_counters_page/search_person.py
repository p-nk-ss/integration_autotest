import time


class SearchPerson:

    def __init__(self, page):
        self.page = page

    def search_person(self, person_name):
        self.page.get_by_placeholder("Search").fill(person_name)
        self.page.locator("div[role='progressbar']").wait_for(state="hidden")
        time.sleep(1)

    def select_person(self, person_name):
        self.search_person(person_name)
        self.page.get_by_role("option", name=f"{person_name}").click()
        self.page.locator(".p-skeleton.p-component").wait_for(state="hidden")

    def get_list_of_persons(self):
        list_of_persons = [name.inner_text() for name in self.page.locator(".p-ripple.p-element.p-listbox-item").all()]
        return list_of_persons



