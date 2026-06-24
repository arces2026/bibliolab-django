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
       

class Prodotto_new(models.Model):
    nome = models.CharField(max_length=500)
    descrizione = models.TextField()
    prezzo = models.DecimalField(max_digits=10,decimal_places= 2)
    categoria = models.CharField(max_length=200)
    quantita = models.IntegerField()

    def __str__(self):
        return f'{self.nome}, {self.descrizione}'
    
    class Meta:
        verbose_name_plural = 'Prodotti_new'

# Definisci le scelte PRIMA del modello
STATO_ORDINE = [
    ('in_elaborazione', 'In elaborazione'),
    ('spedito', 'Spedito'),
    ('consegnato', 'Consegnato'),
    ('cancellato', 'Cancellato'),
]

class Ordine(models.Model):
    cliente = models.ForeignKey('Cliente', on_delete=models.CASCADE, related_name='ordini_clienti')
    prodotto = models.ForeignKey(Prodotto_new, on_delete=models.CASCADE, related_name='ordini_prodotti')
    quantita = models.PositiveIntegerField(default=1)
    totale = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    data_ordine = models.DateTimeField(default='2024-01-01 00:00:00')
    stato = models.CharField(max_length=50, choices=STATO_ORDINE, default='in_elaborazione')
    
    def __str__(self):
        return f"Ordine #{self.id} - {self.cliente.nome} {self.cliente.cognome}"


class Cliente(models.Model):
    nome = models.CharField(max_length=200)
    cognome = models.CharField(max_length=200, blank=True, default='')
    email = models.EmailField(blank=True, default='')
    telefono = models.CharField(max_length=30, blank=True, default='')
    indirizzo = models.CharField(max_length=100, blank=True, default='')

    def __str__(self):
        return f'{self.nome}'
    
    class Meta:
        verbose_name_plural = 'Clienti'




