from datetime import date
from config.config_data import ProjectId as project_id
from config.config_data import ComPackageId as compackage_id
from config.config_data import RoleId as role_id
from config.config_data import ProjectNames as project_name
from config.config_data import PersonData as pers_data
from page_objects.objects_creator import ObjectCreator
from config.config_data import LegalEntityId as legal_entity_id


class Precondition(ObjectCreator):

    def precondition(self):
        self.initialize_sql_query()
        self.sql_infopulse_connect.update_date_current_location(date.today().replace(day=1))
        if role_id.Personnel_Inspector not in self.sql_precondition.get_roles_from_assignment():
            self.sql_assignment.add_PI_role()
        if project_id.IT_TECHGOVERNANCE_ID not in self.sql_precondition.get_projects_from_assignment():
            self.sql_project.add_project_to_assignment(project_id.IT_TECHGOVERNANCE_ID)
        if project_id.IT_BCP_RELOCATION_ID not in self.sql_precondition.get_projects_from_assignment():
            self.sql_project.add_project_to_assignment(project_id.IT_BCP_RELOCATION_ID)
        if self.sql_precondition.get_project_manager_id(project_id.IT_TECHGOVERNANCE_ID) != pers_data.person_id:
            self.sql_assignment.add_management_role(project_id.IT_TECHGOVERNANCE_ID)
        if self.sql_precondition.get_project_manager_id(project_id.IT_BCP_RELOCATION_ID) != pers_data.person_id:
            self.sql_assignment.add_management_role(project_id.IT_BCP_RELOCATION_ID)
        self.sql_staffrelationship.clear_staffrelationship_person_compackage()
        self.sql_staffrelationship.delete_all_staffrelationship_esd()
        self.sql_staffrelationship.add_new_staffrelationship(compackage_id=compackage_id.AI_LP,
                                                             main_1_or_0=1,
                                                             legal_entity_id=legal_entity_id.INFOPULSE_UKRAINE, )
        self.sql_project.delete_project_from_assignment("931B3AFB-05B0-418C-9807-41326B44E5DA")
        self.sql_project.delete_project_from_assignment("43ECAC65-5B32-4B96-BFD4-87CBB237BFEF")
        self.sql_precondition.update_project_state_finish_date()
        self.sql_procedure.run_main_load()
        self.sql_delivery.delete_delivery(project_name.IT_TECHGOVERNANCE)
        self.sql_delivery.delete_delivery(project_name.IT_BCP_RELOCATION)
        self.sql_precondition.actualize_worktypes_project(project_id.IT_TECHGOVERNANCE_ID, project_name.IT_TECHGOVERNANCE)
        self.sql_precondition.actualize_worktypes_project(project_id.IT_BCP_RELOCATION_ID, project_name.IT_BCP_RELOCATION)
        self.sql_precondition.actualize_worktypes_compackage(compackage_id=compackage_id.AI_LP)
        self.sql_precondition.set_export_absence_required(compackage_id=compackage_id.AI_LP)
        self.sql_procedure.actualize_project_hierarchy()
        self.sql_precondition.set_project_attributes(project_id.IT_TECHGOVERNANCE_ID)
        self.app_pull.restart_pull_CTT()



# set_cond = Precondition()
# set_cond.precondition()
