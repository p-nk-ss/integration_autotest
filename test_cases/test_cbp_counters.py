
from page_objects.objects_creator import ObjectCreator
from page_objects.dates import DaysOfWeek
from config.config_data import WorkTypes
from config.config_data import CountersName
from config.config_data import ComPackageName
from config.config_data import PersonData


class TestCounters(ObjectCreator):
    compack = ComPackageName.AI_LP

    def test_turn_off_counter(self, setup_admin_compackage, setup_cbp_counters, setup_admin_counters):
        self.initialize_admin_compackage(setup_admin_compackage)
        self.initialize_cbp_absence(setup_cbp_counters)
        self.initialize(setup_admin_counters)
        try:
            self.cbp_absence.turn_off_counter(CountersName.DONATION, self.compack)
            setup_admin_compackage.reload()
            self.compackage.select_compensation_package(self.compack)
            assert counter_name.DONATION not in self.compackage_validation.get_list_displaying_counters()
            setup_admin_counters.reload()
            self.hours_off_search_person.select_person(PersonData.person_name)
            assert counter_name.DONATION not in self.counter_validation.get_person_available_counters()
        finally:
            self.cbp_absence.turn_on_counter(CountersName.DONATION, self.compack)

    def test_turn_off_all_counters(self, setup_admin_compackage, setup_cbp_counters, setup_admin_counters):
        self.initialize_admin_compackage(setup_admin_compackage)
        self.initialize_cbp_absence(setup_cbp_counters)
        self.initialize(setup_admin_counters)
        try:
            self.cbp_absence.turn_off_all_counters(self.compack)
            setup_admin_compackage.reload()
            self.compackage.select_compensation_package(self.compack)
            assert len(self.compackage_validation.get_list_displaying_counters()) == 0
            self.hours_off_search_person.select_person(PersonData.person_name)
            assert 'No results found' not in self.counter_validation.get_person_available_counters()
        finally:
            self.cbp_absence.turn_on_all_counters(self.compack)

    def test_use_available_counter(self, setup_ctt, setup_admin_compackage,  setup_cbp_counters, setup_admin_counters):
        self.initialize_admin_compackage(setup_admin_compackage)
        self.initialize_cbp_absence(setup_cbp_counters)
        self.initialize(setup_admin_counters)
        self.initialize_ctt(setup_ctt)
        start_date = str(DaysOfWeek.get_first_monday_of_month().day)
        self.cbp_absence.turn_on_counter(CountersName.DONATION, self.compack)
        setup_admin_compackage.reload()
        self.compackage.select_compensation_package(self.compack)
        assert CountersName.DONATION in self.compackage_validation.get_list_displaying_counters()
        setup_admin_counters.reload()
        self.hours_off_search_person.select_person(PersonData.person_name)
        self.persons_hours_off.add_hours_off(day=start_date, counter_name=CountersName.DONATION)
        self.counter_buttons.press_popup_add_item()
        setup_ctt.reload()
        self.day_of_week.open_first_monday_of_month()
        self.add_hours.add_dayoff_time(WorkTypes.DAY_OFF_INTERNALLY_COMPENSATED, "8", 2)
        assert self.ctt_personal_validation.get_day_off_input_value(WorkTypes.DAY_OFF_INTERNALLY_COMPENSATED, 2) == "8"
        setup_admin_counters.reload()
        assert self.ctt_personal_validation.get_day_date(2) in \
               self.counter_validation.get_list_of_dates_used_hours(CountersName.DONATION, "16")

