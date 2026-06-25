# 🔗 URLs in Django — Guida Completa

Routing, pattern, namespace, URL inversi e best practice.

---

## Indice

1. [Come funziona il routing](#1-come-funziona-il-routing)
2. [Configurazione base — urlpatterns](#2-configurazione-base--urlpatterns)
3. [Parametri nelle URL](#3-parametri-nelle-url)
4. [include() — URL per app](#4-include--url-per-app)
5. [Namespace e URL inversi](#5-namespace-e-url-inversi)
6. [URL inversi nelle view e nei template](#6-url-inversi-nelle-view-e-nei-template)
7. [Converter personalizzati](#7-converter-personalizzati)
8. [URL con regex — re_path()](#8-url-con-regex--re_path)
9. [Gestione degli errori HTTP](#9-gestione-degli-errori-http)
10. [URL per file statici e media](#10-url-per-file-statici-e-media)
11. [Riepilogo dei Comandi](#11-riepilogo-e-cheat-sheet)

---

## 1. Come funziona il routing

Quando Django riceve una richiesta HTTP, scorre la lista `urlpatterns` dall'alto verso il basso e si ferma al **primo pattern che corrisponde** all'URL richiesta. La view associata a quel pattern viene quindi eseguita.

Il file di routing principale è indicato in `settings.py`:

```python
# settings.py
ROOT_URLCONF = 'nome_progetto.urls'
```

Il flusso completo di una richiesta:

```
Richiesta HTTP
      ↓
  settings.py → ROOT_URLCONF
      ↓
  nome_progetto/urls.py → urlpatterns
      ↓
  (eventuale include) → myapp/urls.py
      ↓
  View → risposta HTTP
```

---

## 2. Configurazione base — urlpatterns

### Struttura minimale

```python
# nome_progetto/urls.py
from django.contrib import admin
from django.urls import path
from myapp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.homepage, name='homepage'),
    path('chi-siamo/', views.chi_siamo, name='chi-siamo'),
    path('contatti/', views.contatti, name='contatti'),
]
```

### La funzione path()

```python
path(route, view, kwargs=None, name=None)
```

| Parametro | Descrizione |
|---|---|
| `route` | Stringa dell'URL da abbinare (senza dominio e slash iniziale) |
| `view` | Funzione o classe view da chiamare |
| `kwargs` | Dizionario di argomenti extra da passare alla view |
| `name` | Nome univoco dell'URL, usato per gli URL inversi |

---

## 3. Parametri nelle URL

Django permette di catturare parti dell'URL come parametri e passarli automaticamente alla view.

### Converter built-in

```python
urlpatterns = [
    # int — numero intero positivo
    path('articoli/<int:id>/', views.dettaglio_articolo, name='articolo-dettaglio'),

    # str — qualsiasi stringa senza slash (default)
    path('categorie/<str:slug>/', views.categoria, name='categoria'),

    # slug — lettere, numeri, trattini e underscore
    path('post/<slug:slug>/', views.post, name='post-dettaglio'),

    # uuid — UUID nel formato standard
    path('ordini/<uuid:order_id>/', views.ordine, name='ordine-dettaglio'),

    # path — stringa che può contenere slash
    path('files/<path:percorso>/', views.file_view, name='file'),
]
```

| Converter | Corrisponde a | Tipo Python |
|---|---|---|
| `int` | Uno o più cifre | `int` |
| `str` | Qualsiasi stringa senza `/` | `str` |
| `slug` | Lettere, numeri, `-`, `_` | `str` |
| `uuid` | UUID formattato | `uuid.UUID` |
| `path` | Qualsiasi stringa, incluso `/` | `str` |

### View che riceve il parametro

```python
# views.py
def dettaglio_articolo(request, id):
    articolo = get_object_or_404(Articolo, pk=id)
    return render(request, 'articolo.html', {'articolo': articolo})

def post(request, slug):
    post = get_object_or_404(Post, slug=slug)
    return render(request, 'post.html', {'post': post})
```

### Parametri multipli

```python
urlpatterns = [
    path('blog/<int:anno>/<int:mese>/<slug:slug>/', views.archivio, name='archivio'),
]
```

```python
def archivio(request, anno, mese, slug):
    ...
```

### kwargs extra — argomenti statici

```python
urlpatterns = [
    path('bozze/', views.lista_articoli, {'pubblicato': False}, name='bozze'),
    path('pubblicati/', views.lista_articoli, {'pubblicato': True}, name='pubblicati'),
]
```

```python
def lista_articoli(request, pubblicato):
    articoli = Articolo.objects.filter(pubblicato=pubblicato)
    ...
```

---

## 4. include() — URL per app

Per mantenere il codice organizzato, ogni app dovrebbe avere il proprio file `urls.py`. Il file principale del progetto le include con `include()`.

### urls.py dell'app

```python
# myapp/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista, name='lista'),
    path('<int:id>/', views.dettaglio, name='dettaglio'),
    path('nuovo/', views.crea, name='crea'),
    path('<int:id>/modifica/', views.modifica, name='modifica'),
    path('<int:id>/elimina/', views.elimina, name='elimina'),
]
```

### urls.py del progetto

```python
# nome_progetto/urls.py
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('articoli/', include('myapp.urls')),
    path('utenti/', include('accounts.urls')),
    path('api/', include('api.urls')),
]
```

Le URL risultanti saranno:

```
/articoli/              → lista
/articoli/42/           → dettaglio con id=42
/articoli/nuovo/        → crea
/articoli/42/modifica/  → modifica con id=42
/articoli/42/elimina/   → elimina con id=42
```

### include() con una lista inline

```python
extra_patterns = [
    path('report/', views.report, name='report'),
    path('charge/', views.charge, name='charge'),
]

urlpatterns = [
    path('clienti/<int:pk>/', include(extra_patterns)),
]
```

---

## 5. Namespace e URL inversi

I **namespace** evitano collisioni tra nomi di URL appartenenti ad app diverse.

### Definire il namespace nell'app

```python
# myapp/urls.py
from django.urls import path
from . import views

app_name = 'blog'  # definisce il namespace

urlpatterns = [
    path('', views.lista, name='lista'),
    path('<slug:slug>/', views.dettaglio, name='dettaglio'),
]
```

### Includere con namespace nel progetto

```python
# nome_progetto/urls.py
urlpatterns = [
    path('blog/', include('blog.urls')),           # usa app_name definito nell'app
    path('negozio/', include('shop.urls')),
]
```

In alternativa, il namespace può essere dichiarato nell'include:

```python
path('blog/', include(('blog.urls', 'blog'))),
```

### Riferirsi agli URL con namespace

La sintassi è sempre `namespace:nome_url`:

```python
# In Python
from django.urls import reverse
url = reverse('blog:dettaglio', kwargs={'slug': 'il-mio-post'})
```

```django
{# In un template Django #}
{% url 'blog:lista' %}
{% url 'blog:dettaglio' slug=post.slug %}
```

---

## 6. URL inversi nelle view e nei template

Costruire URL a partire dal nome evita di hardcodare i percorsi nel codice.

### reverse() nelle view

```python
from django.urls import reverse
from django.shortcuts import redirect

def crea_articolo(request):
    # ... salva l'articolo
    return redirect(reverse('blog:dettaglio', kwargs={'slug': articolo.slug}))
```

### reverse_lazy() — per contesti di caricamento ritardato

Utile nei class-based view e nella configurazione a livello di modulo:

```python
from django.urls import reverse_lazy
from django.views.generic.edit import DeleteView

class ArticoloDeleteView(DeleteView):
    model = Articolo
    success_url = reverse_lazy('blog:lista')
```

### get_absolute_url() nel modello

Un pattern Django idiomatico: definire il proprio URL direttamente nel modello.

```python
# models.py
from django.urls import reverse

class Articolo(models.Model):
    titolo = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)

    def get_absolute_url(self):
        return reverse('blog:dettaglio', kwargs={'slug': self.slug})
```

Nei template:

```django
<a href="{{ articolo.get_absolute_url }}">{{ articolo.titolo }}</a>
```

### Tag {% url %} nei template

```django
{# URL senza parametri #}
<a href="{% url 'blog:lista' %}">Tutti gli articoli</a>

{# URL con parametro posizionale #}
<a href="{% url 'blog:dettaglio' post.slug %}">Leggi</a>

{# URL con parametro keyword #}
<a href="{% url 'archivio' anno=2024 mese=6 %}">Giugno 2024</a>

{# Salva l'URL in una variabile #}
{% url 'blog:lista' as url_lista %}
<a href="{{ url_lista }}">Lista</a>
```

---

## 7. Converter personalizzati

Puoi definire converter custom per gestire tipi di parametri non coperti da quelli built-in.

```python
# myapp/converters.py

class FourDigitYearConverter:
    regex = '[0-9]{4}'  # pattern regex da abbinare

    def to_python(self, value):
        return int(value)

    def to_url(self, value):
        return f'{value:04d}'
```

```python
# myapp/urls.py
from django.urls import path, register_converter
from . import converters, views

register_converter(converters.FourDigitYearConverter, 'yyyy')

urlpatterns = [
    path('archivio/<yyyy:anno>/', views.archivio_anno, name='archivio-anno'),
]
```

---

## 8. URL con regex — re_path()

Per pattern più complessi, usa `re_path()` con espressioni regolari.

```python
from django.urls import re_path
from . import views

urlpatterns = [
    # Cattura un anno a 4 cifre
    re_path(r'^articoli/(?P<anno>[0-9]{4})/$', views.archivio, name='archivio'),

    # Slug con lunghezza limitata
    re_path(r'^post/(?P<slug>[\w-]{3,50})/$', views.post, name='post'),

    # Formato data YYYY-MM-DD
    re_path(
        r'^eventi/(?P<data>\d{4}-\d{2}-\d{2})/$',
        views.eventi_del_giorno,
        name='eventi-giorno'
    ),
]
```

> ⚠️ Preferisci sempre `path()` con i converter built-in quando possibile. Usa `re_path()` solo per casi che i converter non coprono.

---

## 9. Gestione degli errori HTTP

Django permette di personalizzare le pagine di errore definendo handler specifici nel file `urls.py` principale.

### Definire handler custom

```python
# nome_progetto/urls.py
from django.conf.urls import handler400, handler403, handler404, handler500
from myapp import views

handler400 = views.errore_400  # Bad Request
handler403 = views.errore_403  # Forbidden
handler404 = views.errore_404  # Not Found
handler500 = views.errore_500  # Server Error
```

### View degli errori

```python
# views.py
def errore_404(request, exception):
    return render(request, 'errors/404.html', status=404)

def errore_500(request):
    return render(request, 'errors/500.html', status=500)
```

> Le pagine di errore custom sono attive solo con `DEBUG = False` in `settings.py`.

---

## 10. URL per file statici e media

### File statici in sviluppo

Django serve i file statici automaticamente in sviluppo. Nessuna configurazione extra nelle URL è necessaria se `django.contrib.staticfiles` è in `INSTALLED_APPS`.

```python
# settings.py
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'  # usato da collectstatic
```

### File media in sviluppo

Per servire i file caricati dagli utenti in sviluppo, aggiungi al file `urls.py` del progetto:

```python
# nome_progetto/urls.py
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('myapp.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

```python
# settings.py
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
```

> ⚠️ `static()` aggiunge le URL **solo se `DEBUG = True`**. In produzione, i file media devono essere serviti dal web server (nginx, Apache, S3, ecc.).

---

## 11. Riepilogo e Cheat Sheet

### Tipi di URL a confronto

```python
from django.urls import path, re_path, include

urlpatterns = [
    # Statica
    path('home/', views.home, name='home'),

    # Con parametro intero
    path('item/<int:pk>/', views.item, name='item'),

    # Con slug
    path('post/<slug:slug>/', views.post, name='post'),

    # Con namespace
    path('blog/', include('blog.urls')),  # app_name = 'blog' in blog/urls.py

    # Con regex
    re_path(r'^legacy/(?P<id>\d+)/$', views.legacy, name='legacy'),

    # Con kwargs statici
    path('bozze/', views.lista, {'pubblicato': False}, name='bozze'),
]
```

### URL inversi a confronto

| Contesto | Sintassi |
|---|---|
| View Python | `reverse('blog:dettaglio', kwargs={'slug': 'testo'})` |
| View (redirect) | `redirect('blog:lista')` |
| View lazy | `reverse_lazy('blog:lista')` |
| Template | `{% url 'blog:dettaglio' slug=post.slug %}` |
| Modello | `def get_absolute_url(self): return reverse(...)` |

### Struttura consigliata dei file URL

```
nome_progetto/
├── nome_progetto/
│   └── urls.py          ← ROOT_URLCONF: include le app
├── blog/
│   └── urls.py          ← app_name = 'blog'
├── accounts/
│   └── urls.py          ← app_name = 'accounts'
└── api/
    └── urls.py          ← app_name = 'api'
```

---

> 💡 **Best practice:** usa sempre `name=` su ogni `path()` e accedi alle URL tramite `reverse()` o `{% url %}`. Evita di scrivere URL hardcodate nel codice: se il percorso cambia, basta aggiornare `urls.py` e il resto si adatta automaticamente.
