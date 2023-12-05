
from django.urls import path
from . import views
from . import api_auth
from . import api_user
from . import api_node
from . import api_app
from . import api_error_log
from . import api_action_log

urlpatterns = [
    path("hello", views.hello),
    
    path("auth/token", api_auth.token),
    path("auth/login", api_auth.login),
    
    path("user/login", api_user.login),
    path("user/info", api_user.get_info),
    
    path("node/get", api_node.get),
    path("node/add", api_node.add),
    path("node/delete", api_node.delete),
    
    path("app/add",api_app.add),
    path("app/get",api_app.get),
    path("app/delete",api_app.delete),
    path("app/update/name",api_app.update_name),
    path("app/update/mark",api_app.update_mark),
    path("app/update/runconfig/upload",api_app.update_runconfig_upload),
    path("app/update/runconfig/delete",api_app.update_runconfig_delete),
    path("app/update/planstart",api_app.update_planstart),
    path("app/update/start",api_app.update_start),
    path("app/update/abort",api_app.update_abort),
    path("app/download/result",api_app.download_result),
    
    path("errorlog/get",api_error_log.get),
    
    path("actionlog/get",api_action_log.get),
]

# urlpatterns=[]

