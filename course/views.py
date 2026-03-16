from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from common.api import BaseDetailAPIView, BaseListCreateAPIView
from common.utils import get_object_or_not_found, parse_bool
from course.models import Course
from course.serializers import CourseNestedSerializer, CourseSerializer


class CourseListCreateAPIView(BaseListCreateAPIView):
    queryset = Course.objects.order_by('id')
    serializer_class = CourseSerializer

    def filter_queryset(self, queryset):
        product_id = self.request.query_params.get('product_id')
        is_active = parse_bool(self.request.query_params.get('is_active'))

        if product_id:
            queryset = queryset.filter(productcoursemapping__product_id=product_id, productcoursemapping__is_active=True)
        if is_active is None:
            queryset = queryset.filter(is_active=True)
        else:
            queryset = queryset.filter(is_active=is_active)
        return queryset.distinct()

    @swagger_auto_schema(
        operation_summary='List courses',
        manual_parameters=[
            openapi.Parameter('product_id', openapi.IN_QUERY, description='Filter courses linked to a product ID.', type=openapi.TYPE_INTEGER),
            openapi.Parameter('is_active', openapi.IN_QUERY, description='Filter by active flag. Defaults to true.', type=openapi.TYPE_BOOLEAN),
        ],
        responses={200: CourseSerializer(many=True)},
    )
    def get(self, request):
        return super().get(request)

    @swagger_auto_schema(
        operation_summary='Create course',
        request_body=CourseSerializer,
        responses={201: CourseSerializer, 400: 'Validation error'},
    )
    def post(self, request):
        return super().post(request)


class CourseDetailAPIView(BaseDetailAPIView):
    model = Course
    serializer_class = CourseSerializer

    @swagger_auto_schema(operation_summary='Retrieve course', responses={200: CourseSerializer, 404: 'Course not found'})
    def get(self, request, pk):
        return super().get(request, pk)

    @swagger_auto_schema(operation_summary='Update course', request_body=CourseSerializer, responses={200: CourseSerializer, 400: 'Validation error', 404: 'Course not found'})
    def put(self, request, pk):
        return super().put(request, pk)

    @swagger_auto_schema(operation_summary='Partially update course', request_body=CourseSerializer, responses={200: CourseSerializer, 400: 'Validation error', 404: 'Course not found'})
    def patch(self, request, pk):
        return super().patch(request, pk)

    @swagger_auto_schema(operation_summary='Soft delete course', responses={204: 'Course deactivated', 404: 'Course not found'})
    def delete(self, request, pk):
        return super().delete(request, pk)


class CourseNestedAPIView(APIView):
    @swagger_auto_schema(operation_summary='Retrieve course with nested product and certification mappings', responses={200: CourseNestedSerializer, 404: 'Course not found'})
    def get(self, request, pk):
        course = get_object_or_not_found(Course, pk=pk)
        serializer = CourseNestedSerializer(course)
        return Response(serializer.data, status=status.HTTP_200_OK)
