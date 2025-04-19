"""
URL configuration for checklist project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.urls import include, path

# urlpatterns = [
#     path("polls/", include("polls.urls")),
#     path("admin/", admin.site.urls),
# ]

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ChecklistViewSet, CategoryViewSet, ItemViewSet,
    CategoryFileViewSet, ItemFileViewSet
)

router = DefaultRouter()
router.register(r'checklists', ChecklistViewSet)
router.register(r'checklists/<string:checklist_id>/categories', CategoryViewSet)
# Updated ItemViewSet registration with path converters and basename
router.register(r'checklists/<string:checklist_id>/categories/<string:category_id>/items', ItemViewSet, basename='item')
router.register(r'category-files', CategoryFileViewSet)
router.register(r'item-files', ItemFileViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path("polls/", include("polls.urls")),
    path("admin/", admin.site.urls),
]
