"""xym URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.conf.urls import url
from django.conf import settings
from rest_framework_swagger.views import get_swagger_view

urlpatterns = [
    path('admin/', admin.site.urls),
    url('^api/people/', include('grade.urls'), ),
    url('^api/users/', include('users.urls'), ),
    url('^api/auth/', include('flytrap.auth.account.token.urls')),
    url('^api/comments/', include('flytrap.comments.urls')),

    url('^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]

if getattr(settings, 'SHOW_DOCS', False):
    urlpatterns.append(url('^docs', get_swagger_view('形意门接口文档'), ))
