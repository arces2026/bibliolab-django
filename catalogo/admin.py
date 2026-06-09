from django.contrib import admin
from .models import Libro
# Register your models here.

@admin.register(Libro)
class LibroAdmin(admin.ModelAdmin):
    list_display = ['titolo', 'autore', 'prezzo', 'disponibile', 'creato_il']
    list_filter = ['disponibile']
    search_fields = ['autore', 'titolo']
    list_editable = ['disponibile', 'prezzo']