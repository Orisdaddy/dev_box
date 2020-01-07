from rest_framework.mixins import ListModelMixin
from rest_framework.generics import GenericAPIView
from common.viewset import DataModelViewSet
from common.mixin import ListDestroyModelMixin

from dev_tool.serializers import request_simu as simu
from dev_tool import models
import json


class ReqHistoryList(ListModelMixin, ListDestroyModelMixin, GenericAPIView):
    serializer_class = simu.ReqHistoryListSer

    def get(self, request):
        self.queryset = models.PostManHistory.objects.filter(user_id=request.user.pk)
        return self.list(request)

    def delete(self, request):
        self.queryset = models.PostManHistory.objects.filter(user_id=request.user.pk)
        return self.destroy(request)


class ReqHistory(DataModelViewSet):
    queryset = models.PostManHistory.objects.all()
    serializer_class = simu.ReqHistorySer

    def post(self, request, **kwargs):
        data = request.data
        request.data['headers'] = json.dumps(data['headers'])
        request.data['params'] = json.dumps(data['params'])
        request.data['body'] = json.dumps(data['body'])
        request.data['user'] = request.user.pk
        return self.create(request)

