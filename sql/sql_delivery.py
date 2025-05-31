from sql.sql_connection import SQLConnection
import time


class Delivery(SQLConnection):

    def delete_delivery(self, delivery_name):
        self.cursor.execute(f"""declare @projectid uniqueidentifier;
            select @projectid = id from sp.Project where name = '{delivery_name}'
            delete from tt.ConversationCoordinats where ProjectMarkValue_Id in (select id from tt.ProjectMarkValue where ProjectMarkId in (select id from tt.projectmark where projectid = @projectid))
            delete from tt.HoursOffUsed where TimeTrackingId in(select id from tt.TimeTracking where ProjectMarkValueId in (select id from tt.ProjectMarkValue where ProjectMarkId in (select id from tt.projectmark where projectid = @projectid)))
            delete from tt.TimeTracking where ProjectMarkValueId in (select id from tt.ProjectMarkValue where ProjectMarkId in (select id from tt.projectmark where projectid = @projectid))
            delete from tt.MarkCoefficient where ProjectMarkValueId in (select id from tt.ProjectMarkValue where ProjectMarkId in (select id from tt.projectmark where projectid = @projectid))
            delete from tt.ProjectMarkValue where ProjectMarkId in (select id from tt.projectmark where projectid = @projectid)
            delete from tt.projectmark where projectid = @projectid
            delete from tt.projecthierarchy where projectid = @projectid
            delete from tt.TemplateCoefficient where TemplateHierarchyValueId in (select id from tt.TemplateHierarchyValue where templatehierarchylevelid in (select id from tt.TemplateHierarchyLevel where TemplateVersionId in
            (select id from tt.TemplateVersion where templateid in (select id from tt.Template where LinkedProjectId = @projectid))))
            delete from tt.TemplateHierarchyValueDefinition where TemplateHierarchyValueId in (select id from tt.TemplateHierarchyValue where templatehierarchylevelid in (select id from tt.TemplateHierarchyLevel where TemplateVersionId in
            (select id from tt.TemplateVersion where templateid in (select id from tt.Template where LinkedProjectId = @projectid))))
            delete from tt.TemplateHierarchyValue where templatehierarchylevelid in (select id from tt.TemplateHierarchyLevel where TemplateVersionId in
            (select id from tt.TemplateVersion where templateid in (select id from tt.Template where LinkedProjectId = @projectid)))
            delete from tt.TemplateHierarchyLevel where TemplateVersionId in
            (select id from tt.TemplateVersion where templateid in (select id from tt.Template where LinkedProjectId = @projectid))
            delete from tt.EmailNotificationProject where ProjectId = @projectid
            delete from tt.EmailNotificationQueue where NotificationId in (select id from tt.EmailNotification where TemplateNotificationId in (select id from tt.TemplateNotification where TemplateId in (select id from tt.Template where LinkedProjectId = @projectid)))
            delete from tt.EmailNotification where TemplateNotificationId in (select id from tt.TemplateNotification where TemplateId in (select id from tt.Template where LinkedProjectId = @projectid))
            delete from tt.NotificationEmails where NotificationId in (select id from tt.TemplateNotification where TemplateId in (select id from tt.Template where LinkedProjectId = @projectid))
            delete from tt.TemplateNotification where TemplateId in (select id from tt.Template where LinkedProjectId = @projectid)
            delete from tt.TemplateSettings where TemplateVersionId in (select id from tt.TemplateVersion where templateid in (select id from tt.Template where LinkedProjectId = @projectid))
            delete from tt.TemplateVersion where templateid in (select id from tt.Template where LinkedProjectId = @projectid)
            delete from tt.Template where LinkedProjectId = @projectid
            delete from tt.ConfigurationEnabledProjects where ProjectId = @projectid""")
        self.cursor.commit()

    def set_delivery_start_date(self, start_date, project_name):
        update = self.cursor_ESD.execute(
            f"""UPDATE SP.Project
                SET StartDate = '{start_date}'
                WHERE Name='{project_name}'""")
        update.commit()
        return update

    def set_delivery_finish_date(self, finish_date, project_name):
        update = self.cursor_ESD.execute(
            f"""UPDATE SP.Project
                SET FinishDate = '{finish_date}'
                WHERE Name='{project_name}'""")
        update.commit()
        return update