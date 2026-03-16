from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from common.utils import get_object_or_not_found


class BaseListCreateAPIView(APIView):
    queryset = None
    serializer_class = None

    def get_queryset(self):
        return self.queryset.all()

    def filter_queryset(self, queryset):
        return queryset

    def get_serializer(self, *args, **kwargs):
        return self.serializer_class(*args, **kwargs)

    def get(self, request):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class BaseDetailAPIView(APIView):
    model = None
    serializer_class = None

    def get_object(self, pk):
        return get_object_or_not_found(self.model, pk=pk)

    def get_serializer(self, *args, **kwargs):
        return self.serializer_class(*args, **kwargs)

    def get(self, request, pk):
        instance = self.get_object(pk)
        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        instance = self.get_object(pk)
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, pk):
        instance = self.get_object(pk)
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, pk):
        instance = self.get_object(pk)
        instance.is_active = False
        instance.save(update_fields=['is_active', 'updated_at'])
        return Response(status=status.HTTP_204_NO_CONTENT)
