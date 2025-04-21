
from rest_framework import serializers
from .models import Checklist, Category, Item, CategoryFile, ItemFile

class CategoryFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoryFile
        fields = ['id', 'file']

class ItemFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemFile
        fields = ['id', 'file']

class ItemSerializer(serializers.ModelSerializer):
    files = ItemFileSerializer(many=True, read_only=True)

    class Meta:
        model = Item
        fields = ['id', 'name', 'is_completed', 'files']

class CategorySerializer(serializers.ModelSerializer):
    items = ItemSerializer(many=True, read_only=True)
    files = CategoryFileSerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = ['id', 'name', 'items', 'files']

class ChecklistSerializer(serializers.ModelSerializer):
    categories = CategorySerializer(many=True, read_only=True)

    class Meta:
        model = Checklist
        fields = ['id', 'title', 'description', 'created_at', 'categories', 'owner']
        read_only_fields = ['owner']