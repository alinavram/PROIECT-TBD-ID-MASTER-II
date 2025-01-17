# NYC Taxi Fare Prediction Pipeline
## Descrierea proiectului
Acest proiect implementează un pipeline complet pentru descărcarea, preprocesarea și analiza datelor despre cursele de taxi din New York City, folosind Google Cloud Platform (GCP) și Python. Scopul proiectului este de a antrena un model de regresie pentru a prezice tariful unei curse de taxi pe baza unor caracteristici precum distanța parcursă, locațiile de pick-up și drop-off, durata cursei și alți factori.

## Componentele proiectului
1. preprocess_and_data_storage.py
Este responsabil pentru descărcarea datelor, preprocesarea lor, încărcarea în Google Cloud Storage și importarea lor într-un tabel BigQuery.

### Funcționalități principale:
#### Descărcarea datelor:

 - Descărcăm fișierul PARQUET corespunzător lunii și anului specificat dintr-o sursă externă.
 - URL-ul fișierului este construit dinamic folosind BASE_URL.
   
#### Preprocesarea datelor:

 - Eliminarea atributelor cu mai mult de 50% date lipsă.
 - Eliminarea rândurilor cu valori lipsă pentru atributele rămase.

#### Încărcarea datelor preprocesate în Google Cloud Storage:

 - Verificăm dacă bucket-ul GCS există. Dacă nu, îl creăm automat.
 - Fișierul preprocesat este încărcat în bucket-ul specificat.
   
#### Crearea unui dataset BigQuery:

 - Verificăm dacă dataset-ul BigQuery există. Dacă nu, îl creăm automat.
 - Importul datelor în BigQuery:

Datele preprocesate sunt importate într-un tabel BigQuery pentru a fi utilizate ulterior în antrenarea modelului.

2. fare_amount_prediction.py
Execută pașii necesari pentru o noua procesare a datelor, antrenarea modelului și evaluarea performanței acestuia folosind BigQuery ML.

### Funcționalități principale:
#### Filtrarea și pregătirea datelor:

 - Cream un tabel filtrat (filtered_tripdata) care conține doar cursele relevante, excluzând valorile anormale (e.g., distanțe prea mici sau tarife eronate).
   
#### Împărțirea datelor în seturi de antrenare și testare:

 - training_data (80% din date) este utilizat pentru antrenarea modelului.
 - testing_data (20% din date) este utilizat pentru evaluarea modelului.
   
#### Crearea modelului de predicție a tarifelor:

 - Antrenăm un model de regresie liniară (LINEAR_REG) pentru a prezice tariful unei curse (fare_amount) pe baza caracteristicilor relevante.
   
#### Evaluarea modelului:

Calculăm metrici de performanță (e.g., mean absolute error, R² score) pentru a evalua calitatea predicțiilor.

3. constants.py
Acest fișier definește constantele utilizate în ambele scripturi, pentru a asigura flexibilitatea și ușurința configurării.

Principalele constante:
BASE_URL: URL-ul de descărcare pentru fișierele PARQUET.
BUCKET_NAME: Numele bucket-ului Google Cloud Storage.
PROJECT_ID: ID-ul proiectului Google Cloud.
DATASET_ID: ID-ul dataset-ului BigQuery.
TABLE_ID: Numele tabelului BigQuery.
JSON_KEY: Calea către cheia de autentificare pentru GCP.
