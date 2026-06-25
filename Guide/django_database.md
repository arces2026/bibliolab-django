# 🗄️ Database in Django — Guida Completa

Dalla configurazione iniziale ai dump selettivi e al ripristino dei dati.

---

## Indice

1. [Configurazione del Database](#1-configurazione-del-database)
2. [Migrazioni](#2-migrazioni)
3. [ORM — Interazione con il Database](#3-orm--interazione-con-il-database)
4. [Django Shell](#4-django-shell)
5. [Dump dei Dati](#5-dump-dei-dati)
6. [Dump Selettivi](#6-dump-selettivi)
7. [Ripristino dei Dump](#7-ripristino-dei-dump)
8. [Backup Automatizzato](#8-backup-automatizzato)
9. [Comandi Utili di Riepilogo](#9-comandi-utili-di-riepilogo)

---

## 1. Configurazione del Database

La configurazione del database si trova in `settings.py`, sotto la chiave `DATABASES`.

### SQLite (default)

Ideale per sviluppo locale. Non richiede installazione di software aggiuntivo.

```python
# settings.py
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```

### PostgreSQL

```bash
pip install psycopg2-binary
```

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'nome_database',
        'USER': 'utente',
        'PASSWORD': 'password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

### MySQL / MariaDB

```bash
pip install mysqlclient
```

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'nome_database',
        'USER': 'utente',
        'PASSWORD': 'password',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
```

### Configurazione tramite variabili d'ambiente

È buona pratica non hardcodare le credenziali. Usando `django-environ`:

```bash
pip install django-environ
```

```python
# settings.py
import environ

env = environ.Env()
environ.Env.read_env(BASE_DIR / '.env')

DATABASES = {
    'default': env.db('DATABASE_URL')
}
```

```env
# .env
DATABASE_URL=postgres://utente:password@localhost:5432/nome_database
```

### Database multipli

Django supporta più database contemporaneamente:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'db_principale',
        ...
    },
    'analytics': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'db_analytics',
        ...
    }
}
```

Per usare un database specifico in una query:

```python
MyModel.objects.using('analytics').all()
```

---

## 2. Migrazioni

Le migrazioni traducono i modelli Python in tabelle del database e ne tracciano l'evoluzione nel tempo.

### Comandi principali

```bash
# Crea i file di migrazione a partire dai modelli modificati
python manage.py makemigrations

# Applica le migrazioni pendenti al database
python manage.py migrate

# Applica le migrazioni di una singola app
python manage.py migrate nome_app

# Mostra lo stato delle migrazioni (✓ = applicata)
python manage.py showmigrations

# Mostra l'SQL che verrebbe eseguito, senza applicarlo
python manage.py sqlmigrate nome_app 0001
```

### Rollback di una migrazione

Per tornare a una migrazione precedente, specifica il numero della migrazione target:

```bash
# Torna alla migrazione 0002 (le successive vengono annullate)
python manage.py migrate nome_app 0002

# Annulla tutte le migrazioni di un'app
python manage.py migrate nome_app zero
```

### Migrazione vuota (per logica custom)

```bash
python manage.py makemigrations --empty nome_app
```

```python
# La migrazione generata può contenere RunPython per logica personalizzata
from django.db import migrations

def popola_dati(apps, schema_editor):
    MyModel = apps.get_model('nome_app', 'MyModel')
    MyModel.objects.create(nome='Default')

class Migration(migrations.Migration):
    dependencies = [('nome_app', '0003_auto')]
    operations = [
        migrations.RunPython(popola_dati),
    ]
```

---

## 3. ORM — Interazione con il Database

Django ORM permette di interrogare il database usando Python puro, senza scrivere SQL.

### Operazioni CRUD di base

```python
from myapp.models import Articolo

# CREATE
a = Articolo.objects.create(titolo='Primo post', pubblicato=True)

# READ — tutti i record
tutti = Articolo.objects.all()

# READ — con filtro
pubblicati = Articolo.objects.filter(pubblicato=True)
singolo = Articolo.objects.get(id=1)  # lancia eccezione se non esiste

# UPDATE
Articolo.objects.filter(id=1).update(titolo='Titolo aggiornato')

# DELETE
Articolo.objects.filter(pubblicato=False).delete()
```

### Lookup avanzati

```python
# Contiene (case-insensitive)
Articolo.objects.filter(titolo__icontains='django')

# Range di date
from datetime import date
Articolo.objects.filter(data__range=[date(2024, 1, 1), date(2024, 12, 31)])

# Relazioni (follow FK)
Commento.objects.filter(articolo__titolo__icontains='django')

# Esclusione
Articolo.objects.exclude(pubblicato=False)

# Ordinamento
Articolo.objects.order_by('-data_creazione')  # - = decrescente

# Limita risultati
Articolo.objects.all()[:10]
```

### Aggregazioni

```python
from django.db.models import Count, Avg, Sum, Max, Min

Articolo.objects.aggregate(totale=Count('id'))
Articolo.objects.values('categoria').annotate(num=Count('id'))
```

---

## 4. Django Shell

La shell interattiva permette di interrogare il database senza scrivere script separati.

```bash
python manage.py shell
```

Con `ipython` (interfaccia migliorata):

```bash
pip install ipython
python manage.py shell
```

Esempio di sessione:

```python
>>> from myapp.models import Articolo
>>> Articolo.objects.count()
42
>>> a = Articolo.objects.first()
>>> a.titolo
'Primo articolo'
>>> Articolo.objects.filter(pubblicato=True).count()
38
```

---

## 5. Dump dei Dati

`dumpdata` esporta i dati del database in formato JSON, XML o YAML.

### Dump completo

```bash
# JSON (default)
python manage.py dumpdata > dump_completo.json

# Con indentazione leggibile
python manage.py dumpdata --indent 2 > dump_completo.json

# Formato YAML (richiede pyyaml)
python manage.py dumpdata --format yaml > dump_completo.yaml

# Formato XML
python manage.py dumpdata --format xml > dump_completo.xml
```

### Escludere le tabelle di contenuto

È buona pratica escludere `contenttypes` e i permessi per evitare conflitti al ripristino:

```bash
python manage.py dumpdata \
  --exclude auth.permission \
  --exclude contenttypes \
  --indent 2 \
  > dump_pulito.json
```

---

## 6. Dump Selettivi

È possibile esportare solo parti specifiche del database.

### Dump di una singola app

```bash
# Tutti i modelli dell'app "blog"
python manage.py dumpdata blog --indent 2 > dump_blog.json
```

### Dump di un singolo modello

```bash
# Solo il modello Articolo
python manage.py dumpdata blog.Articolo --indent 2 > dump_articoli.json

# Solo il modello User
python manage.py dumpdata auth.User --indent 2 > dump_utenti.json
```

### Dump di più modelli specifici

```bash
python manage.py dumpdata blog.Articolo blog.Categoria --indent 2 > dump_blog_parziale.json
```

### Dump con filtro tramite fixture naturali

Le "natural keys" permettono di esportare dati con riferimenti leggibili invece di ID numerici. Definisci `natural_key` nel modello e usa `--natural-foreign`:

```python
# models.py
class Categoria(models.Model):
    slug = models.SlugField(unique=True)

    def natural_key(self):
        return (self.slug,)

    class Meta:
        pass

class CategoriaManager(models.Manager):
    def get_by_natural_key(self, slug):
        return self.get(slug=slug)
```

```bash
python manage.py dumpdata blog --natural-foreign --natural-primary --indent 2 > dump_naturale.json
```

### Dump verso database specifico

Se hai più database configurati:

```bash
python manage.py dumpdata --database analytics --indent 2 > dump_analytics.json
```

---

## 7. Ripristino dei Dump

`loaddata` importa i dati da un file di fixture nel database.

### Ripristino base

```bash
python manage.py loaddata dump_completo.json
```

### Ripristino di fixture specifiche

```bash
python manage.py loaddata dump_articoli.json
python manage.py loaddata dump_utenti.json
```

### Ripristino su database specifico

```bash
python manage.py loaddata dump_blog.json --database analytics
```

### Fixture automatiche con cartella `fixtures/`

Django cerca automaticamente le fixture nelle cartelle `fixtures/` delle app. Puoi posizionare i file lì e caricarli per nome:

```
myapp/
└── fixtures/
    ├── categorie.json
    └── articoli_iniziali.json
```

```bash
python manage.py loaddata categorie
python manage.py loaddata articoli_iniziali
```

### Procedura completa di ripristino su database vuoto

Questa è la sequenza consigliata quando si ripristina un ambiente da zero:

```bash
# 1. Applica le migrazioni (crea la struttura delle tabelle)
python manage.py migrate

# 2. Carica prima contenttypes e auth (se inclusi nel dump)
python manage.py loaddata dump_contenttypes.json
python manage.py loaddata dump_utenti.json

# 3. Carica i dati applicativi
python manage.py loaddata dump_blog.json

# oppure, se hai un dump unico pulito
python manage.py loaddata dump_pulito.json
```

> ⚠️ **Attenzione:** se il dump include `contenttypes` o `auth.permission`, potrebbero verificarsi conflitti di chiavi primarie su un database non vuoto. In quel caso, svuota prima le tabelle o usa `--exclude` al momento del dump.

### Svuotare il database prima del ripristino

```bash
# Elimina e ricrea tutte le tabelle
python manage.py flush

# Oppure, per un reset completo con riapplicazione delle migrazioni
python manage.py migrate --run-syncdb
```

---

## 8. Backup Automatizzato

### Script bash per backup periodici

```bash
#!/bin/bash
# backup.sh

DATE=$(date +%Y%m%d_%H%M%S)
OUTPUT="backups/dump_$DATE.json"

mkdir -p backups

python manage.py dumpdata \
  --exclude auth.permission \
  --exclude contenttypes \
  --indent 2 \
  > "$OUTPUT"

echo "Backup salvato in $OUTPUT"

# Elimina backup più vecchi di 30 giorni
find backups/ -name "*.json" -mtime +30 -delete
```

Rendi lo script eseguibile e schedulalo con cron:

```bash
chmod +x backup.sh

# Esegui ogni giorno alle 02:00
crontab -e
# Aggiungi:
# 0 2 * * * /path/to/progetto/backup.sh
```

### django-dbbackup (libreria dedicata)

Per un backup più robusto con supporto a S3, FTP, ecc.:

```bash
pip install django-dbbackup
```

```python
# settings.py
INSTALLED_APPS += ['dbbackup']
DBBACKUP_STORAGE = 'django.core.files.storage.FileSystemStorage'
DBBACKUP_STORAGE_OPTIONS = {'location': '/var/backups/django/'}
```

```bash
# Backup del database
python manage.py dbbackup

# Ripristino
python manage.py dbrestore
```

---

## 9. Comandi Utili di Riepilogo

| Operazione | Comando |
|---|---|
| Applica migrazioni | `python manage.py migrate` |
| Crea migrazioni | `python manage.py makemigrations` |
| Stato migrazioni | `python manage.py showmigrations` |
| Rollback app a zero | `python manage.py migrate nome_app zero` |
| Dump completo | `python manage.py dumpdata --indent 2 > dump.json` |
| Dump singola app | `python manage.py dumpdata nome_app --indent 2 > dump.json` |
| Dump singolo modello | `python manage.py dumpdata app.Modello --indent 2 > dump.json` |
| Dump senza permessi | `python manage.py dumpdata --exclude auth.permission --exclude contenttypes --indent 2 > dump.json` |
| Ripristino dump | `python manage.py loaddata dump.json` |
| Svuota database | `python manage.py flush` |
| Shell interattiva | `python manage.py shell` |

---

> 💡 **Tip:** per ambienti di produzione, preferisci i tool nativi del database (`pg_dump` per PostgreSQL, `mysqldump` per MySQL) per backup più veloci e completi. Usa `dumpdata` principalmente per spostare dati tra ambienti o per fixture di test.
