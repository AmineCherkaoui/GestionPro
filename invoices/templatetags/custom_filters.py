import locale
from django import template
from num2words import num2words

register = template.Library()

@register.filter()
def format_currency(value):
    try:
        locale.setlocale(locale.LC_ALL, 'fr_FR.UTF-8')
    except locale.Error:
        locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
    return locale.currency(value, symbol=False, grouping=True)

@register.filter()
def montant_to_text(value):
    partie_entiere = int(value)
    partie_decimal = int(round((value - partie_entiere) * 100))
    montant_en_lettres = f"{num2words(partie_entiere, lang='fr')} dirhams"
    if partie_decimal > 0:
        montant_en_lettres += f" et {num2words(partie_decimal, lang='fr')} centimes"
    return montant_en_lettres

@register.filter()
def format_rib(value):
    value = str(value)
    return f"{value[:3]} {value[3:6]} {value[6:22]} {value[22:]}"

@register.filter()
def multiply(num1, num2):
    return num1 * num2

@register.filter()
def group(user, group_name):
    return user.groups.filter(name=group_name).exists()


@register.filter
def add_dots(value):
    if isinstance(value, str):
        return '.'.join(value)
    return value



