from django.utils.http import urlencode
from django import template
from store.models import *

register = template.Library()


# @register.simple_tag(takes_context=True)
# def change_params(context, **kwargs):
#     query = context['request'].GET.dict()
#     query.update(kwargs)
#     return urlencode(query)


@register.simple_tag(takes_context=True)
def change_params(context, **kwargs):
    """
    поскольку context['request'].GET.dict() метод в первой закомменченой функции в этом модуле достает из списка только
    последнее значение, а нужны все, то метод .dict() не годится, как и словарь вообще, т.к. он хранит уникальные ключи,
    а нам нужны повторяющиеся ключи. Поэтому из QueryDict объекта первым шагом делаем список кортежей из двух элементов,
    а на втором шаге добавляем в список кортежей значения из словаря kwargs причем так, как бы это сделал метод .update()
    если значение из kwargs уже есть в списке кортежей, то обновляем значение (то есть второй элемент кортежа), если же
    значение из kwargs отсутствует в списке кортежей, то добавляем это значение в конец списка кортежей как кортеж из
    двух элементов
    """
    req = context['request'].GET
    query = []
    for key in req:
        if len(req.getlist(key, default='')) < 2:
            query.append((key, *req.getlist(key, default='')))
        else:
            for value in req.getlist(key, default=''):
                query.append((key, value))

    for key, value in kwargs.items():
        for index, item in enumerate(query):
            if item[0] == key:
                query[index] = (key, value)
                return urlencode(query)
    for key, value in kwargs.items():
        query.append((key, value))
    return urlencode(query)