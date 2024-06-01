from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.conf import settings
from django.core.exceptions import PermissionDenied


class Status(models.Model):
    nome = models.CharField(max_length=100)
    data_criacao = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.nome
    
    def get_absolute_url(self):
        return reverse("calendarapp:status-detail", args=(self.id,))

    @property
    def get_html_url(self):
        url = reverse("calendarapp:status-detail", args=(self.id,))
        return f'<a href="{url}"> {self.title} </a>'


class CanalMarket(models.Model):
    nome = models.CharField(max_length=100)
    data_criacao = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.nome
    
    def get_absolute_url(self):
        return reverse("calendarapp:canal-detail", args=(self.id,))

    @property
    def get_html_url(self):
        url = reverse("calendarapp:canal-detail", args=(self.id,))
        return f'<a href="{url}"> {self.title} </a>'


class ClienteStatusLog(models.Model):
    cliente = models.ForeignKey('Cliente', on_delete=models.CASCADE)
    old_status = models.ForeignKey('Status', related_name='old_status', on_delete=models.CASCADE)
    new_status = models.ForeignKey('Status', related_name='new_status', on_delete=models.CASCADE)
    changed_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    change_date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"O status do {self.cliente.nome} mudou de {self.old_status} para {self.new_status} por {self.changed_by}"


class ClienteManager(models.Manager):
    """ Cliente manager """

    def get_all_clients(self, user):
        # clientes = Cliente.objects.filter(user=user, is_active=True, is_deleted=False)
        # return clientes
        if user.is_staff:
            # clientes = Cliente.objects.filter(is_active=True, is_deleted=False)
            clientes = Cliente.objects.all()
        else:
            clientes = Cliente.objects.filter(usuario_designado=user)
        return clientes


class Cliente(models.Model):
    nome = models.CharField(max_length=100)
    codigo = models.CharField(max_length=20, null=True, blank=True, unique=True)
    telefone = models.CharField(max_length=15, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    # whatsapp = models.BooleanField(default=True)
    status = models.ForeignKey(Status, on_delete=models.CASCADE)
    canal_marketing = models.ForeignKey(CanalMarket, on_delete=models.CASCADE)
    usuario_designado = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True, related_name='designated_clients')
    usuario_admin = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True, related_name='admin_clients')
    # data_visita = models.DateTimeField()
    data_criacao = models.DateTimeField(auto_now_add=True)
    
    objects = ClienteManager()
    
    class Meta:
        ordering = ['nome']  # Ordem padrão pelo campo 'nome'

    def __str__(self):
        try:
            return f"{self.nome} - {self.codigo}"
        except:
            return self.nome
    
    def get_absolute_url(self):
        return reverse("calendarapp:client-detail", args=(self.id,))

    @property
    def get_html_url(self):
        url = reverse("calendarapp:client-detail", args=(self.id,))
        return f'<a href="{url}"> {self.title} </a>'
    
    def delete(self, user, *args, **kwargs):
        if not user.is_superuser:
            raise PermissionDenied("Somente Gestor pode deletar esse cliente.")
        super(Cliente, self).delete(*args, **kwargs)
    
    def save(self, *args, user=None, **kwargs):
        # Verificar se o status foi alterado
        if self.pk is not None:
            old_instance = Cliente.objects.get(pk=self.pk)
            if old_instance.status != self.status:
                # Registre a mudança de status no log
                ClienteStatusLog.objects.create(
                    cliente=self,
                    old_status=old_instance.status,
                    new_status=self.status,
                    changed_by=user
                )
        
        super().save(*args, **kwargs)


class ResultadoComunicacao(models.Model):
    nome = models.CharField(max_length=100)
    data_criacao = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.nome