# Esempi vari

## CRUD dalla shell python di Django

CREATE

```shell
$ py manage.py shell
13 objects imported automatically (use -v 2 for details).

Ctrl click to launch VS Code Native REPL
Python 3.14.6 (tags/v3.14.6:c63aec6, Jun 10 2026, 10:26:10) [MSC v.1944 64 bit (AMD64)] on win32
Type "help", "copyright", "credits" or "license" for more information.
(InteractiveConsole)

# Metodo 1: istanza + save()
>>> from catalogo.models import Prodotto
>>> nuovo_libro = Libro(
...     titolo="Il Nome della Rosa",
...     autore="Umberto Eco",
...     anno_pubblicazione=1980
)
libro.save()

# Metodo 2: create() in un solo passaggio (preferibile)
 
>>> nuovo_libro = Prodotto.objects.create(
...     titolo='Il Nome della Rosa',
...     autore='Umberto Eco',
...     disponibile=True,
...     anno_pubblicazione='1980'
... )
```

READ

```shell
$ py manage.py shell
>>> from catalogo.models import Prodotto
>>> tutti_i_libri = Prodotto.objects.all()
<QuerySet [<Prodotto: Il Nome della Rosa di Umberto>]>
```

UPDATE

```shell
$ py manage.py shell
# get() + save()
>>> libro = Libro.objects.get(id=1)
...     libro.disponibile = False
...     libro.save()

# update() più efficiente
>>> from catalogo.models import Prodotto
>>> Prodotto.objects.filter(id=1).update(
        disponibile = False
)
```

DELETE

```shell
$ py manage.py shell
# Elimina tutti
>>> from catalogo.models import Prodotto
>>> Prodotto.objects.all().delete()
(1, {'catalogo.Prodotto': 1})

# Elimina libri prima del 1950
>>> Libro.objects.filter(
...     anno_pubblicazione__lt=1950
...).delete()
# __lt = "less than" (minore di)
```

CREATE (bulk)

```shell
$ py manage.py shell
>>> from catalogo.models import Prodotto
>>> 
>>> libri = [
...     Prodotto(titolo="Il Nome della Rosa", autore="Umberto Eco", anno_pubblicazione=1980),
...     Prodotto(titolo="Se questo è un uomo", autore="Primo Levi", anno_pubblicazione=1947),
...     Prodotto(titolo="I Promessi Sposi", autore="Alessandro Manzoni", anno_pubblicazione=1827),
...     Prodotto(titolo="L'Alchimista", autore="Paulo Coelho", anno_pubblicazione=1988),
...     Prodotto(titolo="Harry Potter e la pietra filosofale", autore="J.K. Rowling", anno_pubblicazione=1997)),
...     Prodotto(titolo="Il codice da Vinci", autore="Dan Brown", anno_pubblicazione=2003)),
...     Prodotto(titolo="Neuromante", autore="William Gibson", anno_pubblicazione=1984),
... ]
>>> 
>>> Prodotto.objects.bulk_create(libri)
print(f"Creati {Prodotto.objects.count()} prodotti.")
```
