from django.db import models
from django.urls import reverse

# Create your models here.
class Brand(models.Model):
    name = models.CharField(max_length=150, verbose_name='название бренда')
    description = models.TextField(verbose_name='описание бренда', null=True, blank=True)

    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ('name',)
        verbose_name = 'Название бренда'
        verbose_name_plural = 'Названия брендов'

    
class BeerStyle(models.Model):
    name = models.CharField(max_length=150, verbose_name='стиль напитка')
    description = models.TextField(verbose_name='описание стиля напитка', null=True, blank=True)

    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ('name',)
        verbose_name = 'Стиль напитка'
        verbose_name_plural = 'Стили Напитков'

class VolumeNormQs(models.QuerySet):

    def normalize_value(self):
        if self:
            # print('VALUES_FROM MYMANAGER', self.values)
            new_qs = dict()
            for item in self.values():
                # print('INITIAL_DICT_ITEMS', item)
                if item['value'] < 1:
                    new_qs[item['id']]= item['value'].normalize()
                else:
                    new_qs[item['id']]=int(item['value'])
            return new_qs

class VolumeNormManager(models.Manager.from_queryset(VolumeNormQs)):
    pass

class Volume(models.Model):
    value = models.DecimalField(max_digits=5, decimal_places=3, verbose_name='объем')

    def __str__(self):
        if self.value < 1:
            return str(self.value.normalize())
        else:
            return str(int(self.value))
    class Meta:
        verbose_name = 'Объем'
        verbose_name_plural = 'Объемы'

    objects = models.Manager()
    my_objects = VolumeNormManager()

class PackageType(models.Model):
    name = models.CharField(max_length=150, verbose_name='тип упаковки')

    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ('name',)
        verbose_name = 'Тип упаковки'
        verbose_name_plural = 'Типы упаковок'


class Country(models.Model):
    name = models.CharField(max_length=150, verbose_name='страна')

    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ('name',)
        verbose_name = 'Страна'
        verbose_name_plural = 'Страны'


class Discount(models.Model):
    value = models.PositiveSmallIntegerField(default=5, verbose_name='скидка')

    def __str__(self):
        return str(self.value)+'%'
    
    class Meta:
        verbose_name = 'Скидка'
        verbose_name_plural = 'Скидки'


class Category(models.Model):
    name = models.CharField(max_length=150, verbose_name='категория')
    slug = models.SlugField(max_length=150, unique=True)

    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ('name',)
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
    
    def get_absolute_url(self):
        return reverse('store:category', kwargs={'category_slug': self.slug})


class Item(models.Model):
    name = models.CharField(max_length=150, verbose_name='название', db_index=True)
    slug = models.SlugField(max_length=150, unique=True)
    description = models.TextField(verbose_name='описание', null=True, blank=True)
    stock = models.PositiveSmallIntegerField(default=0, verbose_name='количество на складе')
    price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='цена')
    brand = models.ForeignKey(Brand, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='бренд')
    beer_style = models.ForeignKey(BeerStyle, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='стиль напитка')
    volume = models.ForeignKey(Volume, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='объем')
    package_type = models.ForeignKey(PackageType, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='тип упаковки')
    country = models.ForeignKey(Country, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='страна')
    discount = models.ForeignKey(Discount, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='скидка')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, verbose_name='категория')
    img = models.ImageField(upload_to='images/%Y/%m/%d', verbose_name='изображение', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='создано')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='изменено')

    def __str__(self):
        return f'{self.name} Количество - {self.stock}'

    class Meta:
        ordering = ('name',)
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'
    
    def get_absolute_url(self):
        return reverse('store:item', kwargs={'item_slug': self.slug})

    def sell_price(self):
        if self.discount:
            return round(float(self.price) - float(self.price)*self.discount.value/100, 2)
        return self.price
