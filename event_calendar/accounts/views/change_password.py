from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from accounts.forms import UserUpdateForm, PasswordChangeCustomForm
from django.contrib.auth.views import PasswordChangeView, PasswordChangeDoneView
from django.urls import reverse_lazy
from django.contrib import messages


@login_required(login_url="accounts:signin")
def update_user(request):
    user = request.user
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('calendar')
    else:
        form = UserUpdateForm(instance=user)
    return render(request, 'accounts/update_user.html', {'form': form})


class PasswordChangeCustomView(PasswordChangeView):
    form_class = PasswordChangeCustomForm
    template_name = 'accounts/password_change.html'
    success_url = reverse_lazy('accounts:password_change_done')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['messages'] = messages.get_messages(self.request)
        return context

class PasswordChangeCustomDoneView(PasswordChangeDoneView):
    template_name = 'accounts/password_change_done.html'