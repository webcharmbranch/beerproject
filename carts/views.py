from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.views import View

from carts.mixins import CartMixin
from carts.models import Cart
from carts.utils import get_user_carts
from store.models import Item

class CartAddView(CartMixin, View):
    def post(self, request):
        product_id = request.POST.get("product_id")
        item = Item.objects.get(id=product_id)

        cart = self.get_cart(request, item=item)

        if cart:
            cart.quantity += 1
            cart.save()
        else:
            Cart.objects.create(user=request.user if request.user.is_authenticated else None,
                                session_key=request.session.session_key if not request.user.is_authenticated else None,
                                item=item, quantity=1)
        response_data = {
            'message':  'Товар добавлен в корзину',
            'cart_items_html': self.render_cart(request, 'carts/includes/basket_bar.html')
        }
        return JsonResponse(response_data)


class CartChangeView(CartMixin, View):
    def post(self, request):
        cart_id = request.POST.get('cart_id')
        cart = self.get_cart(request, cart_id=cart_id)
        cart.quantity = request.POST.get('quantity')
        cart.save()
        quantity = cart.quantity
        response_data = {
            'message': 'Количество изменено',
            'quantity': quantity,
            'cart_items_html': self.render_cart(request, 'account/included_users_cart.html')
        }
        return JsonResponse(response_data)

class CartRemove(CartMixin, View):
    def post(self, request):
        cart_id = request.POST.get('cart_id')

        cart = self.get_cart(request, cart_id=cart_id)
        quantity = cart.quantity
        cart.delete()

        response_data = {
            'message': 'Товар удален из корзины',
            'quantity_deleted': quantity,
            'cart_items_html': self.render_cart(request, 'account/included_users_cart.html')
        }

        return JsonResponse(response_data)
    