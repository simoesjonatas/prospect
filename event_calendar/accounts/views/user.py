# from django.contrib.auth.models import User
from accounts.models import User
from django.views.generic import ListView
from accounts.forms import UserCreationForm
from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.urls import reverse
from accounts.decorators import staff_required
from django.utils.decorators import method_decorator
from accounts.utils import generate_random_password


@method_decorator(login_required, name='dispatch')
@method_decorator(staff_required, name='dispatch')
class UserListView(ListView):
    model = User
    template_name = 'accounts/user_list.html'  
    context_object_name = 'users'  # Nome da variável de contexto no template
    
    def get_queryset(self):
        return User.objects.all()

@login_required(login_url="accounts:signin")
@staff_required
def user_create(request):
    initial_email = request.POST.get('email') if request.method == 'POST' else ''
    if request.method == 'POST':
        form = UserCreationForm(request.POST, initial={'email': initial_email})
        if form.is_valid():
            form.save()
            # Após o cadastro, redirecione o administrador de volta à lista de usuários ou a qualquer outra página desejada
            return redirect('accounts:user-list')  # Altere 'accounts:user_list' para a URL da lista de usuários
    else:
        form = UserCreationForm(initial={'email': initial_email})
    return render(request, 'accounts/user_create.html', {'form': form})


@login_required(login_url="accounts:signin")
@staff_required
def user_details(request, user_id):
    event = User.objects.get(id=user_id)
    context = {"event": event}
    return render(request, "accounts/user-details.html", context)


@login_required(login_url="accounts:signin")
@staff_required
def reset_user_password(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user.set_password('troque_sua_senha_op')
    new_password = generate_random_password()
    user.set_password(new_password)
    user.save()
    context = {"senha_reset": new_password}
    return render(request,'accounts/password_change_done_reset.html', context)