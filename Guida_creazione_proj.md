# 🐍 Guida alla Creazione di un Progetto Django

Questa guida descrive il flow completo per avviare un progetto Django da zero, partendo dalla creazione dell'ambiente virtuale fino all'avvio del server di sviluppo.

---

## Prerequisiti

- Python 3.10+ installato
- `pip` aggiornato
- Accesso al terminale

Verifica la versione di Python:

```bash
python --version
# oppure
python3 --version
```

---

## 1. Creazione del Virtual Environment

Il virtual environment isola le dipendenze del progetto dal sistema globale.

```bash
# Crea il venv nella cartella del progetto
python -m venv venv
```

> La cartella `venv/` conterrà l'interprete Python e i pacchetti installati localmente.

---

## 2. Attivazione del Virtual Environment

**macOS / Linux:**

```bash
source venv/bin/activate
```

**Windows (CMD):**

```bash
venv\Scripts\activate.bat
```

**Bash (in windows):**

```bash
source .venv/Script/activate
```

**Windows (PowerShell):**

```bash
venv\Scripts\Activate.ps1
```

Quando il venv è attivo, il prompt del terminale mostrerà il prefisso `(venv)`.

---

## 3. Installazione di Django

Con il venv attivo, installa Django tramite pip:

```bash
pip install django
```

Per installare una versione specifica:

```bash
pip install django==5.0
```

Verifica l'installazione:

```bash
django-admin --version
```

---

## 4. Creazione del Progetto Django

```bash
django-admin startproject nome_progetto .
```

> Il `.` finale crea i file nella directory corrente, evitando una cartella annidata.

Struttura generata:

```
.
├── manage.py
├── nome_progetto/
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
└── venv/
```

---

## 5. Creazione di un'App Django

Un progetto Django è composto da una o più **app**, ognuna responsabile di una funzionalità specifica.

```bash
python manage.py startapp nome_app
```

Struttura generata:

```
nome_app/
├── __init__.py
├── admin.py
├── apps.py
├── migrations/
│   └── __init__.py
├── models.py
├── tests.py
└── views.py
```

### Registra l'app nel progetto

Apri `nome_progetto/settings.py` e aggiungi l'app a `INSTALLED_APPS`:

```python
INSTALLED_APPS = [
    # App di default Django
    'django.contrib.admin',
    'django.contrib.auth',
    ...
    # La tua app
    'nome_app',
]
```

---

## 6. Configurazione del Database

Django usa **SQLite** di default. Per usarlo senza modifiche, salta questo step.

Per configurare PostgreSQL, modifica `settings.py`:

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

---

## 7. Esecuzione delle Migrazioni

Le migrazioni sincronizzano i modelli con il database.

```bash
# Crea i file di migrazione
python manage.py makemigrations

# Applica le migrazioni al database
python manage.py migrate
```

---

## 8. Creazione del Superuser

Per accedere all'interfaccia di amministrazione di Django:

```bash
python manage.py createsuperuser
```

Inserisci username, email e password quando richiesto.

---

## 9. Avvio del Server di Sviluppo

```bash
python manage.py runserver
```

Il server sarà disponibile su `http://127.0.0.1:8000/`.

L'interfaccia di admin è raggiungibile su `http://127.0.0.1:8000/admin/`.

Per usare una porta diversa:

```bash
python manage.py runserver 8080
```

---

## 10. Salvataggio delle Dipendenze

Genera il file `requirements.txt` per condividere le dipendenze del progetto:

```bash
pip freeze > requirements.txt
```

Per installare le dipendenze su un altro ambiente:

```bash
pip install -r requirements.txt
```

---

## Riepilogo dei Comandi

| Step | Comando |
|------|---------|
| Crea venv | `python -m venv venv` |
| Attiva venv (Mac/Linux) | `source venv/bin/activate` |
| Installa Django | `pip install django` |
| Crea progetto | `django-admin startproject nome_progetto .` |
| Crea app | `python manage.py startapp nome_app` |
| Migra database | `python manage.py migrate` |
| Crea superuser | `python manage.py createsuperuser` |
| Avvia server | `python manage.py runserver` |
| Salva dipendenze | `pip freeze > requirements.txt` |

---

## .gitignore consigliato

Aggiungi questo `.gitignore` alla root del progetto per escludere file non necessari dal repository:

```gitignore
# Virtual environment
venv/
env/

# Django
*.pyc
__pycache__/
db.sqlite3
*.log
media/

# Environment variables
.env

# IDE
.vscode/
.idea/
```

---

> 💡 **Tip:** usa `python-dotenv` o `django-environ` per gestire le variabili d'ambiente sensibili (chiavi segrete, credenziali database) tramite un file `.env`.
