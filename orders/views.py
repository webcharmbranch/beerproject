from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ValidationError
from django.db import transaction
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import FormView

from carts.models import Cart
from orders.forms import CreateOrderForm
from orders.models import Order, OrderItem


class OrderCreateView(LoginRequiredMixin, FormView):
    template_name = 'orders/create_order.html'
    form_class = CreateOrderForm
    success_url = reverse_lazy('account:simple')

    def get_initial(self):
        initial = super().get_initial()
        initial['first_name'] = self.request.user.username
        return initial

    def form_valid(self, form):
        try:
            with transaction.atomic():
                user = self.request.user
                cart_items = Cart.objects.filter(user=user)

                if cart_items.exists():
                    # Создаем заказ
                    order = Order.objects.create(
                        user=user,
                        phone_number=form.cleaned_data['phone_number'],
                        requires_delivery=form.cleaned_data['requires_delivery'],
                        delivery_address=form.cleaned_data['delivery_address'],
                        payment_on_get=form.cleaned_data['payment_on_get']
                    )
                    # Создаем OrderItem заказанных товаров
                    for cart_item in cart_items:
                        item = cart_item.item
                        name = cart_item.item.name
                        price = cart_item.item.sell_price()
                        quantity = cart_item.quantity

                        if item.stock < quantity:
                            raise ValidationError(f'Недостаточное количество товара {name}, в наличии - {item.stock}')

                        OrderItem.objects.create(
                            order=order,
                            item=item,
                            name=name,
                            price=price,
                            quantity=quantity,
                        )
                        item.stock -= quantity
                        item.save()
                    # Очищаем корзину пользователя после создания заказа
                    cart_items.delete()

                    messages.success(self.request, 'Заказ оформлен!')
                    return redirect('account:simple')
        except ValidationError as e:
            messages.warning(self.request, str(e))
            return redirect('carts:order')

    def form_invalid(self, form):
        messages.error(self.request, 'Заполните все обязательные поля!')
        return redirect('orders:create_order')
