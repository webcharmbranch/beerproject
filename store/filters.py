import django_filters
from django_filters.widgets import RangeWidget
from store.models import *
from django import forms


def get_models_choices(my_model):
    if my_model.__name__ == 'Volume':
        q_set = my_model.my_objects.normalize_value()
        return q_set
    else:
        q_set = my_model.objects.all()
    model_names_dict = {}
    for item in q_set:
        if hasattr(my_model, 'name'):
            model_names_dict[item.name] = item.name
        elif hasattr(my_model, 'value'):
            model_names_dict[item.value] = item.value
    return list(zip(model_names_dict.keys(), model_names_dict.values()))


BRAND_CHOICES = get_models_choices(Brand)
BEER_STYLE_CHOICES = get_models_choices(BeerStyle)
VOLUME_CHOICES = get_models_choices(Volume)
PACKAGETYPE_CHOICES = get_models_choices(PackageType)
COUNTRY_CHOICES = get_models_choices(Country)


class MyModelFilter(django_filters.FilterSet):
    
    price__gt = django_filters.NumberFilter(field_name='price', lookup_expr='gte', label='Цена', 
                                            widget=forms.widgets.TextInput(attrs={'placeholder':'от'}))
    price__lt = django_filters.NumberFilter(field_name='price', lookup_expr='lte', label='', 
                                            widget=forms.widgets.TextInput(attrs={'placeholder':'до'}))
    brand__name = django_filters.MultipleChoiceFilter(label='Бренд',
        choices=BRAND_CHOICES, widget=forms.CheckboxSelectMultiple(attrs={"class":"brand_widget"})
    )
    beer_style__name = django_filters.MultipleChoiceFilter(label='Стиль напитка',
        choices=BEER_STYLE_CHOICES, widget=forms.CheckboxSelectMultiple(attrs={"class":"beer_style_widget"})
    )
    volume__value = django_filters.MultipleChoiceFilter(label='Объем',
        choices=VOLUME_CHOICES, widget=forms.CheckboxSelectMultiple(attrs={"class":"volume_widget"})
    )
    package_type__name = django_filters.MultipleChoiceFilter(label='Тип упаковки',
        choices=PACKAGETYPE_CHOICES, widget=forms.CheckboxSelectMultiple(attrs={"class":"package_type_widget"})
    )
    country__name = django_filters.MultipleChoiceFilter(label='Страна',
        choices=COUNTRY_CHOICES, widget=forms.CheckboxSelectMultiple(attrs={"class":"volume_widget"})
    )

    
    class Meta:
        model = Item
        fields = ['name', 'discount',]