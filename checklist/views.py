from django.conf import settings
from django.db import transaction
from django.shortcuts import get_object_or_404

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Checklist, Category, Item, CategoryFile, ItemFile, ShareLink
from .serializer import (
    ChecklistSerializer, CategorySerializer, ItemSerializer,
    CategoryFileSerializer, ItemFileSerializer
)


class ChecklistViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing Checklists. Requires authentication.
    Includes a 'clone' action to duplicate a checklist, 
    and a 'share' action to generate a public link for sharing.
    """
    serializer_class = ChecklistSerializer

    def get_queryset(self):
        # Only return checklists that belong to the authenticated user
        if self.request.user.is_authenticated:
            return Checklist.objects.filter(owner=self.request.user).prefetch_related('categories__items')
        return Checklist.objects.none()

    def perform_create(self, serializer):
        # Assign the owner of the checklist to the authenticated user
        if self.request.user.is_authenticated:
            serializer.save(owner=self.request.user)
        else:
            raise PermissionError("You must be authenticated to create a checklist.")

    @action(detail=True, methods=['post'])
    def clone(self, request, pk=None):
        """
        Clone an entire checklist (categories, items, and their files).
        """
        original = self.get_object()
        with transaction.atomic():
            new_checklist = Checklist.objects.create(
                title=request.data.get('title', f"Copy of {original.title}"),
                description=original.description,
                owner=request.user if request.user.is_authenticated else None
            )
            for cat in original.categories.all():
                new_cat = Category.objects.create(checklist=new_checklist, name=cat.name)
                for item in cat.items.all():
                    new_item = Item.objects.create(category=new_cat, name=item.name, is_completed=item.is_completed)
                    for item_file in item.files.all():
                        ItemFile.objects.create(item=new_item, file=item_file.file)
                for cat_file in cat.files.all():
                    CategoryFile.objects.create(category=new_cat, file=cat_file.file)

        serializer = self.get_serializer(new_checklist)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'], permission_classes=[AllowAny])
    def share(self, request, pk=None):
        """
        Generate a shareable link for the checklist.
        """
        ck = self.get_object()
        link = ShareLink.objects.create(checklist=ck)
        front = settings.FRONTEND_URL.rstrip("/")
        return Response({
            "share_url": f"{front}/share/{link.token}/"
        }, status=status.HTTP_201_CREATED)


class CategoryViewSet(viewsets.ModelViewSet):
    """
    CRUD operations for Categories, nested under Checklists.
    """
    serializer_class = CategorySerializer

    def get_queryset(self):
        return Category.objects.all()

    def perform_create(self, serializer):
        checklist = get_object_or_404(Checklist, pk=self.kwargs['checklist_pk'])
        serializer.save(checklist=checklist)


class ItemViewSet(viewsets.ModelViewSet):
    """
    CRUD operations for Items, nested under Categories and Checklists.
    """
    serializer_class = ItemSerializer

    def get_queryset(self):
        return Item.objects.filter(
            category__id=self.kwargs['category_pk'],
            category__checklist__id=self.kwargs['checklist_pk']
        )

    def perform_create(self, serializer):
        category = get_object_or_404(Category, pk=self.kwargs['category_pk'], checklist__id=self.kwargs['checklist_pk'])
        serializer.save(category=category)


class CategoryFileViewSet(viewsets.ModelViewSet):
    """
    File uploads for categories. Allows public upload via shared token.
    """
    serializer_class = CategoryFileSerializer
    parser_classes = [MultiPartParser, FormParser]

    def get_permissions(self):
        if 'token_token' in self.kwargs:
            return [AllowAny()]
        return super().get_permissions()

    def get_queryset(self):
        category_id = self.kwargs['category_pk']
        token = self.kwargs.get('token_token')

        if token:
            share_link = get_object_or_404(ShareLink, token=token)
            return CategoryFile.objects.filter(category__id=category_id, category__checklist=share_link.checklist)
        return CategoryFile.objects.filter(category__id=category_id, category__checklist__owner=self.request.user)

    def perform_create(self, serializer):
        category_id = self.kwargs['category_pk']
        token = self.kwargs.get('token_token')

        if token:
            share_link = get_object_or_404(ShareLink, token=token)
            category = get_object_or_404(Category, id=category_id, checklist=share_link.checklist)
        else:
            category = get_object_or_404(Category, id=category_id, checklist__owner=self.request.user)

        serializer.save(category=category)


class ItemFileViewSet(viewsets.ModelViewSet):
    """
    File uploads for items. Allows public upload via shared token.
    """
    serializer_class = ItemFileSerializer
    parser_classes = [MultiPartParser, FormParser]

    def get_permissions(self):
        if 'token_token' in self.kwargs:
            return [AllowAny()]
        return super().get_permissions()

    def get_queryset(self):
        category_id = self.kwargs['category_pk']
        item_id = self.kwargs['item_pk']
        token = self.kwargs.get('token_token')

        if token:
            share_link = get_object_or_404(ShareLink, token=token)
            return ItemFile.objects.filter(
                item__id=item_id,
                item__category__id=category_id,
                item__category__checklist=share_link.checklist
            )
        return ItemFile.objects.filter(
            item__id=item_id,
            item__category__id=category_id,
            item__category__checklist__owner=self.request.user
        )

    def perform_create(self, serializer):
        category_id = self.kwargs['category_pk']
        item_id = self.kwargs['item_pk']
        token = self.kwargs.get('token_token')

        if token:
            share_link = get_object_or_404(ShareLink, token=token)
            item = get_object_or_404(Item, id=item_id, category__id=category_id, category__checklist=share_link.checklist)
        else:
            item = get_object_or_404(Item, id=item_id, category__id=category_id, category__checklist__owner=self.request.user)

        serializer.save(item=item)


class SharedChecklistViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet to access a shared (read-only) checklist via its token.
    """
    serializer_class = ChecklistSerializer
    permission_classes = [AllowAny]
    lookup_field = 'token'
    lookup_url_kwarg = 'token'

    def get_queryset(self):
        return Checklist.objects.filter(share_links__token=self.kwargs['token'])

    def get_object(self):
        return get_object_or_404(self.get_queryset())
