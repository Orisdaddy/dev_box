from django.urls import path, re_path
from dev_tool.views import request_simu, machine

urlpatterns = [
    re_path("^postman/history_list", request_simu.ReqHistoryList.as_view()),
    re_path("^postman/history/(?P<pk>\\d*)", request_simu.ReqHistory.as_view({
        'get': 'retrieve',
        'delete': 'destroy'
    })),

    re_path("^machine/session_list", machine.MachineSessionList.as_view()),
    re_path("^machine/session/(?P<pk>\\d*)", machine.MachineSession.as_view({
        'get': 'retrieve',
        'delete': 'destroy',
        'put': 'update'
    })),

]
