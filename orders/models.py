from django.db import models
from store.models import Item

from account.models import User
from phonenumber_field.modelfields import PhoneNumberField

class OrderitemQuery(models.QuerySet):

    def total_price(self):
        return sum(cart.item_price() for cart in self)

    def total_quantity(self):
        if self:
            return sum(cart.quantity for cart in self)
        return 0

class OrderStatus(models.Model):
    IN_PROGRESS = 'В обработке'
    ISSUED = 'Выдан'
    CANCELED = 'Отменен'
    STATUS_CHOICES = [
        (IN_PROGRESS, 'В обработке'),
        (ISSUED, 'Выдан'),
        (CANCELED, 'Отменен')
    ]
    order_status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=IN_PROGRESS, verbose_name='Статус заказа')

    def __str__(self):
        return self.order_status
    class Meta:
        verbose_name = 'Статус заказа'
        verbose_name_plural = 'Статусы Заказов'


class Order(models.Model):
    user = models.ForeignKey(User, models.SET_DEFAULT, blank=True, null=True, verbose_name='Пользователь', default=None)
    created_timestamp = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания заказа')
    phone_number = PhoneNumberField(max_length=16, verbose_name='Номер телефона')
    requires_delivery = models.BooleanField(default=False, verbose_name='Требуется доставка')
    delivery_address = models.TextField(null=True, blank=True, verbose_name='Адрес доставки')
    payment_on_get = models.BooleanField(default=False, verbose_name='Оплата при получении')
    is_paid = models.BooleanField(default=False, verbose_name='Состояние оплаты')
    status = models.ForeignKey(OrderStatus, on_delete=models.SET_DEFAULT, verbose_name='Статус заказа', default=1)

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return f'Заказ № {self.pk} | Покупатель {self.user.email} {self.user.username if self.user.username else 'покупатель'}'


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name='Заказ')
    item = models.ForeignKey(Item, on_delete=models.SET_DEFAULT, null=True, blank=True, verbose_name='Продукт', default=None)
    name = models.CharField(max_length=150, verbose_name='Название')
    price = models.DecimalField(max_digits=7, decimal_places=2, verbose_name='Цена')
    quantity = models.PositiveSmallIntegerField(default=0, verbose_name='Количество')
    created_timestamp = models.DateTimeField(auto_now_add=True, verbose_name='Дата продажи')

    class Meta:
        verbose_name = 'Проданный товар'
        verbose_name_plural = 'Проданные товары'

    objects = OrderitemQuery.as_manager()

    def items_price(self):
        return round(self.price * self.quantity, 2)

    def __str__(self):
        return f'Товар {self.name} | Заказ № {self.order.pk}'