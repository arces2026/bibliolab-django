# DUMP & LOAD — Guida al Backup e Ripristino Database Django con SQLite3

---

## Indice

1. [Dump dei Dati in JSON](#1-dump-dei-dati-in-json)
2. [Dump in Formato SQL](#2-dump-in-formato-sql)
3. [Dump in CSV](#3-dump-in-csv)
4. [Backup del File Database](#4-backup-del-file-database)
5. [Comando Personalizzato Django](#5-comando-personalizzato-django)
6. [Script per Backup Automatico](#6-script-per-backup-automatico)
7. [Cosa non Backupare](#7-cosa-non-backupare)
8. [Raccomandazioni Finali](#8-raccomandazioni-finali)

---

## 1. Dump dei Dati in JSON

### Esportazione (Dump)

```bash
# Dump di TUTTI i dati del progetto
python manage.py dumpdata > dump.json

# Dump di app specifiche
python manage.py dumpdata myapp > myapp_dump.json

# Dump di modelli specifici
python manage.py dumpdata myapp.Cliente myapp.Prodotto_new myapp.Ordine > ordini_dump.json

# Dump con indentazione per leggibilità
python manage.py dumpdata --indent 4 > dump.json

# Dump escludendo alcune app (esclude permessi e contenttypes)
python manage.py dumpdata --exclude auth.permission --exclude contenttypes > dump.json

# Dump solo dati di una specifica app con esclusione
python manage.py dumpdata myapp --exclude auth.permission > myapp_dump.json
```

### Importazione (Load)

```bash
# Carica un dump JSON
python manage.py loaddata dump.json

# Carica da file specifico
python manage.py loaddata myapp_dump.json

# Carica con esclusione di alcuni modelli
python manage.py loaddata dump.json --exclude myapp.Cliente
```

[↑ Torna all'indice](#indice)

---

## 2. Dump in Formato SQL

### Esportazione (Dump)

```bash
# Vai nella directory del progetto
cd project_directory

# Crea un dump SQL completo
sqlite3 db.sqlite3 .dump > dump.sql

# Con percorso completo
sqlite3 /path/to/your/db.sqlite3 .dump > backup.sql

# Dump di tabelle specifiche
sqlite3 db.sqlite3 "SELECT * FROM myapp_cliente;" > clienti.sql

# Dump solo schema (senza dati)
sqlite3 db.sqlite3 ".schema" > schema.sql

# Dump con formato leggibile in CSV
sqlite3 -header -csv db.sqlite3 "SELECT * FROM myapp_cliente;" > clienti.csv
```

### Importazione (Load)

```bash
# Crea nuovo database dal dump SQL
sqlite3 nuovo_db.sqlite3 < dump.sql

# Importa in database esistente
sqlite3 db.sqlite3 < dump.sql

# Importa via pipe
cat dump.sql | sqlite3 db.sqlite3
```

[↑ Torna all'indice](#indice)

---

## 3. Dump in CSV

### Esportazione da riga di comando

```bash
sqlite3 db.sqlite3 -header -csv "SELECT * FROM myapp_cliente;"      > clienti.csv
sqlite3 db.sqlite3 -header -csv "SELECT * FROM myapp_prodotto_new;" > prodotti.csv
sqlite3 db.sqlite3 -header -csv "SELECT * FROM myapp_ordine;"       > ordini.csv
```

### Esportazione da Django Shell

```python
# Avvia la shell di Django
python manage.py shell

import csv
from your_app.models import Cliente, Prodotto_new, Ordine

# Esporta Clienti
with open('clienti.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['id', 'nome', 'cognome', 'email', 'telefono', 'indirizzo'])
    for cliente in Cliente.objects.all():
        writer.writerow([cliente.id, cliente.nome, cliente.cognome,
                         cliente.email, cliente.telefono, cliente.indirizzo])

# Esporta Prodotti
with open('prodotti.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['id', 'nome', 'descrizione', 'prezzo', 'categoria', 'quantita'])
    for prodotto in Prodotto_new.objects.all():
        writer.writerow([prodotto.id, prodotto.nome, prodotto.descrizione,
                         prodotto.prezzo, prodotto.categoria, prodotto.quantita])

# Esporta Ordini
with open('ordini.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['id', 'cliente_id', 'prodotto_id', 'quantita', 'totale', 'data_ordine', 'stato'])
    for ordine in Ordine.objects.all():
        writer.writerow([ordine.id, ordine.cliente_id, ordine.prodotto_id,
                         ordine.quantita, ordine.totale, ordine.data_ordine, ordine.stato])
```

### Importazione (Load) da CSV

```python
# Da Django Shell
import csv
from your_app.models import Cliente

with open('clienti.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        Cliente.objects.create(
            nome=row['nome'],
            cognome=row['cognome'],
            email=row['email'],
            telefono=row['telefono'],
            indirizzo=row['indirizzo']
        )
```

[↑ Torna all'indice](#indice)

---

## 4. Backup del File Database

### Backup semplice

```bash
# Copia semplice del file
cp db.sqlite3 db_backup.sqlite3

# Con timestamp
cp db.sqlite3 db_backup_$(date +%Y%m%d_%H%M%S).sqlite3

# Con nome personalizzato in una cartella dedicata
cp db.sqlite3 backup/backup_$(date +%Y%m%d).sqlite3
```

### Compressione

```bash
# Comprimi con gzip
gzip -c db.sqlite3 > db_backup.sqlite3.gz

# Comprimi con zip
zip backup.zip db.sqlite3

# Comprimi con tar
tar -czvf backup.tar.gz db.sqlite3
```

### Ripristino

```bash
# Copia backup sul database esistente
cp db_backup.sqlite3 db.sqlite3

# Estrai da gzip e ripristina
gunzip -c db_backup.sqlite3.gz > db.sqlite3

# Estrai da zip
unzip backup.zip

# Estrai da tar
tar -xzvf backup.tar.gz
```

[↑ Torna all'indice](#indice)

---

## 5. Comando Personalizzato Django

### Comando di esportazione

```python
# Crea il file: your_app/management/commands/export_db.py

from django.core.management.base import BaseCommand
import json
from datetime import datetime
from your_app.models import Cliente, Prodotto_new, Ordine

class Command(BaseCommand):
    help = 'Esporta il database in formato JSON'

    def add_arguments(self, parser):
        parser.add_argument(
            '--file',
            type=str,
            default='export_full.json',
            help='Nome del file di output'
        )

    def handle(self, *args, **options):
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = options['file'].replace('.json', f'_{timestamp}.json')

        data = {
            'data_esportazione': timestamp,
            'clienti': list(Cliente.objects.values()),
            'prodotti': list(Prodotto_new.objects.values()),
            'ordini': list(Ordine.objects.values())
        }

        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, default=str)

        self.stdout.write(self.style.SUCCESS(f'Dati esportati con successo in {filename}'))
```

### Comando di importazione

```python
# Crea il file: your_app/management/commands/import_db.py

from django.core.management.base import BaseCommand
import json
from your_app.models import Cliente, Prodotto_new, Ordine

class Command(BaseCommand):
    help = 'Importa dati da file JSON'

    def add_arguments(self, parser):
        parser.add_argument('file', type=str, help='File JSON da importare')

    def handle(self, *args, **options):
        filename = options['file']

        with open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)

        if 'clienti' in data:
            for cliente_data in data['clienti']:
                Cliente.objects.create(**cliente_data)

        if 'prodotti' in data:
            for prodotto_data in data['prodotti']:
                Prodotto_new.objects.create(**prodotto_data)

        if 'ordini' in data:
            for ordine_data in data['ordini']:
                Ordine.objects.create(**ordine_data)

        self.stdout.write(self.style.SUCCESS(f'Dati importati con successo da {filename}'))
```

### Utilizzo dei comandi

```bash
# Esporta
python manage.py export_db --file backup.json

# Importa
python manage.py import_db backup.json
```

[↑ Torna all'indice](#indice)

---

## 6. Script per Backup Automatico

### Script completo di backup

```python
# Crea il file: your_app/management/commands/backup_db.py

import os
import json
import shutil
from datetime import datetime
from django.core.management import call_command
from django.core.management.base import BaseCommand
from django.conf import settings

class Command(BaseCommand):
    help = 'Crea un backup completo del database'

    def add_arguments(self, parser):
        parser.add_argument(
            '--keep',
            type=int,
            default=5,
            help='Numero di backup da mantenere'
        )

    def handle(self, *args, **options):
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_dir = 'backups'
        keep = options['keep']

        # Crea directory backups se non esiste
        if not os.path.exists(backup_dir):
            os.makedirs(backup_dir)

        # 1. Backup JSON
        json_file = f'{backup_dir}/backup_{timestamp}.json'
        with open(json_file, 'w', encoding='utf-8') as f:
            call_command('dumpdata', exclude=['auth.permission', 'contenttypes'], stdout=f)

        # 2. Backup SQLite file
        sqlite_file = f'{backup_dir}/db_backup_{timestamp}.sqlite3'
        shutil.copy2(settings.DATABASES['default']['NAME'], sqlite_file)

        # 3. Comprimi il backup SQLite
        shutil.make_archive(sqlite_file, 'gztar', backup_dir,
                            f'db_backup_{timestamp}.sqlite3')
        os.remove(sqlite_file)

        # 4. Rimuovi backup vecchi
        all_backups = sorted([f for f in os.listdir(backup_dir)
                              if f.startswith('backup_')])
        if len(all_backups) > keep:
            for old_backup in all_backups[:-keep]:
                os.remove(f'{backup_dir}/{old_backup}')

        self.stdout.write(self.style.SUCCESS(
            f'Backup completato in {backup_dir}/backup_{timestamp}.json'
        ))
```

### Esecuzione automatica con cron

```bash
# Apri il crontab
crontab -e

# Backup ogni giorno alle 2:00 di notte
0 2 * * * cd /path/to/project && python manage.py backup_db --keep 7

# Backup ogni settimana (domenica alle 3:00)
0 3 * * 0 cd /path/to/project && python manage.py backup_db --keep 4
```

[↑ Torna all'indice](#indice)

---

## 7. Cosa non Backupare

### Escludi dal dump

```bash
# Escludi autenticazione e permessi
python manage.py dumpdata --exclude auth.permission --exclude contenttypes > dump.json

# Escludi sessioni (dati temporanei)
python manage.py dumpdata --exclude sessions > dump.json

# Escludi migration records
python manage.py dumpdata --exclude django_migrations > dump.json
```

### Backup completo con esclusioni standard

```bash
python manage.py dumpdata \
    --exclude auth.permission \
    --exclude contenttypes \
    --exclude sessions \
    > dump.json
```

[↑ Torna all'indice](#indice)

---

## 8. Raccomandazioni Finali

| Tipo di Backup | Quando usare | Vantaggi | Svantaggi |
|---|---|---|---|
| **JSON** (`dumpdata`) | Migrazioni, condivisione dati | Indipendente dal DB, leggibile, relazioni mantenute | File grande, lento su DB grandi |
| **SQL** (`sqlite3 .dump`) | Backup di emergenza, ripristino veloce | Veloce, completo, ricrea esattamente il DB | Dipendente da SQLite3, meno flessibile |
| **File** (copia `.sqlite3`) | Backup automatici notturni | Semplicissimo e veloce | File binario, non modificabile |
| **CSV** | Export per analisi dati, Excel | Leggibile, usabile in altri software | Perde le relazioni tra tabelle |

### Best Practices

1. **Backup regolari** — ogni giorno o ogni settimana a seconda del progetto.
2. **Mantieni 3–5 versioni** — per poter tornare indietro nel tempo.
3. **Testa il ripristino** — verifica periodicamente che i backup siano integri.
4. **Usa formati multipli** — JSON + copia del file per massima sicurezza.
5. **Includi timestamp** — nei nomi dei file per identificarli facilmente.
6. **Escludi dati non necessari** — sessioni, permessi, contenttypes.
7. **Automatizza** — usa cron o un task scheduler.

### Risorse Utili

- [Django Documentation — dumpdata](https://docs.djangoproject.com/en/stable/ref/django-admin/#dumpdata)
- [Django Documentation — loaddata](https://docs.djangoproject.com/en/stable/ref/django-admin/#loaddata)
- [SQLite3 CLI Documentation](https://www.sqlite.org/cli.html)

[↑ Torna all'indice](#indice)

---

*Documentazione creata per progetto Django con SQLite3 — Ultimo aggiornamento: 2026*
