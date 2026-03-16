from django.urls import path

from certification.views import CertificationDetailAPIView, CertificationListCreateAPIView, CertificationNestedAPIView

urlpatterns = [
    path('', CertificationListCreateAPIView.as_view(), name='certification-list-create'),
    path('<int:pk>/nested/', CertificationNestedAPIView.as_view(), name='certification-nested'),
    path('<int:pk>/', CertificationDetailAPIView.as_view(), name='certification-detail'),
]
