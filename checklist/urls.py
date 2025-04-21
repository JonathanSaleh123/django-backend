# urls.py
from django.urls import path, include
from rest_framework import routers
from rest_framework_nested import routers as nested_routers
from rest_framework.routers      import SimpleRouter
from .views import (
    ChecklistViewSet, CategoryViewSet, ItemViewSet,
    CategoryFileViewSet, ItemFileViewSet, SharedChecklistViewSet
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



# 1) top‑level “share” router
share_router = SimpleRouter()
share_router.register(r'share', SharedChecklistViewSet, basename='shared-checklist')

# 2) /api/share/{token}/categories/
share_cat_router = nested_routers.NestedSimpleRouter(
    share_router, r'share', lookup='token'
)
share_cat_router.register(
    r'categories',
    CategoryViewSet,                   # or a read‑only variant listing them
    basename='shared-categories'
)
share_cat_file_router = nested_routers.NestedSimpleRouter(
    share_cat_router, r'categories', lookup='category'
)
share_cat_file_router.register(r'files', CategoryFileViewSet, basename='shared-category-files')


share_item_router = nested_routers.NestedSimpleRouter(
    share_cat_router, r'categories', lookup='category'
)
share_item_router.register(
    r'items',
    ItemViewSet,                       # or a read‑only variant listing them
    basename='shared-items'
)
share_item_file_router = nested_routers.NestedSimpleRouter(
    share_item_router, r'items', lookup='item'
)
share_item_file_router.register(r'files', ItemFileViewSet, basename='shared-item-files')


urlpatterns = [
    path('api/', include(router.urls)),
    path('api/', include(checklist_router.urls)),
    path('api/', include(category_router.urls)),
    path('api/', include(category_file_router.urls)),
    path('api/', include(item_file_router.urls)),

    path('api/', include(share_router.urls)),
    path('api/', include(share_cat_router.urls)),
    path('api/', include(share_cat_file_router.urls)),
    path('api/', include(share_item_file_router.urls)),


]
