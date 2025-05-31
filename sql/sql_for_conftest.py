import time
from config import env_config as env
from datetime import datetime, timedelta
from sql.sql_connection import SQLConnection
from config.config_data import PersonData as per_data


env_name = env.config['env_name']


class Conftest(SQLConnection):

    def delete_person_TT(self):
        self.cursor.execute(f'''SET NOCOUNT ON
                    declare @personId uniqueidentifier = (select Id from sp.person where Name = '{per_data.person_name}')
                    declare @date date = (SELECT DATEADD(month, -2, GETDATE()))
                    declare @tt_ids table (id uniqueidentifier)
                    declare @traking_ids table (id uniqueidentifier)

                    insert into @tt_ids select id from [TT].[TimeTracking] where Person_Id = @personId and Date >= @date
                    insert into @traking_ids select id from [TT].TrackingDate where PersonId = @personId and Date >= @date

                    SET NOCOUNT ON
                    delete from [TT].HoursOffUsed where TimeTrackingId in (select ID from TT.TimeTracking where Person_Id = @personId  and Date >=  @date)
                    delete from [TT].HoursOff where PersonId = @personId and DateAdd >= @date
                    --delete from [Archive].TimeTracking where Person_Id = @personId and Date >= @date
                    --delete from [Archive].TrackingDate where PersonId = @personId and Date >= @date
                    begin transaction
                    delete FROM [TT].[TimeTracking] where id in (select id from @tt_ids)  
                    delete FROM CTT_Export_{env_name}.[TT].[TimeTracking] where id in (select id from @tt_ids) 
                    commit transaction

                    update [cdc].TT_TimeTracking_CT
                    set  __$end_lsn = 0x00016CD9000001E80002
                    where Person_Id = @personId and Date >= @date and __$end_lsn is NULL

                    delete from CTT_Export_{env_name}.Export.WorkDescriptionReadyForExport where WorkDescriptionId in (select ID from [TT].WorkDescription where Person_Id = @personId and Date > @date)
                    delete from Export.WorkDescriptionReadyForExport where WorkDescriptionId in (select ID from [TT].WorkDescription where Person_Id = @personId and Date > @date)
                    delete from CTT_Export_{env_name}.[TT].WorkDescription where Person_Id = @personId and Date > @date
                    delete from [TT].WorkDescription where Person_Id = @personId and Date > @date
                    declare @ConversationID  TABLE(ConversationId int) INSERT into @ConversationID(ConversationId) 
                    select Conversation_Id from TT.ConversationCoordinats where Person_Id = @personId 
                    and TargetDate >  @date delete from TT.ConversationCoordinats where Conversation_Id in (select ConversationId from @ConversationID)delete from TT.Conversation where Id in (select ConversationId from @ConversationID)
                    begin transaction
                    update [TT].TrackingDate set IsSubmittedByEmployee = 0, IsSubmittedByDm = 0, IsSubmittedByHr = 0 where id in (select id from @traking_ids)
                    update CTT_Export_{env_name}.[TT].TrackingDate set IsSubmittedByEmployee = 0, IsSubmittedByDm = 0, IsSubmittedByHr = 0 where id in (select id from @traking_ids)
                    commit transaction

                    update [cdc].[TT_TrackingDate_CT]
                    set  __$end_lsn = 0x00016CD9000001E80002
                    where PersonId = @personId and Date >= @date and __$end_lsn is NULL

                    delete from [TT].TimeTrackingConflicts where TimeTrackingId in (select ID FROM [TT].[TimeTracking] where Person_Id = @personId and Date >@date)
                    delete from CTT_Export_{env_name}.[Export].[TimeTrackingForExport] where PersonId = @personId and Date >=  @date''')
        while self.cursor.nextset():
            pass
        self.cursor.commit()

    def update_cdc(self):
        self.cursor.execute(f'''SET NOCOUNT ON
                declare @personId uniqueidentifier = (select Id from sp.person where Name = '{per_data.person_name}')
                declare @date date = (SELECT DATEADD(month, -6, GETDATE()))
                declare @tt_ids table (id uniqueidentifier)

                insert into @tt_ids select id from [TT].[TimeTracking] where Person_Id = @personId and Date >= @date

                update [cdc].TT_TimeTracking_CT
                set  __$end_lsn = 0x00016CD9000001E80002
                where Person_Id = @personId and Date >= @date and __$end_lsn is NULL

                update [cdc].[TT_TrackingDate_CT]
                set  __$end_lsn = 0x00016CD9000001E80002
                where PersonId = @personId and Date >= @date and __$end_lsn is NULL

                delete FROM CTT_Export_{env_name}.[TT].[TimeTracking] where id in (select id from @tt_ids)
                    ''')
        while self.cursor.nextset():
            pass
        self.cursor.commit()
