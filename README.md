Generatore di Tracce per Esercizi di Propagazione dell'Incertezza
1. Panoramica del Progetto
Il progetto consiste in uno strumento a riga di comando scritto in Python che genera automaticamente tracce (testi d'esame e relative soluzioni in codice MATLAB) per esercizi di propagazione dell'incertezza di misura con errori indipendenti.
Le tracce vengono generate combinando casualmente un modello matematico (prelevato da un file JSON) con un caso di propagazione (definito in un modulo Python), producendo un testo pronto per la consegna agli studenti con la corrispondente soluzione commentata.

2. Struttura dei File
File
Tipo
Descrizione
genera_traccia.py
Python
Script principale — genera la traccia e la soluzione MATLAB
casi.py
Python
Definisce i 4 casi di propagazione (assoluto/relativo × WCU/standard)
modelli.json
JSON
Contiene i 15 modelli matematici con nominali, sensibilità e incertezze
quesito1_log.csv
CSV
File di log (creato automaticamente) per evitare la ripetizione dei modelli


3. Componenti Principali
3.1  casi.py — I 4 Casi di Propagazione
Il dizionario CASES definisce 4 scenari di propagazione, ciascuno con:
tipo_input: il formato delle incertezze fornite in ingresso (abs_wcu, abs_std, rel_wcu, rel_std)
domande: lista delle quantità che lo studente deve calcolare
soluzione: formule MATLAB commentate per ogni quantità richiesta

ID
Nome
Tipo Input
Propagazione
1
Assoluto – WCU
abs_wcu
Worst-Case Uncertainty con coeff. assoluti
2
Assoluto – Standard
abs_std
Incertezza standard con coeff. assoluti
3
Relativo – WCU
rel_wcu
Worst-Case Uncertainty con coeff. relativi
4
Relativo – Standard
rel_std
Incertezza standard con coeff. relativi


3.2  modelli.json — I Modelli Matematici
Contiene un array di 15 modelli. Ogni modello ha la seguente struttura:

{
  "id": "2",
  "titolo": "Distanza ricavata da velocità, tempo e angolo",
  "equazione_testo": "d = x1*x2 / tan(phi)",
  "funzione": "x1*x2 / tan(phi)",
  "nominali": { "x1": 100, "x2": 25, "phi_deg": 38 },
  "sens": {
    "cx1": "x2/tan(phi)",
    "cx2": "x1/tan(phi)",
    "cphi": "-x1*x2/(sin(phi)^2)",
    "crx1": "1", "crx2": "1", ...
  },
  "unc": {
    "abs_wcu": [{ "Ux1": 1.0, "Ux2": 0.2, "Uphi_deg": 0.5 }],
    "abs_std": [{ "ux1": 0.5, "ux2": 0.01, "uphi_deg": 0.1 }],
    ...
  }
}

I campi principali di ogni modello sono:
id / titolo / equazione_testo / funzione: identificazione e descrizione della formula
msg (opzionale): nota esplicativa aggiuntiva per lo studente
nominali: valori numerici delle variabili (x1, x2, phi_deg)
sens: formule simboliche dei coefficienti di sensibilità assoluti (cx*) e relativi (cr*)
unc: incertezze numeriche suddivise per tipo (abs_wcu, abs_std, rel_wcu, rel_std)

3.3  genera_traccia.py — Script Principale
Orchestratore del sistema. Le sue funzioni principali sono:

read_log / append_log
Gestiscono il file CSV di log (quesito1_log.csv). La funzione read_log legge gli ultimi N modelli utilizzati con esito positivo e li restituisce come insieme da evitare. append_log aggiunge una nuova riga al log al termine dell'esercitazione.

pick_model
Seleziona un modello dalla lista: se viene passato --model, usa quello specifico; altrimenti effettua una scelta casuale escludendo i modelli presenti nel log (evitando ripetizioni recenti).

pick_case
Seleziona uno dei 4 casi di propagazione: casualmente oppure quello specificato con --case.

render_trace
Genera il testo completo della traccia e della soluzione MATLAB. Il testo include:
intestazione con titolo e formula del modello
sezione dati (valori nominali e incertezze come variabili MATLAB)
elenco delle domande richieste allo studente
sezione soluzione con le formule commentate

4. Come si Usa
4.1  Esecuzione Base (Interattiva)
Dalla directory del progetto, eseguire:

python genera_traccia.py

Lo script chiederà innanzitutto se utilizzare il file di log, poi genererà una traccia casuale e stamperà il risultato a terminale. Alla fine chiederà se registrare la traccia nel log.

4.2  Opzioni da Riga di Comando

Opzione
Valore
Descrizione
--model ID
es. --model 3
Forza la selezione del modello con quell'ID
--case ID
es. --case 2
Forza la selezione del caso (1–4)
--seed N
es. --seed 42
Fissa il seme casuale per riproducibilità
--modelli PATH
es. --modelli data/modelli.json
Percorso alternativo al file JSON


4.3  Esempi di Utilizzo
Generazione completamente casuale, senza log:
python genera_traccia.py

Selezionare il modello 5 con il caso 3 (Relativo – WCU):
python genera_traccia.py --model 5 --case 3

Riprodurre esattamente una traccia già generata in precedenza:
python genera_traccia.py --model 5 --case 3 --seed 42

4.4  Il File di Log
Il file quesito1_log.csv viene creato automaticamente nella stessa directory. Ogni riga memorizza la data (campo riservato), l'ID del modello e l'ID del caso. Grazie al log, le ultime 3 tracce registrate vengono escluse dalla selezione casuale, evitando di proporre esercizi già assegnati di recente.

5. Formato dell'Output
L'output è un file di testo in formato MATLAB composto da due sezioni:

5.1  Sezione Dati (visibile allo studente)
Contiene i commenti descrittivi della formula, i valori nominali e le incertezze già assegnati come variabili MATLAB. Questa sezione è preceduta dalla nota che il codice non va riportato nella soluzione.

5.2  Sezione Soluzione (per il docente)
Segue immediatamente dopo ed è contrassegnata dal commento %% Soluzione. Include la conversione dell'angolo da gradi a radianti, il calcolo dei coefficienti di sensibilità e tutte le quantità richieste nelle domande, con le rispettive formule MATLAB commentate.

6. Come Estendere il Progetto
6.1  Aggiungere un Nuovo Modello
Aprire modelli.json e aggiungere un nuovo oggetto nell'array seguendo la struttura descritta nella sezione 3.2. È necessario fornire: id univoco, titolo, funzione MATLAB, valori nominali, tutti i coefficienti di sensibilità (cx1, cx2, cphi, crx1, crx2, crphi) e le incertezze per tutti e 4 i tipi di input.

6.2  Aggiungere un Nuovo Caso
Aprire casi.py e aggiungere una nuova chiave al dizionario CASES con un ID progressivo. Definire tipo_input, domande e soluzione seguendo il formato degli esempi esistenti. Aggiornare anche il dizionario DOMANDA_LABELS in genera_traccia.py se si introducono nuove variabili.
