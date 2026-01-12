from django.contrib import admin

# Register your models here.

from store.models import *




class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {"slug": ["name"]}

class ItemAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price', 'stock', 'created_at', 'updated_at']
    list_filter = ['category', 'created_at', 'updated_at']
    list_editable = ['category', 'price', 'stock']
    prepopulated_fields = {"slug": ["name"]}


admin.site.register(Item, ItemAdmin)
admin.site.register(Brand)
admin.site.register(BeerStyle)
admin.site.register(Volume)
admin.site.register(PackageType)
admin.site.register(Country)
admin.site.register(Discount)
admin.site.register(Category, CategoryAdmin)