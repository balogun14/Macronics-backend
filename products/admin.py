from django.contrib import admin

# Register your models here.
from .models import  *

admin.site.register(Products)
admin.site.register(Vendor)
admin.site.register(Category)
admin.site.register(Brand)
