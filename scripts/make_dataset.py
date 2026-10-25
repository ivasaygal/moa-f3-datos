"""Muestra equilibrada de Andalusian Hotels' Reviews (CC BY-NC 4.0) para el lab de S12."""
import csv
import random
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "raw" / "Big_AHR.csv"
OUT = ROOT / "S12_nosql_vectoriales" / "resenas_hoteles_andalucia_lab.csv"
OUT_S14 = ROOT / "S14_lab_rag" / "resenas_hoteles_andalucia_lab.csv"
QUOTA = {"1": 500, "2": 500, "3": 600, "4": 600, "5": 800}


PROV = {"Seville": "Sevilla", "Cordoba": "Córdoba", "Malaga": "Málaga", "Jaen": "Jaén", "Almeria": "Almería",
        "Granada": "Granada", "Huelva": "Huelva", "Cadiz": "Cádiz", "Malag": "Málaga"}


def city(loc):
    m = re.search(r"Province_of_([A-Za-z]+)", loc)
    return PROV.get(m.group(1), m.group(1)) if m else ""


def clean(t):
    return re.sub(r"\s+", " ", t).strip()


rows = [r for r in csv.DictReader(open(SRC, encoding="utf-8")) if city(r["location"])
        if r["hotel"] and r["location"] and 80 <= len(r["review_text"]) <= 2500]
random.seed(2026)
sample = []
for stars, n in QUOTA.items():
    pool = [r for r in rows if r["rating"] == stars]
    sample += random.sample(pool, min(n, len(pool)))
random.shuffle(sample)

with open(OUT, "w", encoding="utf-8", newline="") as f:
    w = csv.writer(f)
    w.writerow(["id", "hotel", "provincia", "nota", "titulo", "texto"])
    for i, r in enumerate(sample, 1):
        w.writerow([i, clean(r["hotel"].replace("_", " ")), city(r["location"]), r["rating"], clean(r["title"]), clean(r["review_text"])])

import shutil
shutil.copyfile(OUT, OUT_S14)

from collections import Counter
print(OUT, "(copiado también a S14)", len(sample))
print(Counter(r["rating"] for r in sample))
print(Counter(city(r["location"]) for r in sample).most_common())
print("hoteles", len({r["hotel"] for r in sample}))
print("caracteres totales", sum(len(r["review_text"]) for r in sample))
