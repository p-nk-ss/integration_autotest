import datetime
import re
import time

import numpy as np
from dateutil.relativedelta import relativedelta, MO
from datetime import date,  datetime, timedelta

from page_objects.calendar_dates import CalendarDates
from page_objects.waitings import Waitings


class DaysOfWeek:

    def __init__(self, page):
        self.page = page
        self.calendar = CalendarDates(page)
        self.wait = Waitings(page)

    @staticmethod
    def get_first_sunday_of_next_month():
        """Date of the first Sunday of the following month"""
        year_month = (datetime.today() + datetime.timedelta(days=30)).date().strftime('%Y-%m')
        first_sunday = np.busday_offset(year_month, 0, roll='forward', weekmask='Sun')
        return first_sunday.astype(object).day

    @staticmethod
    def get_first_monday_of_month():
        """Date of the first Monday of the current month"""
        year_month = datetime.today().strftime('%Y-%m')
        first_monday = np.busday_offset(year_month, 0, roll='forward', weekmask='Mon')
        return first_monday.astype(date)

    @staticmethod
    def get_last_monday_of_month():
        """Date of the last Monday of the current month"""
        today = date.today()
        last_monday = today + relativedelta(day=31, weekday=MO(-1))
        return last_monday.day

    @staticmethod
    def get_first_sunday_of_month():
        """Date of the first Monday of the current month"""
        year_month = datetime.today().strftime('%Y-%m')
        first_sunday = np.busday_offset(year_month, 0, roll='forward', weekmask='Sun')
        return first_sunday.astype(date)

    @staticmethod
    def get_last_day_of_month():
        last_day = datetime.today() + relativedelta(day=31)
        return last_day.date().strftime("%d/%m/%Y")

    def get_sunday_of_week(self):
        self.page.locator(".week-period-loader").wait_for(state="hidden")
        self.page.locator(".header-loader.active").nth(1).wait_for(state="hidden")
        week_period = self.page.locator('.week-period').inner_text()
        sunday = week_period[week_period.index('-') + 2:-1]
        day = datetime.strptime(sunday, '%d/%m/%Y').date()
        return day

    def get_monday_of_week(self):
        week_days = self.page.locator("button[icon='pi pi-calendar'] .p-button-label").inner_text()
        pattern = r'\((\d+) - \d+'
        match = re.search(pattern, week_days)
        return int(match.group(1))

    def get_date_of_week_day(self, day_number):
        self.page.locator(".header-loader.active").nth(1).wait_for(state="hidden")
        week_period = self.page.locator('.week-period').inner_text()
        monday = week_period[1:week_period.index('-') - 1]
        day = datetime.strptime(monday, '%d/%m/%Y').date()
        return (day + timedelta(days=day_number-1)).strftime("%#d/%#m/%Y")

    def open_first_monday_of_month(self):
        self.wait.load_state_waiting()
        monday = self.get_first_monday_of_month()
        if int(monday.day) != self.get_monday_of_week():
            while not self.page.locator(".p-datepicker-calendar").is_visible():
                self.page.locator("button[icon='pi pi-calendar']").click()
            self.calendar.set_date([monday.day, monday.strftime('%b')])
        self.wait.skeleton_waiting()
        self.wait.progressbar_waiting()
        self.wait.load_state_waiting()

    
    def open_first_week_of_month(self):
        self.page.locator(".week-period-loader").wait_for(state="hidden")
        self.page.locator(".header-loader.active").nth(1).wait_for(state="hidden")
        if self.get_sunday_of_week() != self.get_first_sunday_of_month():
            while self.get_sunday_of_week() != self.get_first_sunday_of_month():
                self.page.locator(".period-previous").click()
                self.page.locator(".week-period-loader").wait_for(state="hidden")
        else:
            pass


    def open_third_week_of_month(self):
        self.page.locator(".week-period-loader").wait_for(state="hidden")
        self.page.locator(".header-loader.active").nth(1).wait_for(state="hidden")
        sunday = self.get_sunday_of_week()
        while sunday.day < 16:
            self.page.locator("a[title='Next'] i[class='mdi mdi-chevron-right']").click()
            sunday = self.get_sunday_of_week()

    
    def open_last_week_of_month(self):
        self.page.locator(".week-period-loader").wait_for(state="hidden")
        self.page.locator(".header-loader.active").nth(1).wait_for(state="hidden")
        monday = self.get_monday_of_week()
        while monday != self.get_last_monday_of_month():
            self.page.locator("a[title='Next'] i[class='mdi mdi-chevron-right']").click()
            monday = self.get_monday_of_week()
