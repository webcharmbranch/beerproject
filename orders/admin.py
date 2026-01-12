from django.contrib import admin
from orders.models import OrderStatus, Order, OrderItem

admin.site.register(OrderStatus)
# admin.site.register(Order)
# admin.site.register(OrderItem)

class OrderItemTabularAdmin(admin.TabularInline):
    model = OrderItem
    fields = ('item', 'name', 'price', 'quantity')
    search_fields = (
        'item',
        'name',
    )
    extra = 0


    @admin.register(OrderItem)
    class OrderItemAdmin(admin.ModelAdmin):
        list_display = ('order', 'item', 'name', 'price', 'quantity')
        search_fields = (
            'order',
            'item',
            'name',
        )


class OrderTabularAdmin(admin.TabularInline):
    model = Order
    fields = (
        'requires_delivery',
        'status',
        'payment_on_get',
        'is_paid',
        'created_timestamp',
    )

    search_fields = (
        'requires_delivery',
        'payment_on_get',
        'is_paid',
        'created_timestamp',
    )
    readonly_fields = ('created_timestamp',)
    extra = 0

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'requires_delivery',
        'status',
        'payment_on_get',
        'is_paid',
        'created_timestamp',
    )
    search_fields = (
        'id',
    )
    readonly_fields = ('created_timestamp',)
    list_filter = (
        'requires_delivery',
        'status',
        'payment_on_get',
        'is_paid'
    )
    inlines = (OrderItemTabularAdmin,)