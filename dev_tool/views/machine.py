from django.conf import settings
from rest_framework.mixins import ListModelMixin
from rest_framework.generics import GenericAPIView
from common.viewset import DataModelViewSet
from common.view import ResView

from dev_tool.serializers import machine as mc
from dev_tool import models
import os


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


class CheckFileTimeOut:
    def check_timeout(self):
        pass

    def delete_file(self):
        pass


class UploadFile(ResView, CheckFileTimeOut):

    def post(self, request):
        file = request.FILES.get('file')
        tab = request.data.get('tab')
        path = settings.BASE_DIR + '/dev_tool/upload_buffer/%s/%s' % (tab, file.name)
        if not os.path.exists(settings.BASE_DIR + '/dev_tool/upload_buffer/%s' % tab):
            os.makedirs(settings.BASE_DIR + '/dev_tool/upload_buffer/%s' % tab)
        with open(path, 'wb') as f:
            for chunk in file.chunks():
                f.write(chunk)
        return self.success()


class UploadFolder(ResView, CheckFileTimeOut):

    def post(self, request):
        return self.success()
