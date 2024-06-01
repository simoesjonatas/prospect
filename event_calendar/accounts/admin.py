from django.contrib import admin
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import AdminPasswordChangeForm

from .models import User

class UserAdmin(BaseUserAdmin):
    # Campos exibidos ao visualizar detalhes do usuário no admin
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
        # ('Important dates', {'fields': ('date_joined',)}),
    )

    # Campos exibidos ao criar um novo usuário no admin
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_active', 'is_staff', 'is_superuser')}
        ),
    )

    # Campos exibidos na lista de usuários no admin
    list_display = ('email', 'is_staff', 'is_superuser', 'is_active', 'date_joined')
    list_filter = ('is_staff', 'is_superuser', 'is_active')
    search_fields = ('email',)
    ordering = ('email',)

    # Adiciona a opção de alterar senha ao editar usuário
    change_password_form = AdminPasswordChangeForm
    change_password = True

# Register your models here.
admin.site.register(User, UserAdmin)