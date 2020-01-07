from rest_framework.response import Response
from rest_framework.mixins import CreateModelMixin, UpdateModelMixin
from rest_framework import status

from common.view import ResView


class ListDestroyModelMixin:
    def destroy(self, request, *args, **kwargs):
        self.queryset.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance):
        instance.delete()


class CreateMixin(CreateModelMixin, ResView):
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return self.success(data=serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class UpdateMixin(UpdateModelMixin, ResView):
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return self.success(data=serializer.data)
