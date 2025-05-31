from page_objects.personal_view.work_type import WorkType
from sql.sql_delete_template import DeleteTemplate
from page_objects.page_buttons.hours_off_counters_buttons import CountersButtons
from page_objects.hours_off_counters_page.search_person import SearchPerson
from page_objects.hours_off_counters_page.person_counters import PersonCounters
from page_objects.personal_view.validation_personal_view import ValidationPersonalView
from page_objects.personal_view.Warnings import Warnings
from page_objects.page_buttons.ManagementCompanyViewButtons import Management_Company_button
from page_objects.hours_off_counters_page.counter_validation import CounterValidation
from page_objects.personal_view.NavigateButton import NavigateButton
from page_objects.dates import DaysOfWeek
from page_objects.personal_view.add_time import AddTime
from sql.sql_delivery import Delivery
from sql.sql_for_conftest import Conftest
from sql.sql_absence import AbsenceSQL
from sql.sql_assignment import Assignment
from sql.sql_staffrelationship import StaffRelationship
from sql.sql_store_procedures import Procedure
from sql.sql_com_package import Com_package
from sql.sql_projects import Projets
from sql.sql_for_precondition import Precondition
from sql.sql_calendar import Calendar
from sql.sql_delete_delivery import DeleteDelivery
from sql.sql_delete_custome_role import DeleteCustomRole
from utilities.pull_reload import Session
from page_objects.admin_compensation_package.AdminCompensationPackage import AdminCompensationPackage
from page_objects.admin_compensation_package.AdminCompensationPackageValidation import AdminCompensationPackageValidation
from page_objects.cbp.absence_type import AbsenceType
from page_objects.cbp.cbp_work_types import CBPWorkTypes
from page_objects.cbp.compackages import CBPCompackages


class ObjectCreator:

    @classmethod
    def initialize(cls, page):
        cls.hours_off_search_person = SearchPerson(page)
        cls.persons_hours_off = PersonCounters(page)
        cls.counter_buttons = CountersButtons(page)
        cls.counter_validation = CounterValidation(page)
        cls.sql_project = Projets()
        cls.sql_com_package = Com_package()
        cls.sql_procedure = Procedure()
        cls.sql_calendar = Calendar()
        cls.sql_assignment = Assignment()
        cls.sql_absence = AbsenceSQL()
        cls.sql_delete_template = DeleteTemplate()
        cls.sql_delete_delivery = DeleteDelivery()
        cls.dates = DaysOfWeek(page)
        cls.sql_delete_tt = Conftest()
        cls.sql_precondition = Precondition()
        cls.sql_delete_custom_role = DeleteCustomRole()
        cls.app_pull = Session()
        cls.ctt_navigate_buttons = NavigateButton(page)


    @classmethod
    def initialize_ctt(cls, setup):
        page = setup
        cls.add_hours = AddTime(page)
        cls.ctt_personal_validation = ValidationPersonalView(page)
        cls.day_of_week = DaysOfWeek(page)
        cls.add_work_types = WorkType(page)
        cls.ctt_warnings = Warnings(page)
        cls.ctt_navigate_buttons = NavigateButton(page)
        cls.management_button = Management_Company_button(page)
        cls.sql_procedure = Procedure()

    @classmethod
    def initialize_admin_compackage(cls, page):
        cls.compackage = AdminCompensationPackage(page)
        cls.compackage_validation = AdminCompensationPackageValidation(page)

    @classmethod
    def initialize_cbp_work_types(cls, page):
        cls.cbp_work_types = CBPWorkTypes(page)

    @classmethod
    def initialize_cbp_absence(cls, page):
        cls.cbp_absence = AbsenceType(page)

    @classmethod
    def initialize_cbp_compack(cls, page):
        cls.cbp_compackage = CBPCompackages(page)


    @classmethod
    def initialize_sql_query(cls):
        cls.sql_com_package = Com_package()
        cls.sql_procedure = Procedure()
        cls.sql_assignment = Assignment()
        cls.sql_absence = AbsenceSQL()
        cls.sql_delete_tt = Conftest()
        cls.sql_precondition = Precondition()
        cls.sql_delivery = Delivery()
        cls.app_pull = Session()
        cls.sql_calendar = Calendar()
        cls.sql_cm = CMJobs()
        cls.sql_confirm = Confirm()
        cls.sql_staffrelationship = StaffRelationship()
        cls.sql_project = Projets()
