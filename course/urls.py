from django.urls import path

from course.views import CourseDetailAPIView, CourseListCreateAPIView, CourseNestedAPIView

urlpatterns = [
    path('', CourseListCreateAPIView.as_view(), name='course-list-create'),
    path('<int:pk>/nested/', CourseNestedAPIView.as_view(), name='course-nested'),
    path('<int:pk>/', CourseDetailAPIView.as_view(), name='course-detail'),
]
