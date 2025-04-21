from django.urls import path, include
from rest_framework import routers
from rest_framework_nested import routers as nested_routers
from rest_framework.routers import SimpleRouter
from .views import (
    ChecklistViewSet, CategoryViewSet, ItemViewSet,
    CategoryFileViewSet, ItemFileViewSet, SharedChecklistViewSet
)

# ─────────────────────────────────────────────────────────────
# Authenticated Routes
# ─────────────────────────────────────────────────────────────

# /api/checklists/
router = routers.SimpleRouter()
router.register(r'checklists', ChecklistViewSet, basename='checklist')

# /api/checklists/{checklist_pk}/categories/
checklist_router = nested_routers.NestedSimpleRouter(router, r'checklists', lookup='checklist')
checklist_router.register(r'categories', CategoryViewSet, basename='checklist-categories')

# /api/checklists/{checklist_pk}/categories/{category_pk}/items/
category_router = nested_routers.NestedSimpleRouter(checklist_router, r'categories', lookup='category')
category_router.register(r'items', ItemViewSet, basename='category-items')

# /api/checklists/{checklist_pk}/categories/{category_pk}/files/
category_file_router = nested_routers.NestedSimpleRouter(checklist_router, r'categories', lookup='category')
category_file_router.register(r'files', CategoryFileViewSet, basename='category-files')

# /api/checklists/{checklist_pk}/categories/{category_pk}/items/{item_pk}/files/
item_file_router = nested_routers.NestedSimpleRouter(category_router, r'items', lookup='item')
item_file_router.register(r'files', ItemFileViewSet, basename='item-files')

# ───────────────────────────────────────────────────────
# Shared Routes (public access via token)
# ───────────────────────────────────────────────────────

# /api/share/{token}/
share_router = SimpleRouter()
share_router.register(r'share', SharedChecklistViewSet, basename='shared-checklist')

# /api/share/{token}/categories/
share_cat_router = nested_routers.NestedSimpleRouter(share_router, r'share', lookup='token')
share_cat_router.register(r'categories', CategoryViewSet, basename='shared-categories')

# /api/share/{token}/categories/{category_pk}/files/
share_cat_file_router = nested_routers.NestedSimpleRouter(share_cat_router, r'categories', lookup='category')
share_cat_file_router.register(r'files', CategoryFileViewSet, basename='shared-category-files')

# /api/share/{token}/categories/{category_pk}/items/
share_item_router = nested_routers.NestedSimpleRouter(share_cat_router, r'categories', lookup='category')
share_item_router.register(r'items', ItemViewSet, basename='shared-items')

# /api/share/{token}/categories/{category_pk}/items/{item_pk}/files/
share_item_file_router = nested_routers.NestedSimpleRouter(share_item_router, r'items', lookup='item')
share_item_file_router.register(r'files', ItemFileViewSet, basename='shared-item-files')

urlpatterns = [
    # Authenticated checklist routes
    path('api/', include(router.urls)),
    path('api/', include(checklist_router.urls)),
    path('api/', include(category_router.urls)),
    path('api/', include(category_file_router.urls)),
    path('api/', include(item_file_router.urls)),

    # Public shared routes (via token)
    path('api/', include(share_router.urls)),
    path('api/', include(share_cat_router.urls)),
    path('api/', include(share_cat_file_router.urls)),
    path('api/', include(share_item_file_router.urls)),
]
