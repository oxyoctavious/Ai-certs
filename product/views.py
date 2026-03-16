from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from common.api import BaseDetailAPIView, BaseListCreateAPIView
from common.utils import get_object_or_not_found, parse_bool
from product.models import Product
from product.serializers import ProductNestedSerializer, ProductSerializer


class ProductListCreateAPIView(BaseListCreateAPIView):
    queryset = Product.objects.order_by('id')
    serializer_class = ProductSerializer

    def filter_queryset(self, queryset):
        vendor_id = self.request.query_params.get('vendor_id')
        is_active = parse_bool(self.request.query_params.get('is_active'))

        if vendor_id:
            queryset = queryset.filter(vendorproductmapping__vendor_id=vendor_id, vendorproductmapping__is_active=True)
        if is_active is None:
            queryset = queryset.filter(is_active=True)
        else:
            queryset = queryset.filter(is_active=is_active)
        return queryset.distinct()

    @swagger_auto_schema(
        operation_summary='List products',
        manual_parameters=[
            openapi.Parameter('vendor_id', openapi.IN_QUERY, description='Filter products linked to a vendor ID.', type=openapi.TYPE_INTEGER),
            openapi.Parameter('is_active', openapi.IN_QUERY, description='Filter by active flag. Defaults to true.', type=openapi.TYPE_BOOLEAN),
        ],
        responses={200: ProductSerializer(many=True)},
    )
    def get(self, request):
        return super().get(request)

    @swagger_auto_schema(
        operation_summary='Create product',
        request_body=ProductSerializer,
        responses={201: ProductSerializer, 400: 'Validation error'},
    )
    def post(self, request):
        return super().post(request)


class ProductDetailAPIView(BaseDetailAPIView):
    model = Product
    serializer_class = ProductSerializer

    @swagger_auto_schema(operation_summary='Retrieve product', responses={200: ProductSerializer, 404: 'Product not found'})
    def get(self, request, pk):
        return super().get(request, pk)

    @swagger_auto_schema(operation_summary='Update product', request_body=ProductSerializer, responses={200: ProductSerializer, 400: 'Validation error', 404: 'Product not found'})
    def put(self, request, pk):
        return super().put(request, pk)

    @swagger_auto_schema(operation_summary='Partially update product', request_body=ProductSerializer, responses={200: ProductSerializer, 400: 'Validation error', 404: 'Product not found'})
    def patch(self, request, pk):
        return super().patch(request, pk)

    @swagger_auto_schema(operation_summary='Soft delete product', responses={204: 'Product deactivated', 404: 'Product not found'})
    def delete(self, request, pk):
        return super().delete(request, pk)


class ProductNestedAPIView(APIView):
    @swagger_auto_schema(operation_summary='Retrieve product with nested vendor and course mappings', responses={200: ProductNestedSerializer, 404: 'Product not found'})
    def get(self, request, pk):
        product = get_object_or_not_found(Product, pk=pk)
        serializer = ProductNestedSerializer(product)
        return Response(serializer.data, status=status.HTTP_200_OK)
