from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('generator/', include('generator.urls')),
    path('admin/', admin.site.urls),
]