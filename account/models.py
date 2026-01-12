from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from phonenumber_field.modelfields import PhoneNumberField
import uuid

# Create your models here.
class UserType(models.Model):
    USER = 'Пользователь'
    MANAGER = 'Менеджер'
    ADMIN = 'Администратор'
    USER_TYPE_CHOICES = [
        (USER, 'пользователь'),
        (MANAGER, 'менеджер'),
        (ADMIN, 'администратор')
    ]
    type_of_user = models.CharField(max_length=13, choices=USER_TYPE_CHOICES, default=USER)

    class Meta:
        verbose_name = 'Тип пользователя'
        verbose_name_plural = 'Типы пользователей'

    def __str__(self):
        return self.type_of_user

class MyUserManager(BaseUserManager):

    def create_superuser(self, email, password, **other_fields):

        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)

        if other_fields.get('is_staff') is not True:
            raise ValueError(
                'Суперпользователь должен иметь поле is_staff=True'
            )
        if other_fields.get('is_superuser') is not True:
            raise ValueError(
                'Суперпользователь должен иметь поле is_superuser=True'
            )
        return self.create_user(email, password, **other_fields)

    def create_user(self, email, password, **other_fields):
        if not email:
            raise ValueError('Адрес электронной почты обязателен')
        email = self.normalize_email(email)
        user = self.model(email=email, **other_fields)
        user.set_password(password)
        user.save()
        return user


class User(AbstractBaseUser, PermissionsMixin):
    uuid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False, verbose_name='уникальный идентификатор')
    email = models.EmailField(verbose_name='адрес электронной почты', max_length=150, unique=True)
    username = models.CharField(verbose_name='имя пользователя', max_length=150, blank=True, null=True, unique=True)
    phone = PhoneNumberField(verbose_name='номер телефона', blank=True, null=True, unique=True)
    image = models.ImageField(verbose_name='фотография пользователя', blank=True, null=True)
    date_of_birth = models.DateField(verbose_name='дата рождения', blank=True, null=True)

    user_type = models.ForeignKey(UserType, on_delete=models.SET_NULL, verbose_name='тип пользователя', blank=True, null=True, default=1)

    date_joined = models.DateTimeField(verbose_name='дата регистрации', auto_now_add=True)
    last_login = models.DateTimeField(verbose_name='дата последнего почещения', auto_now=True)

    is_superuser = models.BooleanField(verbose_name='является суперпользователем', default=False)
    is_staff = models.BooleanField(verbose_name='является сотрудником', default=False)
    is_active = models.BooleanField(verbose_name='учетная запись активирована', default=False)

    is_verified = models.BooleanField(verbose_name='учетная запись верифицирована', default=False)

    objects = MyUserManager()

    USERNAME_FIELD = 'email'
    # REQUIRED_FIELDS = ['username']

    class Meta:
        verbose_name = 'Пользователя'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.email
