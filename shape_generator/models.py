from django.db import models


class Shape(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    modified_at = models.DateTimeField(auto_now=True, blank=True, null=True)
    coords = models.CharField(max_length=200)