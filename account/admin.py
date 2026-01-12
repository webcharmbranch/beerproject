from django.contrib import admin
from account.models import UserType, User
from orders.admin import OrderTabularAdmin

# Register your models here.
admin.site.register(UserType)
# admin.site.register(User)

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['email', 'username', ]
    search_fields = ['email', 'username', ]

    # inlines = [CartTabAdmin,]
    inlines = [OrderTabularAdmin, ]