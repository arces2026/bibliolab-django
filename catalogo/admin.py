from django.contrib import admin
from .models import Libro, Prodotto, Cliente, Ordine
# Register your models here.

@admin.register(Libro)
class LibroAdmin(admin.ModelAdmin):
    list_display = ['titolo', 'autore', 'disponibile', 'anno_pubblicazione']
    list_filter = ['disponibile']
    search_fields = ['autore', 'titolo']
    list_editable = ['disponibile']


@admin.register(Prodotto)
class ProdottoAdmin(admin.ModelAdmin):
    list_display = ['nome', 'descrizione', 'prezzo', 'categoria', 'quantita']
    list_filter = ['categoria']
    search_fields = ['descrizione']
    ordering = ['-prezzo']


@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ['nome', 'cognome', 'telefono', 'email', 'indirizzo']
    list_filter = ['cognome']
    search_fields = ['cognome']


@admin.register(Ordine)
class OrdineAdmin(admin.ModelAdmin):
    list_display = ['cliente', 'prodotto', 'quantita', 'totale', 'data_ordine', 'stato']
    list_filter = ['cliente']
    search_fields = ['stato']