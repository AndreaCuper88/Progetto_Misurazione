from __future__ import annotations

import argparse
import json
import random
from pathlib import Path
from typing import Any

from casi import CASES


DEFAULT_MODELLI_PATH = Path("../data/modelli.json")

# Spiegazione delle domande (coerente con i CASES)
DOMANDA_LABELS = {
    # coefficienti assoluti
    "cx1": "coefficiente assoluto di sensibilità di x rispetto a x1",
    "cx2": "coefficiente assoluto di sensibilità di x rispetto a x2",
    "cphi": "coefficiente assoluto di sensibilità di x rispetto a phi",

    # coefficienti relativi
    "crx1": "coefficiente relativo di sensibilità di x rispetto a x1",
    "crx2": "coefficiente relativo di sensibilità di x rispetto a x2",
    "crphi": "coefficiente relativo di sensibilità di x rispetto a phi",

    # incertezze WCU
    "Ux": "incertezza di caso peggiore assoluta su x",
    "Urx": "incertezza di caso peggiore relativa su x",

    # incertezze standard
    "ux": "incertezza standard assoluta su x",
    "urx": "incertezza standard relativa su x",
}

def read_log(path: Path, last_n: int = 3) -> set[int]:

    if not path.exists():
        return set()

    rows = path.read_text(encoding="utf-8").splitlines()
    rows = rows[1:]  # salta header

    valid = []

    for r in rows:
        if not r.strip():
            continue

        data, model, case = r.split(",")

        if data != "0":
            valid.append(int(model))

    return set(valid[-last_n:])


def append_log(path: Path, model_id: int, case_id: int):

    line = f"0,{model_id},{case_id}\n"

    with path.open("a", encoding="utf-8") as f:
        f.write(line)


# ===============================
# Chiedo se utilizzare il log
# ===============================

while True:
    ans = input("Usare il file di log? (y/n): ").strip().lower()
    if ans in ("y", "n"):
        use_log = (ans == "y")
        break


LOG_PATH = Path("quesito1_log.csv")

if use_log:
    avoid_models = read_log(LOG_PATH)
else:
    avoid_models = set()


def load_modelli(path: Path) -> list[dict[str, Any]]:
    return json.loads(path.read_text(encoding="utf-8"))

def path_str(p: Path) -> str:
    return str(p.as_posix())

def pick_model(
    modelli: list[dict[str, Any]],
    model_id: str | None,
    rng: random.Random,
    avoid_models: set[int] | None = None
) -> tuple[int, dict[str, Any]]:

    if model_id is not None:
        for m in modelli:
            if str(m.get("id")) == str(model_id):
                return int(m["id"]), m
        raise ValueError(f"Modello id={model_id} non trovato in {path_str(DEFAULT_MODELLI_PATH)}")

    # scelta casuale evitando quelli nel log
    while True:
        m = rng.choice(modelli)
        mid = int(m["id"])

        if not avoid_models or mid not in avoid_models:
            return mid, m

def pick_case(case_id: str | None, rng: random.Random) -> tuple[int, dict[str, Any]]:
    if case_id is None:
        k = rng.choice(list(CASES.keys()))
        return int(k), CASES[k]
    cid = int(case_id)
    if cid not in CASES:
        raise ValueError(f"Case id={cid} non trovato in CASES")
    return cid, CASES[cid]



def format_value(v: Any) -> str:
    if isinstance(v, bool):
        return "true" if v else "false"
    if isinstance(v, (int, float)):
        return f"{v:.12g}"
    return str(v)


