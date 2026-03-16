from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from common.api import BaseDetailAPIView, BaseListCreateAPIView
from common.utils import parse_bool
from course_certification_mapping.models import CourseCertificationMapping
from course_certification_mapping.serializers import CourseCertificationMappingSerializer


class CourseCertificationMappingListCreateAPIView(BaseListCreateAPIView):
    queryset = CourseCertificationMapping.objects.select_related('course', 'certification').order_by('id')
    serializer_class = CourseCertificationMappingSerializer

    def filter_queryset(self, queryset):
        course_id = self.request.query_params.get('course_id')
        certification_id = self.request.query_params.get('certification_id')
        is_active = parse_bool(self.request.query_params.get('is_active'))

        if course_id:
            queryset = queryset.filter(course_id=course_id)
        if certification_id:
            queryset = queryset.filter(certification_id=certification_id)
        if is_active is None:
            queryset = queryset.filter(is_active=True)
        else:
            queryset = queryset.filter(is_active=is_active)
        return queryset

    @swagger_auto_schema(
        operation_summary='List course-certification mappings',
        manual_parameters=[
            openapi.Parameter('course_id', openapi.IN_QUERY, description='Filter by course ID.', type=openapi.TYPE_INTEGER),
            openapi.Parameter('certification_id', openapi.IN_QUERY, description='Filter by certification ID.', type=openapi.TYPE_INTEGER),
            openapi.Parameter('is_active', openapi.IN_QUERY, description='Filter by active flag. Defaults to true.', type=openapi.TYPE_BOOLEAN),
        ],
        responses={200: CourseCertificationMappingSerializer(many=True)},
    )
    def get(self, request):
        return super().get(request)

    @swagger_auto_schema(
        operation_summary='Create course-certification mapping',
        request_body=CourseCertificationMappingSerializer,
        responses={201: CourseCertificationMappingSerializer, 400: 'Validation error'},
    )
    def post(self, request):
        return super().post(request)


class CourseCertificationMappingDetailAPIView(BaseDetailAPIView):
    model = CourseCertificationMapping
    serializer_class = CourseCertificationMappingSerializer

    @swagger_auto_schema(operation_summary='Retrieve course-certification mapping', responses={200: CourseCertificationMappingSerializer, 404: 'Mapping not found'})
    def get(self, request, pk):
        return super().get(request, pk)

    @swagger_auto_schema(operation_summary='Update course-certification mapping', request_body=CourseCertificationMappingSerializer, responses={200: CourseCertificationMappingSerializer, 400: 'Validation error', 404: 'Mapping not found'})
    def put(self, request, pk):
        return super().put(request, pk)

    @swagger_auto_schema(operation_summary='Partially update course-certification mapping', request_body=CourseCertificationMappingSerializer, responses={200: CourseCertificationMappingSerializer, 400: 'Validation error', 404: 'Mapping not found'})
    def patch(self, request, pk):
        return super().patch(request, pk)

    @swagger_auto_schema(operation_summary='Soft delete course-certification mapping', responses={204: 'Mapping deactivated', 404: 'Mapping not found'})
    def delete(self, request, pk):
        return super().delete(request, pk)
