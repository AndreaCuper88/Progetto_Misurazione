# Generatore di Tracce — Propagazione dell'Incertezza

Strumento a riga di comando che genera automaticamente **tracce d'esame e soluzioni in codice MATLAB** per esercizi di propagazione dell'incertezza di misura con errori indipendenti.

Le tracce vengono prodotte combinando casualmente un **modello matematico** (da `modelli.json`) con un **caso di propagazione** (da `casi.py`), restituendo un testo pronto per la consegna agli studenti con la corrispondente soluzione commentata.

---

## Struttura dei file

| File | Descrizione |
|------|-------------|
| `generatore.py` | Script principale — genera la traccia e la soluzione MATLAB |
| `casi.py` | Definisce i 4 casi di propagazione (assoluto/relativo × WCU/standard) |
| `modelli.json` | Contiene i 15 modelli matematici con nominali, sensibilità e incertezze |
| `quesito1_log.csv` | File di log (creato automaticamente) per evitare la ripetizione dei modelli |

---

## Componenti principali

### `casi.py` — I 4 casi di propagazione

Il dizionario `CASES` definisce 4 scenari, ciascuno con:
- **`tipo_input`**: formato delle incertezze in ingresso
- **`domande`**: lista delle quantità che lo studente deve calcolare
- **`soluzione`**: formule MATLAB commentate per ogni quantità richiesta

| ID | Nome | Tipo input | Propagazione |
|----|------|------------|--------------|
| 1 | Assoluto – WCU | `abs_wcu` | Worst-Case Uncertainty con coefficienti assoluti |
| 2 | Assoluto – Standard | `abs_std` | Incertezza standard con coefficienti assoluti |
| 3 | Relativo – WCU | `rel_wcu` | Worst-Case Uncertainty con coefficienti relativi |
| 4 | Relativo – Standard | `rel_std` | Incertezza standard con coefficienti relativi |

---

### `modelli.json` — I modelli matematici

Array di 15 modelli. Struttura di ogni voce:

```json
{
  "id": "2",
  "titolo": "Distanza ricavata da velocità, tempo e angolo",
  "equazione_testo": "theta = x1*x2 / tan(phi) (dove phi è in radianti)",
  "funzione": "x1*x2 / tan(phi)",
  "output": "theta",
  "nominali": { "x1": 100, "x2": 25, "phi_deg": 38 },
  "sens": {
    "cx1": "x2/tan(phi)",
    "cx2": "x1/tan(phi)",
    "cphi": "-x1*x2/(sin(phi)^2)",
    "crx1": "1",
    "crx2": "1",
    "crphi": "-phi/(sin(phi)*cos(phi))"
  },
  "unc": {
    "abs_wcu": [{ "Ux1": 1.0, "Ux2": 0.2, "Uphi_deg": 0.5 }],
    "abs_std": [{ "ux1": 0.5, "ux2": 0.01, "uphi_deg": 0.1 }],
    "rel_wcu": [{ "Urx1": 0.01, "Urx2": 0.008, "Uphi_deg": 0.5 }],
    "rel_std": [{ "urx1": 0.005, "urx2": 0.0004, "uphi_deg": 0.1 }]
  }
}
```

Campi principali:
- `id / titolo / equazione_testo / funzione` — identificazione e descrizione della formula
- `output` — nome della variabile di uscita usato nella traccia e nella soluzione (es. `"theta"`)
- `msg` *(opzionale)* — nota esplicativa aggiuntiva per lo studente
- `nominali` — valori numerici delle variabili (`x1`, `x2`, `phi_deg`)
- `sens` — formule simboliche dei coefficienti di sensibilità assoluti (`cx*`) e relativi (`cr*`)
- `unc` — incertezze numeriche suddivise per tipo

---

### `generatore.py` — Script principale

| Funzione | Descrizione |
|----------|-------------|
| `read_log` | Legge gli ultimi N modelli usati dal log CSV e li restituisce come insieme da evitare |
| `append_log` | Aggiunge una riga al log dopo la conferma dell'utente |
| `pick_model` | Seleziona un modello (casuale o forzato via `--model`), escludendo quelli nel log |
| `pick_case` | Seleziona uno dei 4 casi (casuale o forzato via `--case`) |
| `render_trace` | Genera il testo completo della traccia e della soluzione MATLAB |

---

## Utilizzo

### Esecuzione base (interattiva)

```bash
python generatore.py
```

Lo script chiede se usare il log, genera una traccia casuale, la stampa a terminale e infine chiede se registrarla nel log.

### Opzioni da riga di comando

| Opzione | Esempio | Descrizione |
|---------|---------|-------------|
| `-h, --help` | `--help` | Mostra il messaggio di aiuto con la descrizione di tutti gli argomenti ed esce |
| `--model ID` | `--model 3` | Forza la selezione del modello con quell'ID (1–15) |
| `--case ID` | `--case 2` | Forza la selezione del caso (1–4) |
| `--seed N` | `--seed 42` | Fissa il seme casuale per riproducibilità |
| `--modelli PATH` | `--modelli data/modelli.json` | Percorso alternativo al file JSON |

### Esempi

```bash
# Visualizzare l'aiuto
python generatore.py --help

# Generazione completamente casuale
python generatore.py

# Modello 5, caso 3 (Relativo – WCU)
python generatore.py --model 5 --case 3

# Riprodurre esattamente una traccia già generata
python generatore.py --model 5 --case 3 --seed 42
```

---

## Formato dell'output

L'output è un testo in formato MATLAB composto da due sezioni:

**Sezione dati** (per lo studente) — commenti descrittivi, valori nominali e incertezze come variabili MATLAB. Preceduta dalla nota che il codice non va riportato nella soluzione.

**Sezione soluzione** (per il docente) — contrassegnata da `%% Soluzione`. Include la conversione dell'angolo da gradi a radianti, i coefficienti di sensibilità e tutte le quantità richieste con le rispettive formule commentate.

---

## Come estendere il progetto

### Aggiungere un nuovo modello
Aprire `modelli.json` e aggiungere un oggetto nell'array seguendo la struttura sopra. Fornire obbligatoriamente: `id` univoco, `funzione` MATLAB, `output`, `nominali`, tutti e 6 i coefficienti di sensibilità (`cx1`, `cx2`, `cphi`, `crx1`, `crx2`, `crphi`) e le incertezze per tutti e 4 i tipi di input.

### Aggiungere un nuovo caso
Aprire `casi.py` e aggiungere una nuova chiave al dizionario `CASES` con ID progressivo. Definire `tipo_input`, `domande` e `soluzione`. Se si introducono nuove variabili, aggiornare anche `DOMANDA_LABELS` in `generatore.py`.

---

## Dipendenze

Python 3.8+ con sola libreria standard. Nessun pacchetto esterno richiesto.