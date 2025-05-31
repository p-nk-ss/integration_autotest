import time



class CBPWorkTypes:

    work_types = ['1.1 - Work regular', '1.2 - Work overtime', '1.3 - Work on holidays', '1.4 - Work for day-off',
                  '1.5 - Work night overtime', '1.6 - OCD Weekday', '1.7 - OCD Weekend', '2.3 - Illness',
                  '2.4 - Day-off worked off', '2.5 – Day-off internally compensated', '2.6 - Absence',
                  '3.1 - Work on site', '3.2 - Travel', '3.3 - Travel on holiday', '3.4 – Holiday on site',
                  '3.5 – Work on site on holiday', '3.6 - Standard overtime on site', '3.7 - Night overtime on site',
                  '3.81 - OCD Weekday on site', '3.82 - OCD Weekend on site', '4.1 - Direct order']

    def __init__(self, page):
        self.page = page

    def checkbox_locator(self, work_type_name, compackage_name):
        return self.page.locator(".mat-row").filter(has_text=f"{work_type_name}").locator(
            f".mat-column-UA-{compackage_name} .mat-icon")

    def turn_on_work_type(self, work_type_name, compackage_name):
        while self.checkbox_locator(work_type_name, compackage_name).inner_text() != "check_box":
            self.checkbox_locator(work_type_name, compackage_name).click()
        time.sleep(10)

    def turn_off_work_type(self, work_type_name, compackage_name):
        while self.checkbox_locator(work_type_name, compackage_name).inner_text() != "check_box_outline_blank":
            self.checkbox_locator(work_type_name, compackage_name).click()
        time.sleep(10)

    def turn_on_all_work_types(self, compackage_name):
        for item in CBPWorkTypes.work_types:
            while self.checkbox_locator(item, compackage_name).inner_text() != "check_box":
                self.checkbox_locator(item, compackage_name).click()
        time.sleep(10)

    def turn_off_all_work_types(self, compackage_name):
        for item in CBPWorkTypes.work_types:
            while self.checkbox_locator(item, compackage_name).inner_text() != "check_box_outline_blank":
                self.checkbox_locator(item, compackage_name).click()
        time.sleep(10)
