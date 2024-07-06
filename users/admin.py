from django.contrib import admin

# Register your models here.
from .models import Address, Profile,User



admin.site.register(Profile)
admin.site.register(Address)
admin.site.register(User)