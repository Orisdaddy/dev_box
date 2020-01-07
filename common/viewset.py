from rest_framework.viewsets import ModelViewSet
from common.mixin import CreateMixin, UpdateMixin
from common.view import DataViews


class DataModelViewSet(DataViews, CreateMixin, UpdateMixin, ModelViewSet):
    pass
