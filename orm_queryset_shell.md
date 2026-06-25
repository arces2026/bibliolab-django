# ORM QuerySet via shell

---

## Indice

- [1. CREATE](#1-create)
  - [1.1 Prodotti](#11-prodotti)
  - [1.2 Clienti](#12-clienti)
  - [1.3 Ordini](#13-ordini)
  - [1.4 Update stato ordini](#14-update-stato-ordini)
- [2. Filtraggio, Ordinamento e Aggregazioni](#2-filtraggio-ordinamento-e-aggregazioni)
  - [2.1 Cerca prodotti tra 10-100€ in ordine decrescente](#21-cerca-prodotti-tra-10-100-in-ordine-decrescente)
  - [2.2 Filtra prodotti per categoria ed escludi](#22-filtra-prodotti-per-categoria-ed-escludi)
  - [2.3 Filtra ordini per prodotto id = 3](#23-filtra-ordini-per-prodotto-id--3)
- [3. Aggregate](#3-aggregate)
  - [3.1 Media, massimo, minimo, conteggio](#31-media-massimo-minimo-conteggio)
  - [3.2 Ordina — i 5 prodotti più costosi](#32-ordina--i-5-prodotti-più-costosi)

---

## 1. CREATE

### 1.1 Prodotti

Creazione di una lista di 30 prodotti tramite `bulk_create`.

```shell
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
```

[↑ Torna all'indice](#indice)

---

### 1.2 Clienti

Creazione di 10 clienti tramite `bulk_create`.

```shell
from prodotti.models import Prodotto_new, Cliente, Ordine
from decimal import Decimal
from datetime import datetime, timedelta
import random

clienti = [
    Cliente(nome="Mario", cognome="Rossi", email="mario.rossi@email.com", telefono="3331234567", indirizzo="Via Roma 1, Milano"),
    ...
]

Cliente.objects.bulk_create(clienti)
```

[↑ Torna all'indice](#indice)

---

### 1.3 Ordini

Creazione degli ordini con numero di prodotti e stato assegnati casualmente.

```shell
stati_ordine = ['In elaborazione', 'Spedito', 'Consegnato', 'Cancellato']
ordini = []

clienti_creati = Cliente.objects.all()

for cliente in clienti_creati:
    num_ordini = random.randint(1, 5)
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
```

[↑ Torna all'indice](#indice)

---

### 1.4 Update stato ordini

Aggiornamento massivo dello stato di tutti gli ordini tramite `bulk_update`.

```shell
>>> ordini = Ordine.objects.all()
>>> for ordine in ordini:
...     ordine.stato = random.choice(stati)
...
>>> Ordine.objects.bulk_update(ordini, ['stato'])
126
```

[↑ Torna all'indice](#indice)

---

## 2. Filtraggio, Ordinamento e Aggregazioni

### 2.1 Cerca prodotti tra 10-100€ in ordine decrescente

Recupera tutti i prodotti con prezzo tra 10€ e 100€, ordinati per prezzo decrescente.

```shell
>>> Range_desc = Prodotto_new.objects.filter(prezzo__gte=10, prezzo__lte=100).order_by('-prezzo')
# Alternativa equivalente:
# range_desc = Prodotto_new.objects.filter(prezzo__range=(10, 100)).order_by('-prezzo')

>>> Range_desc
<QuerySet [<Prodotto_new: Pattini a Rotelle, ...>, <Prodotto_new: Set Coltelli Cucina, ...>, ...]>
```

[↑ Torna all'indice](#indice)

---

### 2.2 Filtra prodotti per categoria ed escludi

Recupera i prodotti della categoria "Elettronica" in stock, escludendo quelli con prezzo superiore a 500€.

```shell
>>> cat_elett = Prodotto_new.objects.filter(categoria='Elettronica').exclude(prezzo__gt=500)
>>> cat_elett
<QuerySet [
    <Prodotto_new: Orologio Smart Watch, ...>,
    <Prodotto_new: Power Bank 20000mAh, ...>,
    <Prodotto_new: Caricatore Wireless, ...>,
    <Prodotto_new: Batteria Esterna, ...>
]>
```

[↑ Torna all'indice](#indice)

---

### 2.3 Filtra ordini per prodotto id = 3

Conta quanti ordini esistono per il prodotto con `id=3`.

```shell
>>> ord_prod_id3 = Ordine.objects.filter(prodotto_id=3)
>>> ord_prod_id3
<QuerySet [<Ordine: Ordine #2 - Anna Bianchi>]>
```

[↑ Torna all'indice](#indice)

---

## 3. Aggregate

### 3.1 Media, massimo, minimo, conteggio

Calcola prezzo medio, minimo, massimo e numero totale di prodotti in stock.

```shell
>>> from django.db.models import Avg, Min, Max, Count

# Prezzo medio
>>> prezzo_medio = Prodotto_new.objects.aggregate(Avg('prezzo'))
>>> prezzo_medio
{'prezzo__avg': Decimal('160.755049504951')}
>>> prezzo_medio_2 = round(prezzo_medio['prezzo__avg'], 2)
>>> prezzo_medio_2
Decimal('160.76')

# Numero prodotti
>>> numero_prodotti = Prodotto_new.objects.aggregate(Count('id'))
>>> numero_prodotti
{'id__count': 101}

# Prezzo minimo
>>> prezzo_min = Prodotto_new.objects.aggregate(Min('prezzo'))
>>> prezzo_min_2 = round(prezzo_min['prezzo__min'], 2)
>>> prezzo_min_2
Decimal('2.50')

# Prezzo massimo
>>> prezzo_max = Prodotto_new.objects.aggregate(Max('prezzo'))
>>> prezzo_max_2 = round(prezzo_max['prezzo__max'], 2)
>>> prezzo_max_2
Decimal('1499.00')

# Tutte le statistiche in una sola query
>>> stats = Prodotto_new.objects.aggregate(
...     prezzo_medio=Avg('prezzo'),
...     prezzo_max=Max('prezzo'),
...     prezzo_min=Min('prezzo')
... )
>>> stats
{'prezzo_medio': Decimal('160.755049504951'), 'prezzo_max': Decimal('1499'), 'prezzo_min': Decimal('2.5')}
```

[↑ Torna all'indice](#indice)

---

### 3.2 Ordina — i 5 prodotti più costosi

Recupera i 5 prodotti più costosi mostrando solo i campi `nome` e `prezzo`.

```shell
>>> più_costosi = Prodotto_new.objects.order_by('-prezzo').values('nome', 'prezzo')[:5]
>>> più_costosi
<QuerySet [
    {'nome': 'Frigorifero Smart',      'prezzo': Decimal('1499.00')},
    {'nome': 'Laptop Pro 15',          'prezzo': Decimal('1299.50')},
    {'nome': 'Smartphone Galaxy S24',  'prezzo': Decimal('899.99')},
    {'nome': 'Macchina Fotografica',   'prezzo': Decimal('849.00')},
    {'nome': 'Macchina per Caffè',     'prezzo': Decimal('799.00')}
]>
```

[↑ Torna all'indice](#indice)
