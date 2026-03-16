from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from common.api import BaseDetailAPIView, BaseListCreateAPIView
from common.utils import parse_bool
from vendor_product_mapping.models import VendorProductMapping
from vendor_product_mapping.serializers import VendorProductMappingSerializer


class VendorProductMappingListCreateAPIView(BaseListCreateAPIView):
    queryset = VendorProductMapping.objects.select_related('vendor', 'product').order_by('id')
    serializer_class = VendorProductMappingSerializer

    def filter_queryset(self, queryset):
        vendor_id = self.request.query_params.get('vendor_id')
        product_id = self.request.query_params.get('product_id')
        is_active = parse_bool(self.request.query_params.get('is_active'))

        if vendor_id:
            queryset = queryset.filter(vendor_id=vendor_id)
        if product_id:
            queryset = queryset.filter(product_id=product_id)
        if is_active is None:
            queryset = queryset.filter(is_active=True)
        else:
            queryset = queryset.filter(is_active=is_active)
        return queryset

    @swagger_auto_schema(
        operation_summary='List vendor-product mappings',
        manual_parameters=[
            openapi.Parameter('vendor_id', openapi.IN_QUERY, description='Filter by vendor ID.', type=openapi.TYPE_INTEGER),
            openapi.Parameter('product_id', openapi.IN_QUERY, description='Filter by product ID.', type=openapi.TYPE_INTEGER),
            openapi.Parameter('is_active', openapi.IN_QUERY, description='Filter by active flag. Defaults to true.', type=openapi.TYPE_BOOLEAN),
        ],
        responses={200: VendorProductMappingSerializer(many=True)},
    )
    def get(self, request):
        return super().get(request)

    @swagger_auto_schema(
        operation_summary='Create vendor-product mapping',
        request_body=VendorProductMappingSerializer,
        responses={201: VendorProductMappingSerializer, 400: 'Validation error'},
    )
    def post(self, request):
        return super().post(request)


class VendorProductMappingDetailAPIView(BaseDetailAPIView):
    model = VendorProductMapping
    serializer_class = VendorProductMappingSerializer

    @swagger_auto_schema(operation_summary='Retrieve vendor-product mapping', responses={200: VendorProductMappingSerializer, 404: 'Mapping not found'})
    def get(self, request, pk):
        return super().get(request, pk)

    @swagger_auto_schema(operation_summary='Update vendor-product mapping', request_body=VendorProductMappingSerializer, responses={200: VendorProductMappingSerializer, 400: 'Validation error', 404: 'Mapping not found'})
    def put(self, request, pk):
        return super().put(request, pk)

    @swagger_auto_schema(operation_summary='Partially update vendor-product mapping', request_body=VendorProductMappingSerializer, responses={200: VendorProductMappingSerializer, 400: 'Validation error', 404: 'Mapping not found'})
    def patch(self, request, pk):
        return super().patch(request, pk)

    @swagger_auto_schema(operation_summary='Soft delete vendor-product mapping', responses={204: 'Mapping deactivated', 404: 'Mapping not found'})
    def delete(self, request, pk):
        return super().delete(request, pk)
