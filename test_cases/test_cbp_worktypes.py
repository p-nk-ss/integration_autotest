from page_objects.objects_creator import ObjectCreator
from config.config_data import ProjectNames
from config.config_data import WorkTypes
from config.config_data import ComPackageName
import pytest


class TestWorktypes(ObjectCreator):
    compack = ComPackageName.AI_LP
    @pytest.mark.smoke
    def test_turn_off_all_work_types(self, setup_cbp_work_types, setup_admin_compackage, setup_ctt):
        self.initialize_ctt(setup_ctt)
        self.initialize_admin_compackage(setup_admin_compackage)
        self.initialize_cbp_work_types(setup_cbp_work_types)
        self.initialize_sql_query()
        try:
            self.cbp_work_types.turn_off_all_work_types(self.compack)
            setup_admin_compackage.reload()
            self.compackage.select_compensation_package(self.compack)
            assert len(self.compackage_validation.get_list_displaying_work_types()) == 0
            self.app_pull.restart_pull_CTT()
            setup_ctt.reload(wait_until="networkidle")
            self.day_of_week.open_first_monday_of_month()
            assert self.ctt_personal_validation.is_warning_time_tracking_should_not_filled_displaying() is True
        finally:
            self.cbp_work_types.turn_on_all_work_types(self.compack)

    def test_hours_conflict(self, setup_cbp_work_types, setup_ctt):
        """Turn off work type after entering TT hours"""
        self.initialize_ctt(setup_ctt)
        self.initialize_cbp_work_types(setup_cbp_work_types)
        try:
            self.day_of_week.open_first_monday_of_month()
            self.add_hours.add_work_time(ProjectNames.IT_TECHGOVERNANCE, WorkTypes.WORK_REGULAR, "8", 1)
            self.cbp_work_types.turn_off_work_type(WorkTypes.WORK_REGULAR, self.compack)
            self.sql_procedure.recalculate_conflicts()
            setup_ctt.reload()
            self.day_of_week.open_first_monday_of_month()
            assert self.ctt_personal_validation.is_conflict_hours_displaying(ProjectNames.IT_TECHGOVERNANCE,
                                                                             WorkTypes.WORK_REGULAR, 1) is True
        finally:
            self.cbp_work_types.turn_on_work_type(work_type.WORK_REGULAR, self.compack)