def render_trace(modello: dict[str, Any], caso_id: int, caso: dict[str, Any]) -> str:
    #letture
    titolo = modello.get("titolo", "Esercizio").strip()
    eq_testo = (modello.get("equazione_testo") or "").strip()
    funzione = (modello.get("funzione") or "").strip()
    msg = (modello.get("msg") or "").strip()

    nominali: dict[str, Any] = modello.get("nominali", {})
    tipo_input = caso["tipo_input"]  # abs_wcu, abs_std, rel_wcu, rel_std
    domande: list[str] = caso.get("domande", [])

    # incertezze dal blocco unc[tipo_input][0]
    unc_block = modello.get("unc", {})
    unc_list = unc_block.get(tipo_input, [])
    unc: dict[str, Any] = unc_list[0] if unc_list else {}

    n_dom = len(domande)

    out: list[str] = []
    out.append(f"%% Quesito 1 ({n_dom} domande) - Propagazione dell'incertezza con errori indipendenti - {titolo}")
    out.append("% Si ha la quantità, misurata indirettamente")
    out.append("%")
    if eq_testo:
        out.append(f"% {eq_testo}")
    elif funzione:
        out.append(f"% x = {funzione}")
    out.append("%")
    if msg:
        out.append(f"% {msg}")
        out.append("%")
    out.append("% Gli errori sulle grandezze di ingresso sono indipendenti.")
    out.append("%")
    out.append("% Attenzione: rispondere esattamente a tutte le domande di questo quesito è condizione NECESSARIA per superare la prova scritta.")
    # Nota su phi: se esiste phi_deg nei nominali, la evidenzio
    if "phi_deg" in nominali:
        out.append("% Nota: la funzione usa phi in radianti, ma il dato fornito è phi_deg in gradi.")
        out.append("%")
    out.append("%==============================")
    out.append("% Dati (il codice NON VA MAI RIPORTATO NELLA SOLUZIONE)")
    out.append("clear, clc")

    # nominali
    for k, v in nominali.items():
        out.append(f"{k} = {format_value(v)};")

    out.append("")

    # incertezze (già presenti nel JSON)
    for k, v in unc.items():
        out.append(f"{k} = {format_value(v)};")

    out.append("")
    out.append("%==============================")
    out.append("% Domande")

    for d in domande:
        label = DOMANDA_LABELS.get(d, f"risposta richiesta: {d}")
        out.append(f"% {d} = % {label}")

    out.append("")
    #Soluzione
    sens = modello.get("sens", {})
    sol = caso.get("soluzione", {})

    out.append("%% Soluzione")
    out.append("clc")
    out.append("% Conversione da gradi a radianti")
    out.append("phi = phi_deg/180*pi;")
    if "Uphi_deg" in unc:
        out.append("Uphi = Uphi_deg/180*pi;")

    if "uphi_deg" in unc:
        out.append("uphi = uphi_deg/180*pi;")

    out.append("")

    # stampa coefficienti rispetto a x1 e x2
    if any(d.startswith("cx") for d in domande):
        if "cx1" in sens:
            out.append("% Coefficienti di sensibilità assoluti")
            out.append(f"cx1 = {sens['cx1']};")
        if "cx2" in sens:
            out.append(f"cx2 = {sens['cx2']};")

    elif any(d.startswith("cr") for d in domande):
        if "crx1" in sens:
            out.append("% Coefficienti di sensibilità relativi")
            out.append(f"crx1 = {sens['crx1']};")
        if "crx2" in sens:
            out.append(f"crx2 = {sens['crx2']};")

    # stampa coefficiente dell'angolo, serve per i calcoli
    if any(d.startswith("cx") for d in domande) and "cphi" in sens:
        out.append(f"cphi = {sens['cphi']};")

    elif any(d.startswith("cr") for d in domande) and "crphi" in sens:
        out.append(f"crphi = {sens['crphi']};")

    out.append("")


    sol = caso.get("soluzione", {})

    out.append("")

    for var, data in sol.items():

        msg = data["msg"]
        formula = data["formula"]

        out.append(msg)
        if "abs(x)" in formula: #se nella formula uso x, ristampo la funzione per dare modo a matlab di fare il calcolo
            out.append(f"x = {funzione};")

        # serve Urphi se compare nella formula
        if "Urphi" in formula:
            out.append("Urphi = Uphi/abs(phi);")

        # serve urphi se compare nella formula
        if "urphi" in formula:
            out.append("urphi = uphi/abs(phi);")

        out.append(f"{var} = {formula};")
        out.append("")

    d_last = domande[-1]

    if d_last in sens:

        if d_last.startswith("cr"):
            out.append("% Coefficiente di sensibilità relativo")
        else:
            out.append("% Coefficiente di sensibilità assoluto")

        out.append(f"{d_last} = {sens[d_last]};")
        out.append("")


    return "\n".join(out) + "\n"


def main() -> None:

    ap = argparse.ArgumentParser(description="Generatore di tracce (solo testo) da modelli.json + casi.py")
    ap.add_argument("--modelli", type=str, default=str(DEFAULT_MODELLI_PATH))
    ap.add_argument("--model", type=str, default=None)
    ap.add_argument("--case", type=str, default=None)
    ap.add_argument("--seed", type=int, default=None)

    args = ap.parse_args()

    rng = random.Random(args.seed)

    modelli_path = Path(args.modelli)
    modelli = load_modelli(modelli_path)

    # scelta modello
    model_id, modello = pick_model(modelli, args.model, rng, avoid_models)

    # scelta caso
    case_id, caso = pick_case(args.case, rng)

    # generazione traccia
    trace = render_trace(modello, case_id, caso)

    print(trace)

    print(f"\nCombinazione generata: modello={model_id}, caso={case_id}") #Printo la combinazione

    # registrazione log
    if use_log:

        while True:
            ans = input("Registrare questa traccia nel log? (y/n): ").strip().lower()
            if ans in ("y", "n"):
                break

        if ans == "y":
            append_log(LOG_PATH, model_id, case_id)
            print("Traccia registrata nel log.")


if __name__ == "__main__":
    main()