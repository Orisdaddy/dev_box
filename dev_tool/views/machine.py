from rest_framework.mixins import ListModelMixin
from rest_framework.generics import GenericAPIView
from common.viewset import DataModelViewSet

from dev_tool.serializers import machine as mc
from dev_tool import models


class MachineSession(DataModelViewSet):
    queryset = models.Services.objects.all()
    serializer_class = mc.MachineSessionSer

    def post(self, request, **kwargs):
        request.data['user'] = request.user.pk
        return self.create(request)


class MachineSessionList(ListModelMixin, GenericAPIView):
    serializer_class = mc.MachineSessionListSer

    def get(self, request):
        self.queryset = models.Services.objects.filter(user_id=request.user.pk)
        return self.list(request)



