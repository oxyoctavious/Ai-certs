from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from common.api import BaseDetailAPIView, BaseListCreateAPIView
from common.utils import parse_bool
from vendor.models import Vendor
from vendor.serializers import VendorSerializer


class VendorListCreateAPIView(BaseListCreateAPIView):
    queryset = Vendor.objects.order_by('id')
    serializer_class = VendorSerializer

    def filter_queryset(self, queryset):
        product_id = self.request.query_params.get('product_id')
        is_active = parse_bool(self.request.query_params.get('is_active'))

        if product_id:
            queryset = queryset.filter(vendorproductmapping__product_id=product_id, vendorproductmapping__is_active=True)
        if is_active is None:
            queryset = queryset.filter(is_active=True)
        else:
            queryset = queryset.filter(is_active=is_active)
        return queryset.distinct()

    @swagger_auto_schema(
        operation_summary='List vendors',
        manual_parameters=[
            openapi.Parameter('product_id', openapi.IN_QUERY, description='Filter vendors linked to a product ID.', type=openapi.TYPE_INTEGER),
            openapi.Parameter('is_active', openapi.IN_QUERY, description='Filter by active flag. Defaults to true.', type=openapi.TYPE_BOOLEAN),
        ],
        responses={200: VendorSerializer(many=True)},
    )
    def get(self, request):
        return super().get(request)

    @swagger_auto_schema(
        operation_summary='Create vendor',
        request_body=VendorSerializer,
        responses={201: VendorSerializer, 400: 'Validation error'},
    )
    def post(self, request):
        return super().post(request)


class VendorDetailAPIView(BaseDetailAPIView):
    model = Vendor
    serializer_class = VendorSerializer

    @swagger_auto_schema(operation_summary='Retrieve vendor', responses={200: VendorSerializer, 404: 'Vendor not found'})
    def get(self, request, pk):
        return super().get(request, pk)

    @swagger_auto_schema(operation_summary='Update vendor', request_body=VendorSerializer, responses={200: VendorSerializer, 400: 'Validation error', 404: 'Vendor not found'})
    def put(self, request, pk):
        return super().put(request, pk)

    @swagger_auto_schema(operation_summary='Partially update vendor', request_body=VendorSerializer, responses={200: VendorSerializer, 400: 'Validation error', 404: 'Vendor not found'})
    def patch(self, request, pk):
        return super().patch(request, pk)

    @swagger_auto_schema(operation_summary='Soft delete vendor', responses={204: 'Vendor deactivated', 404: 'Vendor not found'})
    def delete(self, request, pk):
        return super().delete(request, pk)
