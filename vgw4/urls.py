"""vgw4 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
admin.autodiscover()
admin.site.enable_nav_sidebar = False


urlpatterns = [
    path('security/', include('security.urls')),
    path('',  include('home.urls')),
    path('admin/', admin.site.urls),
    path('utilities/', include('utilities.urls')),
    path('member/', include('member.urls')),
    path('hr/', include('hr.urls')),
    path('inquiry/', include('inquiry.urls')),

    path('re-member/', include('re_member.urls')),
    path('re-group/', include('re_group.urls')),
    path('re-auth/', include('re_auth.urls')),
    path('re-todo/', include('re_todo.urls')),
    path('re-working/', include('re_working.urls')),
    path('re-working-admin/', include('re_working_admin.urls')),
]
