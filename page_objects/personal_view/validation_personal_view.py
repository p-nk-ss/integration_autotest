import re
from datetime import datetime, timedelta

from page_objects.waitings import Waitings


class ValidationPersonalView:

    def __init__(self, page):
        self.page = page
        self.wait = Waitings(page)

    def get_day_date(self, day_number):
        week_days = self.page.locator("button[icon='pi pi-calendar'] .p-button-label").inner_text()
        pattern = r'(\d+) - \d+ (\w+ \d{4})'
        match = re.search(pattern, week_days)
        value1 = match.group(1)
        value2 = match.group(2)
        month, year = value2.split()
        new_date_str = f"{value1} {month[:3]} {year}"
        date_obj = datetime.strptime(new_date_str, "%d %b %Y")
        return (date_obj + timedelta(days=day_number - 1)).strftime("%d/%m/%Y")

    def is_conflict_hours_displaying(self, project_name, worktype_name, day_number) -> bool:
        self.wait.progressbar_waiting()
        week_days = self.page.locator(f"[app-item-row]:below(:text(\"{project_name}\"))").filter(
            has_text=f"{worktype_name}").first.locator('td[app-log-cell-resolver] div').all()
        return "conflict" in week_days[day_number - 1].get_attribute("class")

    def get_day_off_input_value(self, piwt_name, day_number: int) -> str:
        locator = self.page.locator(f"[app-item-row]").filter(has_text=f"{piwt_name}")
        days_of_week = locator.first.locator("input").all()
        return days_of_week[day_number - 1].input_value()

    def is_warning_time_tracking_should_not_filled_displaying(self) -> bool:
        self.wait.skeleton_waiting()
        self.wait.progressbar_waiting()
        return self.page.get_by_text("In accordance with your terms of cooperation with the company, "
                                     "Corporate Time Tracking should not be filled in.").is_visible()

