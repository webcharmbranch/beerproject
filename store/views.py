from django.shortcuts import redirect, render
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.views.generic import ListView
from store.utils import q_search
from store.models import Item
from store.filters import MyModelFilter

# Create your views here.
def show_item(request, item_slug):
    item = get_object_or_404(Item, slug=item_slug)
    context = {'item': item}
    return render(request, 'store/item.html', context)


class StoreListView(ListView):
    context_object_name = 'items'
    queryset = Item.objects.order_by('name')
    template_name = 'store/store.html'
    paginate_by = 5


class CategoryListView(ListView):
    context_object_name = 'items'
    template_name = 'store/category.html'
    paginate_by = 4
    
    def get_queryset(self):
        query = self.request.GET.get('q', None)
        if query:
            goods = q_search(query)
            if goods:
                self.my_filters = MyModelFilter(self.request.GET, queryset=goods)
                return self.my_filters.qs
            self.my_filters = MyModelFilter(self.request.GET, queryset=Item.objects.filter(id=-5))
            return self.my_filters.qs
        if self.kwargs:
            self.category_slug = self.kwargs.get("category_slug", None)
            if self.category_slug:
                queryset = Item.objects.filter(category__slug=self.category_slug)
                self.my_filters = MyModelFilter(self.request.GET, queryset=queryset)
                return self.my_filters.qs
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.my_filters and len(self.my_filters.qs) != 0:
            context['form'] = self.my_filters.form
        elif self.my_filters and len(self.my_filters.qs) == 0:
            context['empty_search'] = 'Поиск не дал результатов'
        if self.kwargs:
            if self.category_slug:
                if self.my_filters:
                    context['category_name'] = self.category_slug
        return context
    