from django.urls import path

from product.views import ProductDetailAPIView, ProductListCreateAPIView, ProductNestedAPIView

urlpatterns = [
    path('', ProductListCreateAPIView.as_view(), name='product-list-create'),
    path('<int:pk>/nested/', ProductNestedAPIView.as_view(), name='product-nested'),
    path('<int:pk>/', ProductDetailAPIView.as_view(), name='product-detail'),
]
