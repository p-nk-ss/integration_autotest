from sql.sql_connection import SQLConnection

from config.config_data import PersonData
from config.config_data import WorktypesId


class Precondition(SQLConnection):

    def get_roles_from_assignment(self):
        select = self.connection_ESD.cursor().execute(
            f"""
            SELECT Role_Id FROM [SP].[Assignment] where Person_Id = '{per_data.person_id}'
            """)
        return [row.Role_Id for row in select]

    def get_projects_from_assignment(self):
        select = self.connection_ESD.cursor().execute(
            f"""
                SELECT Project_Id FROM [SP].[Assignment] where Person_Id = '{per_data.person_id}'
            """)
        return [row.Project_Id for row in select]

    def get_project_manager_id(self, project_id):
        select = self.connection_ESD.cursor().execute(
            f"""select Manager_Id from SP.Project where Id = '{project_id}'""").fetchone()
        return select[0]

    def get_person_compackage_id(self):
        select = self.connection_ESD.cursor().execute(
            f"""select CompensationPackage_Id from [SP].[PersonCompensationPackageHistory] 
                where Person_Id = '{PersonData.person_id}'""").fetchone()
        return select[0]

    def get_worktypes_from_assignment(self, project_id):
        select = self.connection.cursor().execute(
            f"""
                SELECT MarkValueId FROM TT.ProjectHierarchy where ProjectId = '{project_id}'
            """)
        return [row.MarkValueId for row in select]

    def actualize_worktypes_project(self, project_id, project_name):
        self.connection.cursor().execute(
            f"""update TT.ProjectHierarchy
                set FinishDate = '9999-12-31'
                where ProjectId = '{project_id}'""").commit()
        self.connection.cursor().execute(
            f"""update tt.projectmarkvalue
                set FinishDate = NULL
                where ProjectMarkId = 
                (SELECT top 1 ProjectMarkId FROM TT.ProjectHierarchy where ProjectId 
                = '{project_id}')""").commit()
        self.connection.cursor().execute(
            f"""exec [Admin].[AddHierarchyLevelToProject] '{project_id}', 2, NULL, 
                    '5DBA117B-77DF-4A73-B2D0-C8D242A805AB'""").commit()
        select = self.connection.cursor().execute(
            f"""SELECT MarkValueId FROM TT.ProjectHierarchy where ProjectId = '{project_id}'""")
        existing_ids = [row.MarkValueId for row in select]
        for ids in WorktypesId.worktypes_id_list:
            if ids not in existing_ids:
                self.connection.cursor().execute(f"""SET NOCOUNT ON;
                 declare @emptytable tt.guidlist
                 declare @deftable tt.markdefinition
                 exec [Admin].[AddMarkValuesToHierarchy] '{project_id}', 2,
                '{ids}', '2022-01-01', NULL, NULL, @emptytable, NULL, @emptytable,
                '5DBA117B-77DF-4A73-B2D0-C8D242A805AB' , 1, 1, @deftable""")
            while self.connection.cursor().nextset():
                pass
            self.connection.cursor().commit()
        check_pilot = self.connection.cursor().execute(
            f"""SELECT [ProjectId]
                        FROM [TT].[ConfigurationEnabledProjects]
                        where  ProjectId = '{project_id}'""").commit()
        if not check_pilot:
            self.add_to_pilot(project_id, project_name)
        self.connection.cursor().execute(
            f"""exec [Admin].[SetDefaultMarkValue] '{project_id}', 2,
             'C50575B4-FD99-4FB2-9028-F69B752DAACD','5DBA117B-77DF-4A73-B2D0-C8D242A805AB', NULL, 1""").commit()
        self.connection.cursor().execute(
            f"""exec [Admin].[SetCommentRequirement] '{project_id}',2, 
            'E15A368F-63C8-470C-926A-94CE92F3D88E', '5DBA117B-77DF-4A73-B2D0-C8D242A805AB', 1""").commit()

    def set_project_attributes(self, project_id):  # set project tt step 0.01
        insert = self.connection.cursor().execute(
            f"""insert into [TT].[ProjectAttributes] 
            (id, ProjectId, AttributeId, AttributeValue, StartDate, EndDate, CreateBy,CreateDate, ModifiedBy, ModifiedDate, IsActive)
            values(NEWID(),'{project_id}', 1, NULL, '2022-08-01', NULL, '73096F2F-F8CB-4906-8192-9D0AF9481BF5', '2022-08-18', NULL,NULL, 1)""")
        return insert

    def update_project_state_finish_date(self):
        update = self.connection_ESD.cursor().execute(
            f"""update SP.Project
                set State_Id = '1061979B-12C7-463E-AC3B-24D75C37677C',
                FinishDate = NULL
                where Id in ('E6A5044C-5770-4D30-883F-A56365B98473', '962F8E69-9FAF-4F2F-A502-CE8D166489C8', 
                '1ADB7C32-47AE-44CF-8F9C-A90327EB1B09', '6053EA2C-BED8-4E53-BC2A-04A50CD1B55F', 
                '4A19BE71-2E7E-47AA-84F5-0DADFE9AFCEA', 'A215EEE4-4392-48A2-AC29-040562708EBB')""")
        return update

    def setup_project_with_levels(self, project_id, project_name):
        self.copy_closed_projects_hierarchy()
        self.set_items_start_finish()
        self.add_to_pilot(project_id, project_name)

    def add_to_pilot(self, project_id, project_name):
        self.connection.cursor().execute(
            f"""insert into [TT].[ConfigurationEnabledProjects]
                (ProjectId, ProjectName, PilotStartDate)
                values ('{project_id}', '{project_name}', '2022-01-01')""").commit()

    def copy_closed_projects_hierarchy(self):
        self.cursor.execute("""SET NOCOUNT ON; 
                DECLARE @StartDate DATE = (SELECT DATEADD(m, DATEDIFF(m, 0, GETDATE()), 0));
                DECLARE @ModifiedByName NVARCHAR(MAX) = 'Mykhailo Yefremov';
                DECLARE @ProjectsList TABLE(OldProjectName NVARCHAR(MAX), NewProjectName NVARCHAR(MAX));
                INSERT INTO @ProjectsList(OldProjectName, NewProjectName) VALUES
                ('Econocom-Flow', 'Pythagoras')
                
                BEGIN TRANSACTION;
                BEGIN TRY 	
                    DECLARE @ModifiedById UNIQUEIDENTIFIER;
                    SELECT @ModifiedById = [Id] FROM [SP].[Person] WHERE [Name] = @ModifiedByName;
                    IF @ModifiedById IS NULL
                    BEGIN
                        DECLARE @errorMessage1 NVARCHAR(MAX) = CONCAT(N'Can''t find ModifiedBy person with Name - ', @ModifiedByName);
                        THROW 51000, @errorMessage1, 1;
                    END
                
                    DECLARE 
                        @OldProjectName NVARCHAR(MAX),
                        @NewProjectName NVARCHAR(MAX),
                        @CurrentIndex INT = 0;
                    DECLARE ChangeTimeLogsCurson CURSOR FOR
                        SELECT OldProjectName, NewProjectName
                        FROM @ProjectsList
                    OPEN ChangeTimeLogsCurson;
                    WHILE 1=1
                    BEGIN
                        FETCH NEXT FROM ChangeTimeLogsCurson INTO 
                             @OldProjectName
                            ,@NewProjectName;
                        IF @@FETCH_STATUS < 0 BREAK;
                        SET @CurrentIndex = @CurrentIndex + 1;
                        DECLARE @OldProjectId UNIQUEIDENTIFIER;
                        SELECT @OldProjectId = Id FROM [SP].[Project] WHERE Name = @OldProjectName
                        DECLARE @NewProjectId UNIQUEIDENTIFIER;
                        SELECT @NewProjectId = Id FROM [SP].[Project] WHERE Name = @NewProjectName
                        DECLARE @ExistingHierarchyId UNIQUEIDENTIFIER;
                        select @ExistingHierarchyId = id from tt.ProjectHierarchy where ProjectId = @NewProjectId
                        IF @ExistingHierarchyId IS NOT NULL
                        BEGIN
                            DECLARE @errorMessage11 NVARCHAR(MAX) = CONCAT(N'Existing hierarchy. Project name - ', @NewProjectName);
                            THROW 51000, @errorMessage11, 1;
                        END
                
                        IF (@OldProjectId IS NOT NULL AND @NewProjectId IS NOT NULL)
                        BEGIN
                            DECLARE @NewProjectMarkTable TABLE([OldId] UNIQUEIDENTIFIER, [OldHierarchyId] UNIQUEIDENTIFIER, [NewId] UNIQUEIDENTIFIER);
                            INSERT INTO @NewProjectMarkTable(OldId, OldHierarchyId, NewId)
                            SELECT [Id], [HierarchyId], NEWID()
                            FROM [TT].[ProjectMark] WHERE [ProjectId] = @OldProjectId
                            INSERT INTO [TT].[ProjectMark](
                                 [Id]
                                ,[HierarchyId]
                                ,[ProjectId]
                                ,[MarkId]
                                ,[OrderNumber]
                                ,[IsActive]
                                ,[CreatedBy]
                                ,[Created]
                                ,[ModifiedBy]
                                ,[Modified]
                                ,[ParentId]
                                ,[IsDeleted]
                                ,[StateId]
                                ,[FinishDate]
                                ,[StartDate])
                            SELECT 
                                 npmt.NewId
                                ,parents.NewId
                                ,@NewProjectId
                                ,pm.[MarkId]
                                ,pm.[OrderNumber]
                                ,pm.[IsActive]
                                ,@ModifiedById
                                ,GETDATE()
                                ,@ModifiedById
                                ,GETDATE()
                                ,pm.[ParentId]
                                ,pm.[IsDeleted]
                                ,pm.[StateId]
                                ,pm.FinishDate
                                ,IIF(pm.StartDate > @StartDate, pm.StartDate, @StartDate)
                            FROM [TT].[ProjectMark] pm
                            JOIN @NewProjectMarkTable npmt on npmt.OldId = pm.Id
                            JOIN [SP].Project newProject on newProject.Id = @NewProjectId
                            LEFT JOIN @NewProjectMarkTable parents ON parents.OldHierarchyId = pm.Id
                            WHERE ProjectId = @OldProjectId
                            PRINT ('[TT].[ProjectMark] was updated.')
                            DECLARE @NewProjectMarkValueTable TABLE([OldId] UNIQUEIDENTIFIER, [OldHierarchyId] UNIQUEIDENTIFIER, [NewId] UNIQUEIDENTIFIER);
                            INSERT INTO @NewProjectMarkValueTable(OldId, OldHierarchyId, NewId)
                            SELECT pmv.[Id], pmv.[HierarchyId], NEWID()
                            FROM [TT].[ProjectMarkValue] pmv 
                            JOIN [TT].[ProjectHierarchy] ph on ph.[Id] = pmv.[Id]
                            WHERE ph.ProjectId = @OldProjectId
                
                            INSERT INTO [TT].[ProjectMarkValue](
                                 [Id]
                                ,[HierarchyId]
                                ,[ProjectMarkId]
                                ,[MarkValueId]
                                ,[OrderNumber]
                                ,[IsActive]
                                ,[CreatedBy]
                                ,[StartDate]
                                ,[ModifiedBy]
                                ,[Modified]
                                ,[ParentId]
                                ,[IsDeleted]
                                ,[StateId]
                                ,[IsVisible]
                                ,[IsDefault]
                                ,[FinishDate]
                                ,[IsCommentRequired])
                            SELECT
                                 npmvt.NewId
                                ,parent.[NewId]
                                ,npmt.NewId
                                ,pmv.[MarkValueId]
                                ,pmv.[OrderNumber]
                                ,pmv.[IsActive]
                                ,@ModifiedById
                                ,IIF(pmv.StartDate > @StartDate, pmv.StartDate, @StartDate)
                                ,@ModifiedById
                                ,GETDATE()
                                ,subtype.NewId
                                ,pmv.[IsDeleted]
                                ,pmv.[StateId]
                                ,pmv.[IsVisible]
                                ,pmv.[IsDefault]
                                ,pmv.[FinishDate]
                                ,pmv.[IsCommentRequired]
                            FROM [TT].[ProjectMarkValue] pmv
                            JOIN @NewProjectMarkValueTable npmvt ON npmvt.OldId = pmv.Id
                            JOIN [SP].Project newProject on newProject.Id = @NewProjectId
                            JOIN @NewProjectMarkTable npmt on npmt.OldId = pmv.ProjectMarkId
                            LEFT JOIN @NewProjectMarkValueTable parent ON parent.OldId = pmv.HierarchyId
                            LEFT JOIN @NewProjectMarkValueTable subtype ON subtype.OldId = pmv.ParentId
                            PRINT ('[TT].[ProjectMarkValue] was updated.')
                            INSERT INTO [TT].[ProjectMarkValueDefinition](
                               [ProjectMarkValueId]
                              ,[MarkDefinitionId]
                              ,[Value])
                            SELECT 
                                 npmvt.NewId
                                ,pmvd.MarkDefinitionId
                                ,pmvd.Value
                            FROM [TT].[ProjectMarkValueDefinition] pmvd
                            JOIN @NewProjectMarkValueTable npmvt on npmvt.OldId = pmvd.ProjectMarkValueId
                            PRINT ('[TT].[ProjectMarkValueDefinition] was updated.')
                            INSERT INTO [TT].[MarkCoefficient](
                               [Id]
                              ,[CoefficientTypeId]
                              ,[CoefficientValue]
                              ,[ProjectMarkValueId]
                              ,[StartDate]
                              ,[FinishDate]
                              ,[ModifiedBy]
                              ,[Modified])
                            SELECT 
                                 NEWID()
                                ,mc.[CoefficientTypeId]
                                ,mc.[CoefficientValue]
                                ,npmvt.NewId
                                ,mc.[StartDate]
                                ,mc.[FinishDate]
                                ,@ModifiedById
                                ,GETDATE()
                            FROM [TT].[MarkCoefficient] mc
                            JOIN @NewProjectMarkValueTable npmvt on npmvt.OldId = mc.ProjectMarkValueId
                            PRINT ('[TT].[MarkCoefficient] was updated.')
                            PRINT CONCAT ('Project hierarchy is start to updating for project - ', @NewProjectName)
                            DECLARE @AffectedRecords INT;
                            EXEC [Admin].[ActualizeProjectHierarchyByProjectId] @NewProjectId, @AffectedRecords;
                            PRINT CONCAT ('Update project hierarchy was successfully - ', @NewProjectName)
                        END		
                    END
                    CLOSE ChangeTimeLogsCurson;
                    DEALLOCATE ChangeTimeLogsCurson;
                    COMMIT TRANSACTION;
                END TRY
                BEGIN CATCH
                    ROLLBACK TRANSACTION;
                    DECLARE @errorMessage NVARCHAR(MAX) = CONCAT(
                            N'Something went wrong during the execution at ''', 
                            CONVERT(NVARCHAR, GETDATE(), 127), '''. Exception message: ', ERROR_MESSAGE());
                    THROW 51000, @errorMessage, 1;
                END CATCH""")
        while self.cursor.nextset():
            pass
        self.cursor.commit()

    def set_items_start_finish(self):
        self.cursor.execute("""
          update [TT].[ProjectMarkValue]
              set StartDate = (select DATEADD(wk, DATEDIFF(wk,0, dateadd(dd,6-datepart(day,getdate()),getdate())), 0)),
               FinishDate = '9999-12-31'
              where ProjectMarkId = (select top 1 ProjectMarkId from TT.ProjectHierarchy where ProjectId = 
              'F26792C4-1E99-4FD7-BBF7-3B755AF8F1A6' and MarkName = 'Work Type')
            
              update [TT].[ProjectMarkValue]
              set StartDate = (select DATEADD(wk, DATEDIFF(wk,0, dateadd(dd,6-datepart(day,getdate()),getdate())), +7)),
               FinishDate = '9999-12-31'
              where ProjectMarkId = (select top 1 ProjectMarkId from TT.ProjectHierarchy where ProjectId = 
              'F26792C4-1E99-4FD7-BBF7-3B755AF8F1A6' and MarkName = 'Activity')
            
              update [TT].[ProjectMarkValue]
              set StartDate = (select DATEADD(wk, DATEDIFF(wk,0, dateadd(dd,6-datepart(day,getdate()),getdate())), +7)),
               FinishDate = (select DATEADD(wk, DATEDIFF(wk,0, dateadd(dd,6-datepart(day,getdate()),getdate())), +13))
              where ProjectMarkId = (select top 1 ProjectMarkId from TT.ProjectHierarchy where ProjectId = 
              'F26792C4-1E99-4FD7-BBF7-3B755AF8F1A6' and MarkName = 'Cost Center')
        """)
        while self.cursor.nextset():
            pass
        self.cursor.commit()

    def set_export_absence_required(self, compackage_id):
        update = self.connection.cursor().execute(
            f"""
            update [TT].[CompensationPackageInfo]
            set IsAbsenceExportedToSharepoint = 1
            where CompensationPackageId = '{compackage_id}'""")
        update.commit()
        return update

    def actualize_worktypes_compackage(self, compackage_id):
        select = self.connection.cursor().execute(
            f"""select WorkTypeId from [TT].[CompensationPackageWorkTypeGroup]
                where CompensationPackageId = '{compackage_id}'""")
        existing_ids = [row.WorkTypeId for row in select]
        for ids in WorktypesId.worktypes_id_list_compackage:
            if ids not in existing_ids:
                self.connection.cursor().execute(f"""  
                insert into [TT].[CompensationPackageWorkTypeGroup]
                (CompensationPackageId, WorkTypeId)
                values('{compackage_id}', '{ids}')""")
            while self.connection.cursor().nextset():
                pass
            self.connection.cursor().commit()


