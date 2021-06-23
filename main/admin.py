from django.contrib import admin
from .models import User

# Register your models here.
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    search_fields = ['phone_number', 'name']
    list_display = ['id','phone_number', 'name']