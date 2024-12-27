from django.contrib import admin

# Register your models here.

from .models import  Category
from .models import  Products



class CategoryAdmin(admin.ModelAdmin):
    list_display=('name','image','description')


admin.site.register(Category,CategoryAdmin)
admin.site.register(Products)

