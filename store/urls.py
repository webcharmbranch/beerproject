from django.urls import path
from store import views

app_name = "store"

urlpatterns = [
               path('', views.StoreListView.as_view(), name='main'),
               path('search/', views.CategoryListView.as_view(), name='search'),
               path('category/<slug:category_slug>/', views.CategoryListView.as_view(), name='category'),
               path('item/<slug:item_slug>/', views.show_item, name='item'),
               ]
