from django.db import models

from account.models import User
from store.models import Item

class CartQueryset(models.QuerySet):

    def total_price(self):
        return sum(cart.item_price() for cart in self)

    def total_quantity(self):
        if self:
            return sum(cart.quantity for cart in self)
        return 0


class Cart(models.Model):

    user = models.ForeignKey(to=User, on_delete=models.CASCADE, blank=True, null=True, verbose_name='пользователь')
    item = models.ForeignKey(to=Item, on_delete=models.CASCADE, verbose_name='продукт')
    quantity = models.PositiveSmallIntegerField(default=0, verbose_name='количество')
    session_key = models.CharField(max_length=32, null=True, blank=True)
    created_timestamp = models.DateTimeField(auto_now_add=True, verbose_name='дата добавления')

    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'

    objects = CartQueryset().as_manager()

    def item_price(self):
        return round(self.item.sell_price()*self.quantity ,2)
    def __str__(self):
        if self.user:
            return f'Корзина {self.user.email} | Товар {self.item.name} | Количество {self.quantity}'
        return f'Анонимная корзина | Товар {self.item.name} | Количество {self.quantity}'
