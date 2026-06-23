from django.db import models

# Create your models here.
class Prodotto(models.Model):
    titolo = models.CharField(max_length=500)
    autore = models.CharField(max_length=200)
    anno_pubblicazione = models.IntegerField()
    disponibile = models.BooleanField(default=True)
    

    def __str__(self):
        return f"{self.titolo} di {self.autore}"

    class Meta:
        verbose_name_plural = 'Prodotti' # Forza il plurale nella visualizzazione in /Admin
       
