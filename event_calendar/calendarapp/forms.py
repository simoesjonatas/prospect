from django.forms import ModelForm, DateInput
from calendarapp.models import Event, EventMember, Cliente, Status, CanalMarket
from django_select2.forms import ModelSelect2Widget
from django import forms
from django.conf import settings


class EventForm(ModelForm):
    class Meta:
        model = Event
        fields = ["cliente", "title", "description", "start_time", "end_time"]
        # datetime-local is a HTML5 input type
        widgets = {
            # select search in django
            # pip install django-select2
            # importar 'django_select2', no settings 
            # add as rotas do select2 
            # path('select2/', include('django_select2.urls')),
            "cliente": ModelSelect2Widget(
                model=Cliente,
                search_fields=['nome__icontains', 'codigo__icontains'],
                attrs={'class': 'form-control', 'style': 'width: 100%;'}# Ajuste o campo de busca conforme necessário
            ),
            "title": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Enter event title"}
            ),
            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter event description",
                }
            ),
            "start_time": DateInput(
                attrs={"type": "datetime-local", "class": "form-control"},
                format="%Y-%m-%dT%H:%M",
            ),
            "end_time": DateInput(
                attrs={"type": "datetime-local", "class": "form-control"},
                format="%Y-%m-%dT%H:%M",
            ),
        }
        exclude = ["user"]

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # Obtém o usuário do kwargs
        # print(user)
        super(EventForm, self).__init__(*args, **kwargs)
        # input_formats to parse HTML5 datetime-local input to datetime field
        self.fields["start_time"].input_formats = ("%Y-%m-%dT%H:%M",)
        self.fields["end_time"].input_formats = ("%Y-%m-%dT%H:%M",)
        if user and not user.is_staff:
            self.fields['cliente'].queryset = Cliente.objects.filter(usuario_designado=user)
    # def __init__(self, cliente=None, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     if cliente:
    #         self.fields['cliente'].widget.attrs['readonly'] = True
    #         self.fields['cliente'].initial = cliente.nome
    #         self.fields['cliente_id'] = forms.IntegerField(widget=forms.HiddenInput(), initial=cliente.id)



class AddMemberForm(forms.ModelForm):
    class Meta:
        model = EventMember
        fields = ["user"]


class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        exclude = ['usuario_admin']
        widgets = {
            "usuario_designado": ModelSelect2Widget(
                model=settings.AUTH_USER_MODEL,
                search_fields=['email__icontains'],
                attrs={'class': 'form-control', 'style': 'width: 100%;'}# Ajuste o campo de busca conforme necessário
            ),
        }
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(ClienteForm, self).__init__(*args, **kwargs)
        # If the user is not staff, make the usuario_designado field read-only
        if self.user and not self.user.is_staff:
            self.fields['usuario_designado'].disabled = True


class StatusForm(forms.ModelForm):
    class Meta:
        model = Status
        fields = '__all__'


class CanalForm(forms.ModelForm):
    class Meta:
        model = CanalMarket
        fields = '__all__'