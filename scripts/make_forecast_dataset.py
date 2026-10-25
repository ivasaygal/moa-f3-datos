"""Series mensuales de pernoctaciones hoteleras en Andalucía (INE, Encuesta de Ocupación Hotelera, tabla 67190).

Fuente: INE · https://www.ine.es/jaxiT3/Tabla.htm?t=67190 · uso libre citando la fuente (aviso legal del INE).
"""
import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "raw" / "ine_67190.csv"
OUT = ROOT / "S15_forecasting"
DESDE = "2010M01"

series = {}
for r in csv.DictReader(open(SRC, encoding="utf-8-sig"), delimiter=";"):
    if r["Viajeros y pernoctaciones"] != "Pernoctaciones" or r["Residencia: Nivel 2"]:
        continue
    if r["Comunidades y Ciudades Autónomas"] != "01 Andalucía" or r["Periodo"] < DESDE or not r["Total"]:
        continue
    nombre = r["Provincias"][3:] if r["Provincias"] else "Andalucía"
    fecha = f"{r['Periodo'][:4]}-{r['Periodo'][5:]}-01"
    series.setdefault(nombre, {})[fecha] = int(r["Total"].replace(".", ""))

and_ = series.pop("Andalucía")
with open(OUT / "pernoctaciones_andalucia_mensual.csv", "w", encoding="utf-8", newline="") as f:
    w = csv.writer(f)
    w.writerow(["fecha", "valor"])
    for k in sorted(and_):
        w.writerow([k, and_[k]])

with open(OUT / "pernoctaciones_provincias_mensual.csv", "w", encoding="utf-8", newline="") as f:
    w = csv.writer(f)
    w.writerow(["provincia", "fecha", "valor"])
    for prov in sorted(series):
        for k in sorted(series[prov]):
            w.writerow([prov, k, series[prov][k]])

fechas = sorted(and_)
print("Andalucía:", len(fechas), "meses", fechas[0], "→", fechas[-1])
print("Provincias:", sorted(series), {p: len(v) for p, v in series.items()})
for y in ("2019", "2020", "2021", "2024", "2025"):
    print(y, sum(v for k, v in and_.items() if k.startswith(y)))
print("agosto 2025", and_.get("2025-08-01"), "enero 2025", and_.get("2025-01-01"))
