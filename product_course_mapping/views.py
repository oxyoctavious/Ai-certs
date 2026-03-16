from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from common.api import BaseDetailAPIView, BaseListCreateAPIView
from common.utils import parse_bool
from product_course_mapping.models import ProductCourseMapping
from product_course_mapping.serializers import ProductCourseMappingSerializer


class ProductCourseMappingListCreateAPIView(BaseListCreateAPIView):
    queryset = ProductCourseMapping.objects.select_related('product', 'course').order_by('id')
    serializer_class = ProductCourseMappingSerializer

    def filter_queryset(self, queryset):
        product_id = self.request.query_params.get('product_id')
        course_id = self.request.query_params.get('course_id')
        is_active = parse_bool(self.request.query_params.get('is_active'))

        if product_id:
            queryset = queryset.filter(product_id=product_id)
        if course_id:
            queryset = queryset.filter(course_id=course_id)
        if is_active is None:
            queryset = queryset.filter(is_active=True)
        else:
            queryset = queryset.filter(is_active=is_active)
        return queryset

    @swagger_auto_schema(
        operation_summary='List product-course mappings',
        manual_parameters=[
            openapi.Parameter('product_id', openapi.IN_QUERY, description='Filter by product ID.', type=openapi.TYPE_INTEGER),
            openapi.Parameter('course_id', openapi.IN_QUERY, description='Filter by course ID.', type=openapi.TYPE_INTEGER),
            openapi.Parameter('is_active', openapi.IN_QUERY, description='Filter by active flag. Defaults to true.', type=openapi.TYPE_BOOLEAN),
        ],
        responses={200: ProductCourseMappingSerializer(many=True)},
    )
    def get(self, request):
        return super().get(request)

    @swagger_auto_schema(
        operation_summary='Create product-course mapping',
        request_body=ProductCourseMappingSerializer,
        responses={201: ProductCourseMappingSerializer, 400: 'Validation error'},
    )
    def post(self, request):
        return super().post(request)


class ProductCourseMappingDetailAPIView(BaseDetailAPIView):
    model = ProductCourseMapping
    serializer_class = ProductCourseMappingSerializer

    @swagger_auto_schema(operation_summary='Retrieve product-course mapping', responses={200: ProductCourseMappingSerializer, 404: 'Mapping not found'})
    def get(self, request, pk):
        return super().get(request, pk)

    @swagger_auto_schema(operation_summary='Update product-course mapping', request_body=ProductCourseMappingSerializer, responses={200: ProductCourseMappingSerializer, 400: 'Validation error', 404: 'Mapping not found'})
    def put(self, request, pk):
        return super().put(request, pk)

    @swagger_auto_schema(operation_summary='Partially update product-course mapping', request_body=ProductCourseMappingSerializer, responses={200: ProductCourseMappingSerializer, 400: 'Validation error', 404: 'Mapping not found'})
    def patch(self, request, pk):
        return super().patch(request, pk)

    @swagger_auto_schema(operation_summary='Soft delete product-course mapping', responses={204: 'Mapping deactivated', 404: 'Mapping not found'})
    def delete(self, request, pk):
        return super().delete(request, pk)
