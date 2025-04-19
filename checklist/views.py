
from rest_framework import viewsets, status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response

from .models import Checklist, Category, Item, CategoryFile, ItemFile
from .serializer import (
    ChecklistSerializer, CategorySerializer, ItemSerializer,
    CategoryFileSerializer, ItemFileSerializer
)
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action
from django.db import transaction

class ChecklistViewSet(viewsets.ModelViewSet):
    queryset = Checklist.objects.all().prefetch_related('categories__items')
    serializer_class = ChecklistSerializer
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