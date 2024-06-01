from django.contrib import admin
from calendarapp import models
from django import forms


@admin.register(models.Event)
class EventAdmin(admin.ModelAdmin):
    model = models.Event
    list_display = [
        "id",
        "title",
        "cliente",
        "user",
        "is_active",
        "is_deleted",
        "created_at",
        "updated_at",
    ]
    list_filter = ["is_active", "is_deleted"]
    search_fields = ["title"]


@admin.register(models.EventMember)
class EventMemberAdmin(admin.ModelAdmin):
    model = models.EventMember
    list_display = ["id", "event", "user", "created_at", "updated_at"]
    list_filter = ["event"]

admin.site.register(models.Status)
admin.site.register(models.CanalMarket)

class ClienteAdminForm(forms.ModelForm):
    class Meta:
        model = models.Cliente
        exclude = ['usuario_admin']

class ClienteAdmin(admin.ModelAdmin):
    form = ClienteAdminForm
    list_display = ['nome', 'codigo', 'telefone', 'email', 'status', 'canal_marketing', 'usuario_designado', 'usuario_admin', 'data_criacao']
    search_fields = ['nome', 'codigo', 'email']
    list_filter = ['status', 'canal_marketing']
    ordering = ['nome']

admin.site.register(models.Cliente, ClienteAdmin)
admin.site.register(models.ClienteStatusLog)
