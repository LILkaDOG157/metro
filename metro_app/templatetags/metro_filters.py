from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()

@register.filter
def normalize_coord(value):
    """Нормализует координаты для отображения на карте"""
    try:
        # Предполагаем, что координаты в диапазоне примерно от 55.5 до 55.9 для широты
        # и от 37.3 до 37.9 для долготы (для Москвы)
        if float(value) > 50:  # Это широта
            return ((float(value) - 55.5) / (55.9 - 55.5)) * 100
        else:  # Это долгота
            return ((float(value) - 37.3) / (37.9 - 37.3)) * 100
    except (ValueError, TypeError):
        return 50

@register.filter
def line_color(line):
    """Возвращает цвет для линии метро"""
    colors = {
        'Красная': '#FF0000',
        'Синяя': '#0000FF',
        'Зеленая': '#00FF00',
        'Оранжевая': '#FFA500',
        'Фиолетовая': '#800080',
        'Коричневая': '#A52A2A',
        'Серая': '#808080',
        'Желтая': '#FFFF00',
        'Бирюзовая': '#40E0D0',
        'Розовая': '#FFC0CB'
    }
    return colors.get(line, '#000000')

@register.filter
def get_item(dictionary, key):
    """Получает значение из словаря по ключу"""
    return dictionary.get(key) 