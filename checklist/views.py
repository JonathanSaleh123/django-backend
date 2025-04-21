
from rest_framework import viewsets, status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from django.conf import settings
from .models import Checklist, Category, Item, CategoryFile, ItemFile, ShareLink
from .serializer import (
    ChecklistSerializer, CategorySerializer, ItemSerializer,
    CategoryFileSerializer, ItemFileSerializer
)
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.db import transaction
from rest_framework.permissions import IsAuthenticated
class ChecklistViewSet(viewsets.ModelViewSet):
    # queryset = Checklist.objects.all().prefetch_related('categories__items')

    serializer_class = ChecklistSerializer

    def get_queryset(self):
        """
        Return the queryset of checklists, filtering by the authenticated user if available.
        """
        if self.request.user.is_authenticated:
            return Checklist.objects.filter(owner=self.request.user).prefetch_related('categories__items')
        return Checklist.objects.none()
    
    def perform_create(self, serializer):
        """
        Save the checklist with the authenticated user as the owner.
        """
        if self.request.user.is_authenticated:
            serializer.save(owner=self.request.user)
        else:
            raise PermissionError("You must be authenticated to create a checklist.")


    @action(detail=True, methods=['post'])
    def clone(self, request, pk=None):
        """
        Clone a checklist and its categories and items.
        """
        original = self.get_object()
        with transaction.atomic():
            # Create a new checklist
            new_checklist = Checklist.objects.create(
                title=request.data.get('title', f"Copy of {original.title}"),
                description=original.description
            )
            # Clone categories and items
            for cat in original.categories.all():
                new_cat = Category.objects.create(
                    checklist=new_checklist,
                    name=cat.name
                )
                for item in cat.items.all():
                    new_item = Item.objects.create(
                        category=new_cat,
                        name=item.name,
                        is_completed=item.is_completed
                    )
                    for item_file in item.files.all():
                        ItemFile.objects.create(
                            item=new_item,
                            file=item_file.file
                        )
                # Clone files for categories
                for cat_file in cat.files.all():
                    CategoryFile.objects.create(
                        category=new_cat,
                        file=cat_file.file
                    )


        # 3) return the new checklist representation
        serializer = self.get_serializer(new_checklist)
        return Response(serializer.data, status=201)
    
    @action(detail=True, methods=['post'], permission_classes=[AllowAny])
    def share(self, request, pk=None):
        ck = self.get_object()
        link = ShareLink.objects.create(checklist=ck)
        front = settings.FRONTEND_URL.rstrip("/") 
        return Response({
            "share_url": f"{front}/share/{link.token}/"
        }, status=201)
    


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def perform_create(self, serializer):
        # nested router gives you 'checklist_pk'
        checklist = get_object_or_404(Checklist, pk=self.kwargs['checklist_pk'])
        serializer.save(checklist=checklist)

class ItemViewSet(viewsets.ModelViewSet):
    serializer_class = ItemSerializer

    def get_queryset(self):
        checklist_pk = self.kwargs['checklist_pk']
        category_pk  = self.kwargs['category_pk']
        return Item.objects.filter(
            category__id=category_pk,
            category__checklist__id=checklist_pk
        )

    def perform_create(self, serializer):
        checklist = get_object_or_404(Checklist, pk=self.kwargs['checklist_pk'])
        category  = get_object_or_404(Category,  pk=self.kwargs['category_pk'])
        serializer.save(category=category)


class CategoryFileViewSet(viewsets.ModelViewSet):
    queryset = CategoryFile.objects.all()
    serializer_class = CategoryFileSerializer
    parser_classes = [MultiPartParser, FormParser]

    def perform_create(self, serializer):
        category = get_object_or_404(Category, pk=self.kwargs['category_pk'])
        serializer.save(category=category)

class ItemFileViewSet(viewsets.ModelViewSet):
    queryset = ItemFile.objects.all()
    serializer_class = ItemFileSerializer
    parser_classes = [MultiPartParser, FormParser]

    def perform_create(self, serializer):
        item = get_object_or_404(Item, pk=self.kwargs['item_pk'])
        serializer.save(item=item)



class SharedChecklistViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for accessing shared checklists via a unique token.
    """
    serializer_class = ChecklistSerializer
    permission_classes = [AllowAny]
    lookup_field = 'token'
    lookup_url_kwarg = 'token'

    def get_queryset(self):
        return Checklist.objects.filter(share_links__token=self.kwargs['token'])

    def get_object(self):
        return get_object_or_404(self.get_queryset())
    
class SharedCategoryFileViewSet(CategoryFileViewSet):
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        token       = self.kwargs['token']
        category_id = self.kwargs['category']     # ← use 'category'
        category = get_object_or_404(
            Category,
            id=category_id,
            checklist__share_links__token=token
        )
        serializer.save(category=category)

class SharedItemFileViewSet(ItemFileViewSet):
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        token    = self.kwargs['token']
        item_id  = self.kwargs['item']         
        item = get_object_or_404(
            Item,
            id=item_id,
            category__checklist__share_links__token=token
        )
        serializer.save(item=item)