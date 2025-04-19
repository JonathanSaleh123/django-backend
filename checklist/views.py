
from rest_framework import viewsets, status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response

from .models import Checklist, Category, Item, CategoryFile, ItemFile
from .serializer import (
    ChecklistSerializer, CategorySerializer, ItemSerializer,
    CategoryFileSerializer, ItemFileSerializer
)

class ChecklistViewSet(viewsets.ModelViewSet):
    queryset = Checklist.objects.all().prefetch_related('categories__items')
    serializer_class = ChecklistSerializer

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    def perform_create(self, serializer):
        checklist = Checklist.objects.get(id=self.kwargs['checklist_id'])
        serializer.save(checklist=checklist)

class ItemViewSet(viewsets.ModelViewSet):
    serializer_class = ItemSerializer

    def get_queryset(self):
        checklist_id = self.kwargs['checklist_id']
        category_id = self.kwargs['category_id']
        return Item.objects.filter(category__id=category_id, category__checklist__id=checklist_id)

    def perform_create(self, serializer):
        checklist = Checklist.objects.get(id=self.kwargs['checklist_id'])
        category = Category.objects.get(id=self.kwargs['category_id'])
        serializer.save(checklist=checklist, category=category)


class CategoryFileViewSet(viewsets.ModelViewSet):
    queryset = CategoryFile.objects.all()
    serializer_class = CategoryFileSerializer
    parser_classes = [MultiPartParser, FormParser]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class ItemFileViewSet(viewsets.ModelViewSet):
    queryset = ItemFile.objects.all()
    serializer_class = ItemFileSerializer
    parser_classes = [MultiPartParser, FormParser]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
