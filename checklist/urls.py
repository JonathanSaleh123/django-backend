# urls.py
from django.urls import path, include
from rest_framework import routers
from rest_framework_nested import routers as nested_routers

from .views import (
    ChecklistViewSet, CategoryViewSet, ItemViewSet,
    CategoryFileViewSet, ItemFileViewSet
)

# 1) top‑level checklist router
router = routers.SimpleRouter()
router.register(r'checklists', ChecklistViewSet, basename='checklist')

# 2) /api/checklists/{checklist_pk}/categories/
checklist_router = nested_routers.NestedSimpleRouter(router, r'checklists', lookup='checklist')
checklist_router.register(r'categories', CategoryViewSet, basename='checklist-categories')

# 3) /api/checklists/{checklist_pk}/categories/{category_pk}/items/
category_router = nested_routers.NestedSimpleRouter(checklist_router, r'categories', lookup='category')
category_router.register(r'items', ItemViewSet, basename='category-items')

# — 4) /api/checklists/{checklist_pk}/categories/{category_pk}/files/
category_file_router = nested_routers.NestedSimpleRouter(checklist_router, r'categories', lookup='category')
category_file_router.register(r'files', CategoryFileViewSet, basename='category-files')

# — 5) /api/checklists/{checklist_pk}/categories/{category_pk}/items/{item_pk}/files/
item_file_router = nested_routers.NestedSimpleRouter(category_router, r'items', lookup='item')
item_file_router.register(r'files', ItemFileViewSet, basename='item-files')

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/', include(checklist_router.urls)),
    path('api/', include(category_router.urls)),
    path('api/', include(category_file_router.urls)),
    path('api/', include(item_file_router.urls)),
]
