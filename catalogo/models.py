from django.db import models

# Create your models here.
class Libro(models.Model):
    titolo = models.CharField(max_length=500)
    autore = models.CharField(max_length=200)
    editore = models.CharField(max_length=200)
    descrizione = models.TextField(blank=True)
    disponibile = models.BooleanField(default=True)
    prezzo = models.DecimalField(max_digits=8, decimal_places=2)
    anno_pubblicazione = models.DateField(blank=True)
    creato_il = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.titolo} di {self.autore} edito da {self.editore}"