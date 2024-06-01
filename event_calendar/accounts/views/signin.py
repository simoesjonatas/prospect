from django.views.generic import View
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from axes.models import AccessAttempt
from accounts.forms import SignInForm
from django.conf import settings
from django.http import HttpResponseForbidden

max_attempts = settings.AXES_FAILURE_LIMIT


class SignInView(View):
    """ User registration view """

    template_name = "accounts/signin.html"
    form_class = SignInForm

    def get(self, request, *args, **kwargs):
        forms = self.form_class()
        context = {"form": forms}
        return render(request, self.template_name, context)
    
    def post(self, request, *args, **kwargs):
        context = {}
        forms = self.form_class(request.POST)
        remaining_attempts = max_attempts  # Define o número máximo de tentativas aqui
        if forms.is_valid():
            email = forms.cleaned_data["email"]
            password = forms.cleaned_data["password"]
            user = authenticate(request=request, username=email, password=password)
            if user:
                login(request, user)
                # Se o login for bem-sucedido, resete as tentativas restantes
                remaining_attempts = max_attempts
                return redirect("calendarapp:calendar")
            else:
                # Se o login falhar, decrementa as tentativas restantes
                try:
                    ip_address = self.request.META.get('REMOTE_ADDR')
                    user_agent = self.request.META.get('HTTP_USER_AGENT', '')
                    # Filtrar tentativas de login malsucedidas para o usuário e endereço IP especificados
                    user_attempts = AccessAttempt.objects.filter(username=email,ip_address=ip_address, user_agent=user_agent).order_by('-failures_since_start').first()
                    if user_attempts:
                        # max_attempts = 5  # Defina o número máximo de tentativas aqui
                        remaining_attempts = max_attempts - user_attempts.failures_since_start
                        # print("remaining_attempts")
                        # print(remaining_attempts)
                        if remaining_attempts > 0:
                            context['remaining_attempts'] = remaining_attempts
                        else:
                            # Se as tentativas esgotarem, retorna uma resposta de proibido
                            return HttpResponseForbidden("Você excedeu o número máximo de tentativas de login.")
                except AccessAttempt.DoesNotExist:
                    pass

        # # Atualiza a sessão com o número de tentativas restantes
        # request.session['remaining_attempts'] = remaining_attempts

        context = {"form": forms, "remaining_attempts": remaining_attempts}
        return render(request, self.template_name, context)

    # def post(self, request, *args, **kwargs):
    #     forms = self.form_class(request.POST)
    #     if forms.is_valid():
    #         email = forms.cleaned_data["email"]
    #         password = forms.cleaned_data["password"]
    #         user = authenticate(request=request, email=email, password=password)
    #         if user:
    #             login(request, user)
    #             return redirect("calendarapp:calendar")
    #     context = {"form": forms}
    #     return render(request, self.template_name, context)