import django_filters
from django_filters.widgets import RangeWidget
from store.models import *
from django import forms


class MyModelFilter(django_filters.FilterSet):
    
    price__gt = django_filters.NumberFilter(field_name='price', lookup_expr='gte', label='Цена', 
                                            widget=forms.widgets.TextInput(attrs={'placeholder':'от'}))
    price__lt = django_filters.NumberFilter(field_name='price', lookup_expr='lte', label='', 
                                            widget=forms.widgets.TextInput(attrs={'placeholder':'до'}))
    brand__name = django_filters.ModelMultipleChoiceFilter(label='Бренд',
        field_name='brand__name',
        to_field_name='name',
        queryset=Brand.objects.all(), widget=forms.CheckboxSelectMultiple(attrs={"class":"brand_widget"})
    )
    beer_style__name = django_filters.ModelMultipleChoiceFilter(label='Стиль напитка',
        field_name='beer_style__name',
        to_field_name='name',
        queryset=BeerStyle.objects.all(), widget=forms.CheckboxSelectMultiple(attrs={"class":"beer_style_widget"})
    )
    volume__value = django_filters.ModelMultipleChoiceFilter(label='Объем',
        field_name='volume__value',
        to_field_name='value',
        queryset=Volume.objects.all(), widget=forms.CheckboxSelectMultiple(attrs={"class":"volume_widget"})
    )
    package_type__name = django_filters.ModelMultipleChoiceFilter(label='Тип упаковки',
        field_name='package_type__name',
        to_field_name='name',
        queryset=PackageType.objects.all(), widget=forms.CheckboxSelectMultiple(attrs={"class":"package_type_widget"})
    )
    country__name = django_filters.ModelMultipleChoiceFilter(label='Страна',
        field_name='country__name',
        to_field_name='name',
        queryset=Country.objects.all(), widget=forms.CheckboxSelectMultiple(attrs={"class":"volume_widget"})
    )

    
    class Meta:
        model = Item
        fields = ['name', 'discount',]