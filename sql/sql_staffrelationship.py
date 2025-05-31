from page_objects.dates import DaysOfWeek as days
from sql.sql_connection import SQLConnection
from config.config_data import PersonData as per_data
from datetime import date, datetime, timedelta


class StaffRelationship(SQLConnection):


    # SP_id, Execution, Modified must be different(greater) in the second tenant
    def add_new_staffrelationship(self, compackage_id,
                                  legal_entity_id,
                                  main_1_or_0=0,
                                  start_date=days.get_first_monday_of_month(),
                                  finish_date=None,
                                  person_id=per_data.person_id,
                                  add_same_legal_entity=False,
                                  sp_id=2332,
                                  compackage_start_date=days.get_first_monday_of_month(),
                                  execution=datetime.today().date(),
                                  modified=datetime.today().date()
                                  ):

        count = self.connection_ESD.cursor().execute(
            f"""
                            SELECT COUNT(*)
                            FROM [SP].[StaffRelationship]
                            WHERE LegalEntity_Id = '{legal_entity_id}' and FullNameEn_Id = '{person_id}'
                        """
        ).fetchone()[0]

        if count > 0 and add_same_legal_entity is False:
            return
        if finish_date is None:
            finish_date_sql = 'NULL'
        else:
            finish_date_sql = f"'{finish_date}'"
        insert = self.cursor_ESD.execute(
            f"""
            INSERT into [SP].[StaffRelationship] (Id, FullNameEn_Id, StartDate, FinishDate, GroupLeader_Id, 
            CompPackage_Id, CompPackageStartDate, RelationshipType_Id, MainLE, LegalEntity_Id, PartnerCompany_Id, 
            SP_Id, Execution, State_Id, Modified, PartnerCompany_GUID)
            VALUES(NEWID ( ),'{person_id}', '{start_date}', {finish_date_sql}, '93D70AA8-7330-4862-92CC-50BA846CDA9F', 
            '{compackage_id}', '{compackage_start_date}', '64961C2B-EDA3-4D8E-B4B8-C65315AEC2E1', {main_1_or_0}, 
            '{legal_entity_id}', '00000000-0000-0000-0000-000000000000', '{sp_id}', 
            '{execution}', '1061979B-12C7-463E-AC3B-24D75C37677C', 
            '{modified}', '00000000-0000-0000-0000-000000000000')
            """)
        insert.commit()
        return insert


    def delete_all_staffrelationship_esd(self, person_id=per_data.person_id):
        delete = self.cursor_ESD.execute(
            f"""
            DELETE from  [SP].[StaffRelationship] where FullNameEn_Id='{person_id}'
            """)
        delete.commit()
        return delete

    def clear_staffrelationship_person_compackage(self, person_id=PersonData.person_id):
        delete = self.cursor.execute(
            f"""
            DELETE [SP].[StaffRelationship]
            where FullNameEn_Id = '{person_id}'
            DELETE [SP].[PersonCompensationPackageHistory] 
            where PersonId = '{person_id}'
            """)
        delete.commit()
        return delete

