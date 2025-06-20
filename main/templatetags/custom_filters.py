import unicodedata
from django import template

register = template.Library()

def remover_acentos(texto):
    return ''.join(
        c for c in unicodedata.normalize('NFD', texto)
        if unicodedata.category(c) != 'Mn'
    )

@register.filter
def dict_get(dicionario, chave):
    if dicionario and chave:
        chave_normalizada = remover_acentos(chave).lower()
        return dicionario.get(chave_normalizada)
    return ''
