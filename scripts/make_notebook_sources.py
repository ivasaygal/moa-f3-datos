"""Convierte las 3.000 reseñas en archivos Markdown para subirlos como fuentes a Gemini Notebook (sprint 3 de S14).

Gemini Notebook trata los CSV y las hojas de cálculo como Google Sheets (límite de 100.000 tokens),
así que las reseñas se suben como texto, repartidas en varios archivos.
"""
import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "S14_lab_rag" / "resenas_hoteles_andalucia_lab.csv"
OUT = ROOT / "S14_lab_rag" / "gemini_notebook"
POR_ARCHIVO = 750

rows = sorted(csv.DictReader(open(SRC, encoding="utf-8")), key=lambda r: int(r["id"]))
OUT.mkdir(exist_ok=True)
for old in OUT.glob("resenas_*.md"):
    old.unlink()

for n, i in enumerate(range(0, len(rows), POR_ARCHIVO), 1):
    lote = rows[i:i + POR_ARCHIVO]
    nombre = f"resenas_{n}_ids_{lote[0]['id']}-{lote[-1]['id']}.md"
    with open(OUT / nombre, "w", encoding="utf-8") as f:
        f.write(f"# Reseñas de hoteles de Andalucía · parte {n} (reseñas {lote[0]['id']} a {lote[-1]['id']})\n\n")
        f.write("Fuente: Andalusian Hotels' Reviews (Kaggle, CC BY-NC 4.0). Cada reseña lleva su id para poder citarla.\n\n")
        for r in lote:
            f.write(f"## Reseña {r['id']} · {r['hotel']} · {r['provincia']} · nota {r['nota']}/5\n\n")
            f.write(f"**{r['titulo'].strip()}**\n\n{r['texto'].strip()}\n\n")
    palabras = sum(len((r["titulo"] + " " + r["texto"]).split()) for r in lote)
    print(f"{nombre}: {len(lote)} reseñas, {palabras} palabras, {(OUT / nombre).stat().st_size // 1024} KB")
