from sql.sql_connection import SQLConnection
import time
from config.config_data import PersonData as per_data


class Procedure(SQLConnection):

    def run_main_load(self):
        time.sleep(10)
        self.cursor.execute("""SET NOCOUNT ON; EXEC	[Import].[MainLoad]""")
        while self.cursor.nextset():
            pass
        self.cursor.commit()

    def actualize_project_hierarchy(self):
        self.cursor.execute('''SET NOCOUNT ON; DECLARE	@return_value int,
                    @AffectedRecords int
                    EXEC	@return_value = [Admin].[ActualizeProjectHierarchy]
                    @AffectedRecords = @AffectedRecords OUTPUT
                    SELECT	@AffectedRecords as N'@AffectedRecords'
                    SELECT	'Return Value' = @return_value''')
        while self.cursor.nextset():
            pass
        self.cursor.commit()

    def actualize_time_tracking(self):
        self.cursor.execute('''SET NOCOUNT ON; DECLARE	@return_value int,
                   @AffectedRecords int
                   EXEC	@return_value = [Export].[ActualizeTimeTracking]
                   @AffectedRecords = @AffectedRecords OUTPUT
                   SELECT	@AffectedRecords as N'@AffectedRecords'
                   SELECT	'Return Value' = @return_value''')
        while self.cursor.nextset():
            pass
        self.cursor.commit()

    def recalculate_absence(self):
        self.cursor.execute('''SET NOCOUNT ON; declare @d1 date = (SELECT DATEADD(m, DATEDIFF(m, 0, GETDATE()), 0))
        declare @d2 date = (SELECT DATEADD(m, DATEDIFF(m, 0, GETDATE()), 31))
        DECLARE	@return_value int
        DECLARE @personIds tt.GuidList
        insert into @personIds values ('5DBA117B-77DF-4A73-B2D0-C8D242A805AB')
        select *from @personIds
        EXEC	@return_value = [TT].[ActualizePersonsCalculatedData]
        @RequestorId = '5DBA117B-77DF-4A73-B2D0-C8D242A805AB',
        @From = @d1,
        @To = @d2,
        @PersonIds = @personIds --'3CF545CC-1B44-453C-9100-7999D3EBCC37'
        SELECT	'Return Value' = @return_value''')
        while self.cursor.nextset():
            pass
        self.cursor.commit()

    def recalculate_conflicts(self):
        self.cursor.execute(f'''SET NOCOUNT ON; 
            DECLARE @RC int
            DECLARE @PersonsToCheck [TT].[GuidListIndexed]
            DECLARE @IsPersonCompensationPackageHistorySource bit = 1
            DECLARE @IsCompensationPackageSource bit = 1
            DECLARE @IsCompensationPackageInfoSource bit = 1
            DECLARE @IsStaffRelationshipSource bit = 1
    
            insert into @PersonsToCheck select '{PersonData.person_id}'
            EXECUTE @RC = [Import].[CheckTimeTrackingConflicts] 
            @PersonsToCheck 
            ,@IsPersonCompensationPackageHistorySource
            ,@IsCompensationPackageSource
            ,@IsCompensationPackageInfoSource
            ,@IsStaffRelationshipSource''')
        while self.cursor.nextset():
            pass
        self.cursor.commit()
