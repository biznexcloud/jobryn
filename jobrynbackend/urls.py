"""
URL configuration for jobrynbackend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
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
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

urlpatterns = [
    path('', admin.site.urls),
    path('api/v1/account/', include('account.urls')),
    path('api/v1/profiles/', include('profiles.urls')),
    path('api/v1/certifications/', include('certifications.urls')),
    path('api/v1/projects/', include('projects.urls')),
    path('api/v1/experiences/', include('experiences.urls')),
    path('api/v1/educations/', include('educations.urls')),
    path('api/v1/skills/', include('skills.urls')),
    path('api/v1/companies/', include('companies.urls')),
    path('api/v1/jobs/', include('jobs.urls')),
    path('api/v1/applications/', include('applications.urls')),
    path('api/v1/meetings/', include('meetings.urls')),
    path('api/v1/billing/', include('billing.urls')),
    path('api/v1/learning/', include('learning.urls')),
    
    # Swagger
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]
