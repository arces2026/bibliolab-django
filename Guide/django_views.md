# 👁️ Views in Django — Guida Completa

Function-based views, class-based views, generic views e best practice.

---

## Indice

1. [Cosa è una View](#1-cosa-è-una-view)
2. [Function-Based Views (FBV)](#2-function-based-views-fbv)
3. [Request e Response](#3-request-e-response)
4. [Shortcuts utili](#4-shortcuts-utili)
5. [Class-Based Views (CBV)](#5-class-based-views-cbv)
6. [Generic Display Views](#6-generic-display-views)
7. [Generic Editing Views](#7-generic-editing-views)
8. [Mixins](#8-mixins)
9. [Decoratori](#9-decoratori)
10. [Gestione di form nelle view](#10-gestione-di-form-nelle-view)
11. [View per API — JsonResponse](#11-view-per-api--jsonresponse)
12. [FBV vs CBV — confronto](#12-fbv-vs-cbv--confronto)
13. [Cheat Sheet](#13-cheat-sheet)

---

## 1. Cosa è una View

Una **view** in Django è una funzione (o una classe) che riceve una `HttpRequest` e restituisce una `HttpResponse`. È il layer che contiene la **logica applicativa**: recupera dati, li elabora e decide cosa restituire al client.

```
URL → View → (Model + Template) → HttpResponse
```

Ogni view deve:
- Accettare almeno il parametro `request`
- Restituire un oggetto `HttpResponse` (o una sua sottoclasse)

---

## 2. Function-Based Views (FBV)

Le FBV sono semplici funzioni Python. Sono dirette, esplicite e facili da leggere.

### View minimale

```python
# views.py
from django.http import HttpResponse

def hello(request):
    return HttpResponse("Ciao, mondo!")
```

### View con template

```python
from django.shortcuts import render

def homepage(request):
    contesto = {
        'titolo': 'Benvenuto',
        'anno': 2024,
    }
    return render(request, 'homepage.html', contesto)
```

### View con metodo HTTP

```python
def contatti(request):
    if request.method == 'POST':
        # elabora il form
        nome = request.POST.get('nome')
        return HttpResponse(f"Grazie, {nome}!")
    else:
        # mostra il form vuoto
        return render(request, 'contatti.html')
```

### View con parametri dall'URL

```python
def dettaglio_articolo(request, slug):
    articolo = get_object_or_404(Articolo, slug=slug)
    return render(request, 'articolo/dettaglio.html', {'articolo': articolo})
```

---

## 3. Request e Response

### L'oggetto HttpRequest

Django passa automaticamente l'oggetto `request` ad ogni view. Contiene tutte le informazioni sulla richiesta in arrivo.

```python
def mia_view(request):
    # Metodo HTTP
    request.method          # 'GET', 'POST', 'PUT', 'DELETE', ...

    # Dati inviati
    request.GET             # QueryDict con parametri GET (?chiave=valore)
    request.POST            # QueryDict con dati del form POST
    request.FILES           # File caricati
    request.body            # Body grezzo della richiesta (bytes)

    # Utente
    request.user            # Utente autenticato (o AnonymousUser)
    request.user.is_authenticated  # True/False

    # Sessione
    request.session         # Dizionario della sessione corrente

    # Metadati
    request.META            # Dizionario con header HTTP e info server
    request.META['HTTP_USER_AGENT']
    request.META['REMOTE_ADDR']  # IP del client

    # URL
    request.path            # '/articoli/il-mio-post/'
    request.get_full_path() # '/articoli/il-mio-post/?pagina=2'
    request.build_absolute_uri()  # 'https://esempio.com/articoli/...'
```

### Tipi di HttpResponse

```python
from django.http import (
    HttpResponse,
    HttpResponseRedirect,
    HttpResponsePermanentRedirect,
    HttpResponseNotFound,
    HttpResponseForbidden,
    HttpResponseServerError,
    JsonResponse,
    FileResponse,
    StreamingHttpResponse,
)

# Risposta base
HttpResponse("Testo", content_type="text/plain", status=200)

# Redirect temporaneo (302)
HttpResponseRedirect('/nuova/url/')

# Redirect permanente (301)
HttpResponsePermanentRedirect('/nuova/url/')

# Errori
HttpResponseNotFound('<h1>404</h1>')
HttpResponseForbidden()
HttpResponseServerError()

# JSON
JsonResponse({'chiave': 'valore'})

# File
FileResponse(open('documento.pdf', 'rb'), content_type='application/pdf')
```

---

## 4. Shortcuts utili

Django fornisce funzioni di convenienza nel modulo `django.shortcuts`.

```python
from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
```

### render()

Combina un template con un contesto e restituisce un `HttpResponse`.

```python
return render(request, 'template.html', {'chiave': valore}, status=200)
```

### redirect()

Genera un redirect verso un URL, un nome di URL o un oggetto con `get_absolute_url()`.

```python
# Verso URL stringa
return redirect('/articoli/')

# Verso nome URL
return redirect('blog:lista')

# Verso nome URL con parametri
return redirect('blog:dettaglio', slug=articolo.slug)

# Verso un oggetto modello (chiama get_absolute_url())
return redirect(articolo)

# Redirect permanente
return redirect('blog:lista', permanent=True)
```

### get_object_or_404()

Recupera un oggetto o restituisce 404 se non esiste. Evita il try/except manuale.

```python
# Con pk
articolo = get_object_or_404(Articolo, pk=id)

# Con più filtri
articolo = get_object_or_404(Articolo, slug=slug, pubblicato=True)

# Con queryset
articolo = get_object_or_404(Articolo.objects.filter(autore=request.user), pk=id)
```

### get_list_or_404()

Come `get_object_or_404`, ma per liste. Restituisce 404 se la lista è vuota.

```python
articoli = get_list_or_404(Articolo, categoria=categoria)
```

---

## 5. Class-Based Views (CBV)

Le CBV organizzano la logica in classi, sfruttando l'ereditarietà per riutilizzare il codice.

### View base

```python
from django.views import View

class HomepageView(View):
    def get(self, request):
        return render(request, 'homepage.html')

    def post(self, request):
        # gestisce POST
        return HttpResponse("POST ricevuto")
```

### Collegamento alle URL

```python
# urls.py
from django.urls import path
from .views import HomepageView

urlpatterns = [
    path('', HomepageView.as_view(), name='homepage'),
]
```

### Attributi e metodi comuni

```python
class MiaView(View):
    template_name = 'mia_template.html'  # template da usare
    extra_context = {'titolo': 'Pagina'}  # contesto aggiuntivo

    def setup(self, request, *args, **kwargs):
        """Chiamato prima di dispatch, per inizializzazioni."""
        super().setup(request, *args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        """Smista la richiesta al metodo corretto (get, post, ecc.)."""
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        """Costruisce il contesto del template."""
        context = super().get_context_data(**kwargs)
        context['extra'] = 'valore'
        return context
```

---

## 6. Generic Display Views

Django include CBV predefinite per operazioni comuni. Evitano di riscrivere codice ripetitivo.

### TemplateView — pagina statica

```python
from django.views.generic import TemplateView

class ChiSiamoView(TemplateView):
    template_name = 'chi_siamo.html'
    extra_context = {'titolo': 'Chi siamo'}
```

### ListView — lista di oggetti

```python
from django.views.generic import ListView
from .models import Articolo

class ArticoloListView(ListView):
    model = Articolo
    template_name = 'blog/lista.html'    # default: blog/articolo_list.html
    context_object_name = 'articoli'     # default: object_list
    paginate_by = 10                     # attiva paginazione
    ordering = ['-data_creazione']

    def get_queryset(self):
        """Personalizza il queryset."""
        return Articolo.objects.filter(pubblicato=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categorie'] = Categoria.objects.all()
        return context
```

Nel template:

```django
{% for articolo in articoli %}
    <h2>{{ articolo.titolo }}</h2>
{% endfor %}

{# Paginazione #}
{% if is_paginated %}
    {% if page_obj.has_previous %}
        <a href="?page={{ page_obj.previous_page_number }}">Precedente</a>
    {% endif %}
    <span>Pagina {{ page_obj.number }} di {{ page_obj.paginator.num_pages }}</span>
    {% if page_obj.has_next %}
        <a href="?page={{ page_obj.next_page_number }}">Successiva</a>
    {% endif %}
{% endif %}
```

### DetailView — dettaglio di un oggetto

```python
from django.views.generic import DetailView

class ArticoloDetailView(DetailView):
    model = Articolo
    template_name = 'blog/dettaglio.html'  # default: blog/articolo_detail.html
    context_object_name = 'articolo'       # default: object
    slug_field = 'slug'                    # campo del modello (default: 'slug')
    slug_url_kwarg = 'slug'                # parametro nell'URL (default: 'slug')

    def get_queryset(self):
        return Articolo.objects.filter(pubblicato=True)
```

URL corrispondente:

```python
path('post/<slug:slug>/', ArticoloDetailView.as_view(), name='dettaglio'),
```

---

## 7. Generic Editing Views

### CreateView — creazione di un oggetto

```python
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy

class ArticoloCreateView(CreateView):
    model = Articolo
    template_name = 'blog/form.html'
    fields = ['titolo', 'contenuto', 'categoria', 'pubblicato']
    success_url = reverse_lazy('blog:lista')

    def form_valid(self, form):
        """Chiamato quando il form è valido. Puoi modificare l'oggetto prima del salvataggio."""
        form.instance.autore = self.request.user
        return super().form_valid(form)
```

### UpdateView — modifica di un oggetto

```python
from django.views.generic.edit import UpdateView

class ArticoloUpdateView(UpdateView):
    model = Articolo
    template_name = 'blog/form.html'
    fields = ['titolo', 'contenuto', 'categoria', 'pubblicato']

    def get_success_url(self):
        return reverse_lazy('blog:dettaglio', kwargs={'slug': self.object.slug})
```

### DeleteView — eliminazione di un oggetto

```python
from django.views.generic.edit import DeleteView

class ArticoloDeleteView(DeleteView):
    model = Articolo
    template_name = 'blog/conferma_elimina.html'
    success_url = reverse_lazy('blog:lista')
```

Template di conferma:

```django
{# blog/conferma_elimina.html #}
<p>Sei sicuro di voler eliminare "{{ object.titolo }}"?</p>
<form method="post">
    {% csrf_token %}
    <button type="submit">Elimina</button>
    <a href="{% url 'blog:lista' %}">Annulla</a>
</form>
```

### FormView — form generico (senza modello)

```python
from django.views.generic.edit import FormView
from .forms import ContattiForm

class ContattiView(FormView):
    template_name = 'contatti.html'
    form_class = ContattiForm
    success_url = reverse_lazy('contatti-grazie')

    def form_valid(self, form):
        form.invia_email()  # logica custom
        return super().form_valid(form)
```

---

## 8. Mixins

I mixin sono classi riutilizzabili che aggiungono funzionalità alle CBV tramite ereditarietà multipla.

### LoginRequiredMixin — richiede autenticazione

```python
from django.contrib.auth.mixins import LoginRequiredMixin

class ArticoloCreateView(LoginRequiredMixin, CreateView):
    model = Articolo
    fields = ['titolo', 'contenuto']
    login_url = '/login/'           # default: settings.LOGIN_URL
    redirect_field_name = 'next'    # parametro GET per il redirect post-login
```

### PermissionRequiredMixin — richiede permessi specifici

```python
from django.contrib.auth.mixins import PermissionRequiredMixin

class ArticoloDeleteView(PermissionRequiredMixin, DeleteView):
    model = Articolo
    permission_required = 'blog.delete_articolo'
    # oppure più permessi:
    # permission_required = ['blog.change_articolo', 'blog.delete_articolo']
```

### UserPassesTestMixin — test personalizzato

```python
from django.contrib.auth.mixins import UserPassesTestMixin

class ArticoloUpdateView(UserPassesTestMixin, UpdateView):
    model = Articolo

    def test_func(self):
        articolo = self.get_object()
        return self.request.user == articolo.autore
```

### Mixin personalizzato

```python
class AutoreRequiredMixin:
    """Permette solo all'autore dell'oggetto di accedere alla view."""
    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.autore != request.user:
            return redirect('home')
        return super().dispatch(request, *args, **kwargs)

class ArticoloUpdateView(AutoreRequiredMixin, LoginRequiredMixin, UpdateView):
    model = Articolo
    fields = ['titolo', 'contenuto']
```

---

## 9. Decoratori

I decoratori aggiungono funzionalità alle FBV (e alle CBV tramite `method_decorator`).

### login_required

```python
from django.contrib.auth.decorators import login_required

@login_required
def area_riservata(request):
    return render(request, 'riservata.html')

# Con URL di login personalizzata
@login_required(login_url='/accedi/')
def profilo(request):
    ...
```

### permission_required

```python
from django.contrib.auth.decorators import permission_required

@permission_required('blog.add_articolo')
def crea_articolo(request):
    ...

# Con redirect su 404 invece del login
@permission_required('blog.add_articolo', raise_exception=True)
def crea_articolo(request):
    ...
```

### require_http_methods — limita i metodi HTTP

```python
from django.views.decorators.http import require_http_methods, require_GET, require_POST

@require_GET
def solo_get(request):
    ...

@require_POST
def solo_post(request):
    ...

@require_http_methods(['GET', 'POST'])
def get_o_post(request):
    ...
```

### cache_page — caching della risposta

```python
from django.views.decorators.cache import cache_page

@cache_page(60 * 15)  # cache per 15 minuti
def homepage(request):
    ...
```

### Decoratori sulle CBV

```python
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

@method_decorator(login_required, name='dispatch')
class ProfiloView(View):
    def get(self, request):
        ...
```

---

## 10. Gestione di form nelle view

### FBV con form

```python
from django import forms
from django.shortcuts import render, redirect

class ArticoloForm(forms.ModelForm):
    class Meta:
        model = Articolo
        fields = ['titolo', 'contenuto', 'pubblicato']

def crea_articolo(request):
    if request.method == 'POST':
        form = ArticoloForm(request.POST, request.FILES)
        if form.is_valid():
            articolo = form.save(commit=False)
            articolo.autore = request.user
            articolo.save()
            return redirect('blog:dettaglio', slug=articolo.slug)
    else:
        form = ArticoloForm()

    return render(request, 'blog/form.html', {'form': form})
```

### Template del form

```django
<form method="post" enctype="multipart/form-data">
    {% csrf_token %}
    {{ form.as_p }}
    <button type="submit">Salva</button>
</form>
```

### Gestione degli errori nel template

```django
{% if form.errors %}
    <div class="errori">
        {% for field in form %}
            {% for error in field.errors %}
                <p>{{ field.label }}: {{ error }}</p>
            {% endfor %}
        {% endfor %}
        {% for error in form.non_field_errors %}
            <p>{{ error }}</p>
        {% endfor %}
    </div>
{% endif %}
```

---

## 11. View per API — JsonResponse

Per restituire dati JSON senza librerie esterne.

```python
from django.http import JsonResponse
from django.views.decorators.http import require_GET
from django.views import View
import json

# FBV
@require_GET
def api_articoli(request):
    articoli = list(
        Articolo.objects.filter(pubblicato=True).values('id', 'titolo', 'slug')
    )
    return JsonResponse({'articoli': articoli})

# Con status personalizzato
def api_crea(request):
    if request.method != 'POST':
        return JsonResponse({'errore': 'Metodo non consentito'}, status=405)

    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'errore': 'JSON non valido'}, status=400)

    articolo = Articolo.objects.create(
        titolo=data.get('titolo'),
        autore=request.user,
    )
    return JsonResponse({'id': articolo.id, 'titolo': articolo.titolo}, status=201)

# CBV per API
class ArticoloApiView(View):
    def get(self, request, pk):
        articolo = get_object_or_404(Articolo, pk=pk)
        return JsonResponse({
            'id': articolo.id,
            'titolo': articolo.titolo,
            'slug': articolo.slug,
        })

    def delete(self, request, pk):
        articolo = get_object_or_404(Articolo, pk=pk)
        articolo.delete()
        return JsonResponse({'eliminato': True}, status=204)
```

> 💡 Per API più strutturate, considera **Django REST Framework (DRF)**, che aggiunge serializzatori, autenticazione token, viewset e molto altro.

---

## 12. FBV vs CBV — confronto

| Caratteristica | FBV | CBV |
|---|---|---|
| Leggibilità | Alta per logica semplice | Alta per pattern standard |
| Flessibilità | Totale | Alta tramite override |
| Riutilizzo | Tramite funzioni helper | Tramite ereditarietà e mixin |
| Boilerplate | Minimo | Ridotto dalle generic view |
| Curva di apprendimento | Bassa | Media |
| Ideale per | Logica custom, API semplici | CRUD standard, pattern ripetitivi |

### Quando usare le FBV

- Logica complessa e molto specifica
- View con molte condizioni diverse
- Quando la semplicità e la leggibilità sono prioritarie
- Endpoint API semplici

### Quando usare le CBV

- Operazioni CRUD standard su modelli
- Quando hai molte view simili da riutilizzare
- Per sfruttare le generic view di Django
- Quando vuoi separare la logica per metodo HTTP (`get`, `post`, ecc.)

---

## 13. Cheat Sheet

### Generic Views — riferimento rapido

| View | Scopo | Template default |
|---|---|---|
| `TemplateView` | Pagina statica | — |
| `ListView` | Lista oggetti | `app/modello_list.html` |
| `DetailView` | Dettaglio oggetto | `app/modello_detail.html` |
| `CreateView` | Crea oggetto | `app/modello_form.html` |
| `UpdateView` | Modifica oggetto | `app/modello_form.html` |
| `DeleteView` | Elimina oggetto | `app/modello_confirm_delete.html` |
| `FormView` | Form senza modello | — |

### Mixins — riferimento rapido

| Mixin | Scopo |
|---|---|
| `LoginRequiredMixin` | Richiede login |
| `PermissionRequiredMixin` | Richiede permesso specifico |
| `UserPassesTestMixin` | Test logica custom |

### Decoratori — riferimento rapido

| Decoratore | Scopo |
|---|---|
| `@login_required` | Richiede login |
| `@permission_required` | Richiede permesso |
| `@require_GET` | Solo metodo GET |
| `@require_POST` | Solo metodo POST |
| `@require_http_methods([...])` | Metodi specifici |
| `@cache_page(secondi)` | Caching della risposta |

---

> 💡 **Best practice:** mantieni le view snelle. La logica di business pesante va nei modelli o in moduli di servizio separati (`services.py`). La view dovrebbe solo ricevere la richiesta, delegare l'elaborazione e restituire una risposta.
