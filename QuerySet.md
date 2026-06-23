from prodotti.models import Prodotto
from decimal import Decimal

prodotti = [
    Prodotto(
        nome="Smartphone Galaxy S24",
        descrizione="Smartphone di ultima generazione con display AMOLED, 5G e fotocamera da 108MP",
        prezzo=Decimal("899.99"),
        categoria="Elettronica",
        quantita=25
    ),
    ...
    
]

# Inserisci con bulk_create
creati = Prodotto.objects.bulk_create(prodotti)



from prodotti.models import Prodotto_new, Cliente, Ordine
from decimal import Decimal
from datetime import datetime, timedelta
import random

# 1. CREA 10 CLIENTI
clienti = [
    Cliente(nome="Mario", cognome="Rossi", email="mario.rossi@email.com", telefono="3331234567", indirizzo="Via Roma 1, Milano"),
    ...
]

Cliente.objects.bulk_create(clienti)

### creazione array per stato ordine random
stati_ordine = ['In elaborazione', 'Spedito', 'Consegnato', 'Cancellato']
ordini = []

for cliente in clienti_creati:
    num_ordini = random.randint(1, 3)
    for _ in range(num_ordini):
        prodotto = random.choice(prodotti)
        ordine = Ordine(
            cliente=cliente,
            prodotto=prodotto,  # ForeignKey
            data_ordine=datetime.now() - timedelta(days=random.randint(0, 30)),
            stato=random.choice(stati_ordine),
            quantita=random.randint(1, 5),
            totale=prodotto.prezzo * random.randint(1, 5)
        )
        ordini.append(ordine)

Ordine.objects.bulk_create(ordini)

### Cerca prodotti tra 10-100 €
queryset

>>> prodotti_10_100_euro = Prodotto_new.objects.filter(prezzo__gte=10, prezzo__lte=100)
>>> 
>>> prodotti_10_100_euro                                                                   
<QuerySet [<Prodotto_new: T-Shirt Cotton Basic, T-shirt in cotone 100% bio, disponibile in vari colori>, <Prodotto_new: Jeans Slim Fit, Jeans in denim stretch, vestibilità slim fit>, <Prodotto_new: Giacca Invernale Puffer, Giacca imbottita con piumino, impermeabile e antivento>, <Prodotto_new: Zaino Travel Backpack, Zaino da viaggio 40L con porta PC, impermeabile>, <Prodotto_new: Bollitore Elettrico, Bollitore in acciaio con doppia parete, temperatura regolabile>, <Prodotto_new: Lampada da Scrivania LED, Lampada LED con regolazione intensità e temperatura colore>, <Prodotto_new: Borsa in Pelle, Borsa in vera pelle, capiente e con tracolla regolabile>, <Prodotto_new: Portafoglio Minimal, Portafoglio in pelle, scomparti per carte e monete>, <Prodotto_new: Bracciale Argento, Bracciale in argento 925, chiusura a moschettone>, <Prodotto_new: Collana Cuore, Collana con pendente a forma di cuore, placcata oro>, <Prodotto_new: Anello Brillante, Anello con zircone, in argento 925>, <Prodotto_new: Set Cosmetici Naturali, Set con crema viso, siero e tonico, ingredienti bio>, <Prodotto_new: Crema Solare SPF 50, Crema solare ad ampio spettro, resistente all'acqua>, <Prodotto_new: Kit Primo Soccorso, Kit completo con garze, cerotti, disinfettante e forbici>, <Prodotto_new: Mouse Wireless Logitech, Mouse ergonomico wireless, silenzioso, batteria 2 anni>, <Prodotto_new: Tastiera Meccanica RGB, Tastiera meccanica con switch blue, retroilluminazione RGB>, <Prodotto_new: Cavo USB-C 2m, Cavo USB-C ad alta velocità, ricarica rapida e trasferimento dati>, <Prodotto_new: Tappetino Yoga Premium, Tappetino antiscivolo, spessore 6mm, con tracolla>]>
>>> 

### filtra prodotti per categoria
>>> cat_elettr = Prodotto_new.objects.filter(categoria = 'Elettronica')
>>> cat_elettr
<QuerySet [<Prodotto_new: Smartphone Galaxy S24, Smartphone di ultima generazione con display AMOLED, 5G e fotocamera da 108MP>, <Prodotto_new: Laptop Dell XPS 13, Notebook ultraportatile con schermo InfinityEdge, processore Intel i7 e 16GB RAM>, <Prodotto_new: Auricolar Wireless Sony WH-1000XM5, Cuffie over-ear con cancellazione attiva del rumore e batteria da 30 ore>, <Prodotto_new: Tablet iPad Air, Tablet con chip M1, display Liquid Retina e supporto Apple Pencil>, <Prodotto_new: Orologio Smart Watch Pro, Smartwatch con GPS, monitoraggio fitness e battito cardiaco>, <Prodotto_new: Mouse Wireless Logitech, Mouse ergonomico wireless, silenzioso, batteria 2 anni>, <Prodotto_new: Tastiera Meccanica RGB, Tastiera meccanica con switch blue, retroilluminazione RGB>, <Prodotto_new: Monitor 4K 27 Pollici, Monitor UHD 4K, HDR, alta fedeltà colore>, <Prodotto_new: Cavo USB-C 2m, Cavo USB-C ad alta velocità, ricarica rapida e trasferimento dati>]>
>>> 

### filtra ordini con prodotto id = 3
>>> ordini_con_prodotto_3 = Ordine.objects.filter(prodotto_id=3)
>>> ordini_con_prodotto_3   
<QuerySet [<Ordine: Ordine #7 - Francesco Gialli>, <Ordine: Ordine #17 - Sara Marrone>]>
>>> 

### Media, massimo, minimo, conteggio
>>> from django.db.models import Avg, Min, Max, Count

    prezzo_medio = Prodotto_new.objects.aggregate(Avg('prezzo'))

>>> prezzo_medio = Prodotto_new.objects.aggregate(Avg('prezzo')) 
>>> prezzo_medio
{'prezzo__avg': Decimal('183.756666666667')}
>>> 

>>> numero_prodotti = Prodotto_new.objects.aggregate(Count('id'))
>>> numero_prodotti
{'id__count': 30}

>>> prezzo_min = Prodotto_new.objects.aggregate(Min('prezzo'))
>>> prezzo_min
{'prezzo__min': Decimal('8.99000000000000')}
>>> 

### Ordina
>>> prod_piu_costosi = Prodotto_new.objects.order_by('-prezzo')[:5]
>>> prod_piu_costosi
<QuerySet [<Prodotto_new: Laptop Dell XPS 13, Notebook ultraportatile con schermo InfinityEdge, processore Intel i7 e 16GB RAM>, <Prodotto_new: Smartphone Galaxy S24, Smartphone di ultima generazione con display AMOLED, 5G e fotocamera da 108MP>, <Prodotto_new: Tablet iPad Air, Tablet con chip M1, display Liquid Retina e supporto Apple Pencil>, <Prodotto_new: Monitor 4K 27 Pollici, Monitor UHD 4K, HDR, alta fedeltà colore>, <Prodotto_new: Auricolar Wireless Sony WH-1000XM5, Cuffie over-ear con cancellazione attiva del rumore e batteria da 30 ore>]>