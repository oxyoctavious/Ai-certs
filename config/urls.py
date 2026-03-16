from django.contrib import admin
from django.urls import include, path, re_path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework.permissions import AllowAny

schema_view = get_schema_view(
    openapi.Info(
        title='Django Intern Assignment API',
        default_version='v1',
        description='Modular vendor, product, course, certification, and mapping APIs built with APIView.',
    ),
    public=True,
    permission_classes=(AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/vendors/', include('vendor.urls')),
    path('api/products/', include('product.urls')),
    path('api/courses/', include('course.urls')),
    path('api/certifications/', include('certification.urls')),
    path('api/vendor-product-mappings/', include('vendor_product_mapping.urls')),
    path('api/product-course-mappings/', include('product_course_mapping.urls')),
    path('api/course-certification-mappings/', include('course_certification_mapping.urls')),
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
