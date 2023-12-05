from django.db import models
from django.contrib.auth.models import User
import uuid
import json
import os
from django.utils import timezone
from datetime import datetime

# Define user directory path


def app_user_path(instance, filename):
    filename = 'AutoRunX-RunConfig.%s' % filename.split('.')[-1].lower()
    return os.path.join('app', str(instance.id), filename)

# Create your models here.


class Node(models.Model):
    uuid = models.UUIDField(primary_key=True,
                            default=uuid.uuid4,
                            editable=False,
                            help_text="self ID")
    node_name = models.CharField(max_length=128,
                                 blank=False,
                                 help_text="module name, unique but delete")
    id = models.CharField(max_length=128,
                          blank=True,
                          default="",
                          help_text="node id for AutoRunX, auto generate by program")
    name = models.CharField(max_length=128,
                            blank=False,
                            db_index=True,
                            help_text="node name")
    node_type = models.CharField(max_length=4,
                                 blank=False,
                                 choices=(
                                     ("evtx", "event transmit"),
                                     ("evrx", "event receive"),
                                     ("dtio", "data input/output"),
                                     ("dtpc", "data process"),
                                     ("ctrl", "flow control"),
                                     ("func", "flow function")
                                 ),
                                 help_text="node type")
    pre_edge_id = models.TextField(blank=False,
                                   default="[]",)
    nxt_edge_id = models.TextField(blank=False,
                                   default="[]",)
    input = models.TextField(blank=False,
                             default="{}",)
    input_type = models.TextField(blank=False,
                                  default="{}",)
    input_intro = models.TextField(blank=False,
                                   default="{}",)
    output = models.TextField(blank=False,
                              default="{}",)
    output_type = models.TextField(blank=False,
                                   default="{}",)
    output_intro = models.TextField(blank=False,
                                    default="{}",)
    readme = models.TextField(blank=True,
                              default='',
                              null=True,
                              help_text='README.md')
    update_time = models.DateTimeField(auto_now=True)
    create_time = models.DateTimeField(auto_now_add=True)
    delete_time = models.DateTimeField(blank=True,
                                       null=True,
                                       default=None,
                                       help_text='logic delete')


class App(models.Model):
    id = models.UUIDField(primary_key=True,
                          default=uuid.uuid4,
                          editable=False,
                          help_text="self ID")
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=128,
                            blank=False,
                            help_text='self name')
    upload_run_config = models.BooleanField(blank=False,
                                            default=False,
                                            help_text='whether to upload run configuration file')
    run_config_file = models.FileField(upload_to=app_user_path,
                                       blank=True,
                                       null=True,
                                       help_text='run configuration file')
    plan_start_time = models.DateTimeField(blank=True,
                                           null=True,
                                           help_text='time of planning to start')
    start_running_time = models.DateTimeField(blank=True,
                                              null=True,
                                              help_text='start running time')
    end_running_time = models.DateTimeField(blank=True,
                                            null=True,
                                            help_text='end running time')
    abort_running_time = models.DateTimeField(blank=True,
                                              null=True,
                                              help_text='manual or abnormal abort running time')
    run_time_error = models.TextField(blank=True,
                                      default='',
                                      null=True,
                                      help_text='information that an error occurred at runtime')
    mark = models.TextField(blank=True,
                            default='',
                            null=True,
                            help_text='mark')
    update_time = models.DateTimeField(auto_now=True)
    create_time = models.DateTimeField(auto_now_add=True)
    delete_time = models.DateTimeField(blank=True,
                                       null=True,
                                       default=None,
                                       help_text='logic delete')

    def delete(self, using=None, keep_parents=False):
        self.delete_time = datetime.now()
        self.save()


class ActionLog(models.Model):
    id = models.UUIDField(primary_key=True,
                          default=uuid.uuid4,
                          editable=False,
                          help_text="self ID")
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    action = models.CharField(max_length=128,
                              blank=True,
                              help_text='action')
    action_type = models.CharField(max_length=128,
                                   blank=True,
                                   help_text='action type')
    action_data = models.TextField(blank=True,
                                   default='',
                                   null=True,
                                   help_text='action data')
    mark = models.TextField(blank=True,
                            default='',
                            null=True,
                            help_text='mark')
    update_time = models.DateTimeField(auto_now=True)
    create_time = models.DateTimeField(auto_now_add=True)
    delete_time = models.DateTimeField(blank=True,
                                       null=True,
                                       default=None,
                                       help_text='logic delete')

    def delete(self, using=None, keep_parents=False):
        self.delete_time = datetime.now()
        self.save()


class ErrorLog(models.Model):
    id = models.UUIDField(primary_key=True,
                          default=uuid.uuid4,
                          editable=False,
                          help_text="self ID")
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    error = models.CharField(max_length=128,
                             blank=True,
                             help_text='error')
    error_type = models.CharField(max_length=128,
                                  blank=True,
                                  help_text='error type')
    error_data = models.TextField(blank=True,
                                  default='',
                                  null=True,
                                  help_text='error data')
    mark = models.TextField(blank=True,
                            default='',
                            null=True,
                            help_text='mark')
    update_time = models.DateTimeField(auto_now=True)
    create_time = models.DateTimeField(auto_now_add=True)
    delete_time = models.DateTimeField(blank=True,
                                       null=True,
                                       default=None,
                                       help_text='logic delete')

    def delete(self, using=None, keep_parents=False):
        self.delete_time = datetime.now()
        self.save()
