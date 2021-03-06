"""djangoWeb URL Configuration

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
from rest_framework_jwt.views import obtain_jwt_token
from rest_framework.documentation import include_docs_urls
from rest_framework_swagger.views import get_swagger_view


urlpatterns = [
    # path('admin/', admin.site.urls),
    path('user/login', obtain_jwt_token),
    path('docs/', include_docs_urls(title='API 文档', permission_classes=[])),
    path('swagger-docs/', get_swagger_view(title='API 文档')),
    # path('api/', include('use_drf.urls')),
    # path('api-auth/', include('rest_framework.urls',namespace='rest_framework')),
    path('cms/', include('apps.cms.urls')),
    path('', include('apps.mtauth.urls'))
]

# 版本控制
api_v1 = [
    path('', include('apps.meituan.urls.v1.urls'))
]

urlpatterns += [
    path('api/v1/', include(api_v1))
]
