from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from certification.models import Certification
from certification.serializers import CertificationNestedSerializer, CertificationSerializer
from common.api import BaseDetailAPIView, BaseListCreateAPIView
from common.utils import get_object_or_not_found, parse_bool


class CertificationListCreateAPIView(BaseListCreateAPIView):
    queryset = Certification.objects.order_by('id')
    serializer_class = CertificationSerializer

    def filter_queryset(self, queryset):
        course_id = self.request.query_params.get('course_id')
        is_active = parse_bool(self.request.query_params.get('is_active'))

        if course_id:
            queryset = queryset.filter(coursecertificationmapping__course_id=course_id, coursecertificationmapping__is_active=True)
        if is_active is None:
            queryset = queryset.filter(is_active=True)
        else:
            queryset = queryset.filter(is_active=is_active)
        return queryset.distinct()

    @swagger_auto_schema(
        operation_summary='List certifications',
        manual_parameters=[
            openapi.Parameter('course_id', openapi.IN_QUERY, description='Filter certifications linked to a course ID.', type=openapi.TYPE_INTEGER),
            openapi.Parameter('is_active', openapi.IN_QUERY, description='Filter by active flag. Defaults to true.', type=openapi.TYPE_BOOLEAN),
        ],
        responses={200: CertificationSerializer(many=True)},
    )
    def get(self, request):
        return super().get(request)

    @swagger_auto_schema(
        operation_summary='Create certification',
        request_body=CertificationSerializer,
        responses={201: CertificationSerializer, 400: 'Validation error'},
    )
    def post(self, request):
        return super().post(request)


class CertificationDetailAPIView(BaseDetailAPIView):
    model = Certification
    serializer_class = CertificationSerializer

    @swagger_auto_schema(operation_summary='Retrieve certification', responses={200: CertificationSerializer, 404: 'Certification not found'})
    def get(self, request, pk):
        return super().get(request, pk)

    @swagger_auto_schema(operation_summary='Update certification', request_body=CertificationSerializer, responses={200: CertificationSerializer, 400: 'Validation error', 404: 'Certification not found'})
    def put(self, request, pk):
        return super().put(request, pk)

    @swagger_auto_schema(operation_summary='Partially update certification', request_body=CertificationSerializer, responses={200: CertificationSerializer, 400: 'Validation error', 404: 'Certification not found'})
    def patch(self, request, pk):
        return super().patch(request, pk)

    @swagger_auto_schema(operation_summary='Soft delete certification', responses={204: 'Certification deactivated', 404: 'Certification not found'})
    def delete(self, request, pk):
        return super().delete(request, pk)


class CertificationNestedAPIView(APIView):
    @swagger_auto_schema(operation_summary='Retrieve certification with nested course mappings', responses={200: CertificationNestedSerializer, 404: 'Certification not found'})
    def get(self, request, pk):
        certification = get_object_or_not_found(Certification, pk=pk)
        serializer = CertificationNestedSerializer(certification)
        return Response(serializer.data, status=status.HTTP_200_OK)
