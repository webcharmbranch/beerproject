from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import CreateView

from account.forms import LoginUserForm, RegisterUserForm

from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str, DjangoUnicodeDecodeError
from account.utils import generate_token
from django.utils.html import strip_tags
from django.core.mail import EmailMessage, EmailMultiAlternatives, send_mail
from django.conf import settings
from django.contrib import messages, auth
from django.contrib.auth.mixins import LoginRequiredMixin

from carts.models import Cart


# Create your views here.
class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = 'account/login.html'
    extra_context = {'title': 'Авторизация'}
    redirect_authenticated_user = True

    def get_success_url(self):
        redirect_page = self.request.GET.get('next')
        print('SELF_POST_NEXT_FROM_LoginUser_view', redirect_page)
        if redirect_page and redirect_page != reverse('account:logout'):
            return redirect_page
            # return redirect('127.0.0.1:8000'+ redirect_page)
        return reverse_lazy('account:simple')
    def form_valid(self, form):
        session_key = self.request.session.session_key

        # email = self.request.POST['email']
        # password = self.request.POST['password']
        user = form.get_user()

        if user:
            auth.login(self.request, user)
            if session_key:
                # delete old authorized user carts
                forgot_carts = Cart.objects.filter(user=user)
                if forgot_carts.exists():
                    forgot_carts.delete()
                # add new authorized user cart from anonymous session
                Cart.objects.filter(session_key=session_key).update(user=user)

                messages.success(self.request, f"{user.email}, Вы вошли в аккаунт")

                return HttpResponseRedirect(self.get_success_url())

def simple_view(request):
    return render(request, 'account/simple.html')


class RegisterUser(CreateView):
    form_class = RegisterUserForm
    template_name = 'account/register.html'
    extra_context = {'title': 'Регистрация'}
    success_url = reverse_lazy('account:login')

    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect(settings.LOGIN_REDIRECT_URL)
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        sup = super(RegisterUser, self).post(request,*args, **kwargs)
        print('EMAIL_HOST_USER', settings.EMAIL_HOST_USER)
        print('EMAIL_HOST_PASSWORD', settings.EMAIL_HOST_PASSWORD)
        email = request.POST['email']
        user = get_object_or_404(get_user_model(), email=email)
        current_site = get_current_site(request)
        email_subject = 'Activate your account',
        html_message = render_to_string('account/activate.html',
        {
            'user': user,
            'domain': current_site.domain,
            'uid':urlsafe_base64_encode(force_bytes(user.pk)),
            'token': generate_token.make_token(user)
        }
        )

        plain_message = strip_tags(html_message)
        email_message = EmailMultiAlternatives(
            subject='Activate your account',
            body=plain_message,
            from_email=settings.EMAIL_HOST_USER,
            to=[email,],
        )
        email_message.attach_alternative(html_message, "text/html")
        email_message.send(fail_silently=False)
        return render(request, 'account/login.html')

class ActivateAccountView(View):
    def get(self, request, uidb64, token):
        try:
            uid=force_str(urlsafe_base64_decode(uidb64))
            user = get_user_model().objects.get(pk=uid)
        except Exception as error:
            print(error)
            user = None

        if user is not None and generate_token.check_token(user, token):
            user.is_active = True
            user.save()
            messages.add_message(request, messages.INFO, 'account activated successfully')
            return redirect('account:login')
        return render(request, 'account/activation_failed.html', status=401)

# @login_required - нужен был для проверки работы с параметром гет запроса next при переходе на закрытую от анонима страницу
def users_cart(request):
    return render(request, 'account/users_cart.html')