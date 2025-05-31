from page_objects.waitings import Waitings


class AddTime:
    def __init__(self, page):
        self.page = page
        self.wait = Waitings(page)

    def add_work_time(self, project_name, work_type_name, hours, day_number: int):
        self.wait.progressbar_waiting()
        item_row = (self.page.locator(f"[app-item-row]:below(:text(\"{project_name}\"))")
                    .filter(has_text=f"{work_type_name}").first)
        item_row.wait_for(state="visible")
        days_of_week = item_row.locator('div[app-log-cell-personal], '
                                        'div[app-log-cell-manager], '
                                        'div[app-log-cell-company]').all()
        days_of_week[day_number - 1].click()
        days_of_week[day_number - 1].locator("input").fill(str(hours))
        days_of_week[day_number - 1].press("Enter", timeout=30000)
        self.wait.progressbar_waiting()

    def add_dayoff_time(self, piwt_name, hours: str, day_number: int):
        self.wait.progressbar_waiting()
        days_of_week = (self.page.locator("[app-item-row]").filter(has_text=f"{piwt_name}")
                        .first.locator("input").all())
        days_of_week[day_number - 1].click()
        days_of_week[day_number - 1].fill(str(hours))
        days_of_week[day_number - 1].press("Enter", timeout=30000)
        self.wait.progressbar_waiting()
