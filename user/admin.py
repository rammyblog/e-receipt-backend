from django.contrib import admin

from django.contrib.auth.admin import UserAdmin

from .models import  User

# UserAdmin.list_display += ('is_admin', 'is_buyer', 'is_supplier',)  # don't forget the commas
# UserAdmin.list_filter += ('is_admin', 'is_buyer', 'is_supplier',)
UserAdmin.fieldsets += (('Seller', {'fields': ('phone_number', 'logo', 'address',)}),)

admin.site.register(User, UserAdmin)
