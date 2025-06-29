from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from account.models import User

# Register your models here.
class UserAdmin(BaseUserAdmin):
    model = User
    list_display = ['id','email', 'name', 'is_active', 'is_admin']
    list_filter = ['is_active', 'is_admin']
    search_fields = ['email', 'name']
    ordering = ['email']
    filter_horizontal = ()
    
    # Define fieldsets for add and change forms
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('name',)}),
        ('Permissions', {'fields': ('is_active', 'is_admin')}),
    )
    
    # Define fieldsets for add user form
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'name', 'password1', 'password2', 'is_active', 'is_admin'),
        }),
    )


admin.site.register(User, UserAdmin)
 