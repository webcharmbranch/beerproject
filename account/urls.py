from django.contrib.auth.views import LogoutView
from django.urls import path
from account import views


app_name = 'account'

urlpatterns = [
    path('login/', views.LoginUser.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('simple/', views.simple_view, name='simple'),
    path('register/', views.RegisterUser.as_view(), name='register'),
    path('activate/<uidb64>/<token>', views.ActivateAccountView.as_view(), name='activate'),
    path('users-cart/', views.users_cart, name='users_cart')

]