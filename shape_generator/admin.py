from django.contrib import admin

from .models import Shape


@admin.register(Shape)
class ShapeAdmin(admin.ModelAdmin):
    pass
