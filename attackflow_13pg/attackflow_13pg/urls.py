"""
URL configuration for attackflow_13pg project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from attackflow_app import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('admin_page/', views.admin_page, name='admin_page'),
    path('get_users/', views.get_users, name='get_users'),
    path('get_files/', views.get_files, name='get_files'),
    path('update_role/', views.update_role, name='update_role'),
    path('upload/', views.upload_and_annotate, name='upload'),
    path('validate_with_attack_flow/', views.validate_with_attack_flow, name='validate_with_attack_flow'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)