from sql.sql_connection import SQLConnection

from config.config_data import PersonData as per_data
from config.config_data import RoleId as role_id
from config.config_data import ProjectId as projId


class Projets(SQLConnection):

    def add_project_to_assignment(self, project_id):
        insert = self.connection_ESD.cursor().execute(
            f"""
                insert into [SP].[Assignment] (Id, Person_Id, Project_Id, Role_Id, Manager_Id, State_Id, DateFrom, DateTo, EmploymentLevel, Execution, ContractPosition_Id, Workplace_Id, Sp_Id)
                values (NEWID(), '{PersonData.person_id}', '{project_id}', '{role_id.Employee}', '20F95CB3-D4C6-4F95-83DA-C55D929F4620', '1061979B-12C7-463E-AC3B-24D75C37677C', '2022-11-01', NULL, 100, '2022-03-08 14:02:56.373', 'B002DAA6-8C1D-4DD6-9A57-C9DD698694E4', '049E6F9D-BA14-4755-9A3B-538177406CA5', '38471')
                       """)
        insert.commit()
        return insert

    def delete_project_from_assignment(self, project_id):
        insert = self.connection_ESD.cursor().execute(
            f"""delete from sp.Assignment where Person_Id = '{PersonData.person_id}' 
            and Project_Id = '{project_id}'""")
        insert.commit()
        return insert
