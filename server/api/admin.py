from django.contrib import admin

# Register your models here.

from . import models

@admin.register(models.Node)
class NodeAdmin(admin.ModelAdmin):
    list_display = ('node_name', 'name', 'node_type','update_time','create_time')
    list_display_links = ('node_name',)
    pass


@admin.register(models.App)
class AppAdmin(admin.ModelAdmin):
    list_display = ('id', 'owner', 'name', 'mark', 'upload_run_config','plan_start_time','start_running_time','end_running_time','abort_running_time','run_time_error', 'create_time','delete_time')
    list_display_links = ('id', 'owner', 'name',)
    pass


@admin.register(models.ActionLog)
class AppAdmin(admin.ModelAdmin):
    list_display = ('id', 'owner', 'action', 'action_type', 'action_data','mark','update_time', 'create_time','delete_time')
    list_display_links = ('id', 'owner', 'action',)
    pass


@admin.register(models.ErrorLog)
class AppAdmin(admin.ModelAdmin):
    list_display = ('id', 'owner', 'error', 'error_type', 'error_data','mark','update_time', 'create_time','delete_time')
    list_display_links = ('id', 'owner', 'error',)
    pass


