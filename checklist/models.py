from django.db import models


class Checklist(models.Model):
    """
    Checklist model representing a collection of categories.
    Contains a title, description, and creation timestamp.
    """
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.title

class Category(models.Model):
    """
    Category model representing a group of items within a checklist.
    Each category is linked to a checklist and has a name.
    """
    checklist = models.ForeignKey(Checklist, related_name="categories", on_delete=models.CASCADE)
    name = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.checklist.title} - {self.name}"

class Item(models.Model):
    """
    Item model representing a task or checklist item within a category.
    Each item is linked to a category and has a name and completion status.
    """
    category = models.ForeignKey(Category, related_name="items", on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    is_completed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.category.name} - {self.name}"

class CategoryFile(models.Model):
    category = models.ForeignKey(Category, related_name="files", on_delete=models.CASCADE)
    file = models.FileField(upload_to="category_files/")

class ItemFile(models.Model):
    item = models.ForeignKey(Item, related_name="files", on_delete=models.CASCADE)
    file = models.FileField(upload_to="item_files/")