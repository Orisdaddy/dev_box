from rest_framework import serializers
from dev_tool.models import RequestHistory


class ReqHistorySer(serializers.ModelSerializer):
    class Meta:
        model = RequestHistory
        exclude = ('date_time',)


class ReqHistoryListSer(serializers.Serializer):
    id = serializers.IntegerField()
    host = serializers.CharField()
    method = serializers.CharField()
    date_time = serializers.DateTimeField()
