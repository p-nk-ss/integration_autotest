import time


class AbsenceType:

    counters = ['Military services AFU (Armeded Forces of Ukraine)', 'Donation', 'Military check-up',
                'Hours By Experience', 'Hours Off Worked Off', 'Travel On Holiday', 'Illness', 'Training',
                'Day off by law (first line)', 'Day off by law (second line)', 'Paternity', 'Childcare leave',
                'Military services TD (territorial defense)', 'Maternity leave', 'Pregnancy Illness', 'Regional Holiday',
                'Illness (without certificate)', 'Marriage/Childbirth']

    def __init__(self, page):
        self.page = page

    def checkbox_locator(self, counter_name, compackage_name):
        return self.page.locator(".mat-row").filter(has=self.page.get_by_text(f"{counter_name}", exact=True)).locator(
            f".mat-column-UA-{compackage_name} .mat-icon")

    def turn_on_counter(self, counter_name, compackage_name):
        while self.checkbox_locator(counter_name, compackage_name).inner_text() != "check_box":
            self.checkbox_locator(counter_name, compackage_name).click()
        time.sleep(10)

    def turn_off_counter(self, counter_name, compackage_name):
        while self.checkbox_locator(counter_name, compackage_name).inner_text() != "check_box_outline_blank":
            self.checkbox_locator(counter_name, compackage_name).click()
        time.sleep(10)

    def turn_on_all_counters(self, compackage_name):
        for item in AbsenceType.counters:
            while self.checkbox_locator(item, compackage_name).inner_text() != "check_box":
                self.checkbox_locator(item, compackage_name).click()
        time.sleep(10)

    def turn_off_all_counters(self, compackage_name):
        for item in AbsenceType.counters:
            while self.checkbox_locator(item, compackage_name).inner_text() != "check_box_outline_blank":
                self.checkbox_locator(item, compackage_name).click()
        time.sleep(10)
