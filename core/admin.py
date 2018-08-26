from django.contrib import admin

from core.models import Assignee, Organization, Task


@admin.register(Assignee)
class AssigneeAdmin(admin.ModelAdmin):
    readonly_fields = ["organiz_login"]


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    pass


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    pass
