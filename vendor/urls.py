from django.urls import path

from vendor.views import VendorDetailAPIView, VendorListCreateAPIView, VendorNestedAPIView

urlpatterns = [
    path('', VendorListCreateAPIView.as_view(), name='vendor-list-create'),
    path('<int:pk>/nested/', VendorNestedAPIView.as_view(), name='vendor-nested'),
    path('<int:pk>/', VendorDetailAPIView.as_view(), name='vendor-detail'),
]
