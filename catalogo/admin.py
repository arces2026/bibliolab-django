from django.contrib import admin
from .models import Prodotto
# Register your models here.

@admin.register(Prodotto)
class ProdottoAdmin(admin.ModelAdmin):
    list_display = ['titolo', 'autore', 'disponibile', 'anno_pubblicazione']
    list_filter = ['disponibile']
    search_fields = ['autore', 'titolo']
    list_editable = ['disponibile']