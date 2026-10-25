"""Genera el esquema de demo de la slide 11 (cadenas · hoteles · usuarios · reseñas) a partir del dataset del lab.

Reseñas y hoteles: reales (Andalusian Hotels' Reviews, CC BY-NC 4.0).
Cadenas y usuarios: FICTICIOS, solo para la demo. La asignación de hoteles a cadenas es inventada.
"""
import csv
import random
import unicodedata
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "S12_nosql_vectoriales" / "resenas_hoteles_andalucia_lab.csv"
OUT = ROOT / "S12_nosql_vectoriales" / "esquema_demo"
OUT.mkdir(exist_ok=True)
rnd = random.Random(2026)

CADENAS = [
    (1, "Grupo Azahar (ficticia)", "Enterprise"),
    (2, "Costa Luz Hoteles (ficticia)", "Pro"),
    (3, "Sierra y Mar (ficticia)", "Pro"),
    (4, "Patio Andaluz (ficticia)", "Básico"),
]
NOMBRES = ["Lucía", "Hugo", "Martina", "Daniel", "Sofía", "Pablo", "Julia", "Álvaro", "Paula", "Adrián", "Carmen",
           "Javier", "Elena", "Manuel", "Irene", "Sergio", "Noelia", "Raúl", "Rocío", "Antonio"]
APELLIDOS = ["García", "Martín", "López", "Sánchez", "Romero", "Navarro", "Torres", "Ruiz", "Moreno", "Jiménez",
             "Molina", "Ortega", "Delgado", "Castro", "Vargas", "Rubio"]
ROLES = ["admin", "analista", "analista", "lector"]


def slug(t):
    t = unicodedata.normalize("NFKD", t).encode("ascii", "ignore").decode().lower()
    return "".join(c for c in t if c.isalnum())


resenas = list(csv.DictReader(open(SRC, encoding="utf-8")))

# hoteles: provincia más frecuente de cada hotel
prov_por_hotel = defaultdict(Counter)
for r in resenas:
    prov_por_hotel[r["hotel"]][r["provincia"]] += 1
nombres_hotel = sorted(prov_por_hotel)
hoteles = []
hotel_id = {}
for i, nombre in enumerate(nombres_hotel, 1):
    hotel_id[nombre] = i
    hoteles.append({"id": i, "cadena_id": rnd.choice([1, 1, 2, 2, 3, 3, 4]), "nombre": nombre,
                    "provincia": prov_por_hotel[nombre].most_common(1)[0][0]})

usuarios = []
uid = 1
for cid, cnombre, _ in CADENAS:
    dominio = slug(cnombre.split("(")[0]) + ".example.com"
    for rol in ROLES:
        n, a = rnd.choice(NOMBRES), rnd.choice(APELLIDOS)
        usuarios.append({"id": uid, "cadena_id": cid, "nombre": f"{n} {a}",
                         "email": f"{slug(n)}.{slug(a)}{uid}@{dominio}", "rol": rol})
        uid += 1


def write(name, fields, rows):
    with open(OUT / name, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)


write("1_cadenas.csv", ["id", "nombre", "plan"], [{"id": c, "nombre": n, "plan": p} for c, n, p in CADENAS])
write("2_hoteles.csv", ["id", "cadena_id", "nombre", "provincia"], hoteles)
write("3_usuarios.csv", ["id", "cadena_id", "nombre", "email", "rol"], usuarios)
write("4_resenas.csv", ["id", "hotel_id", "nota", "titulo", "texto"],
      [{"id": r["id"], "hotel_id": hotel_id[r["hotel"]], "nota": r["nota"], "titulo": r["titulo"], "texto": r["texto"]}
       for r in resenas])

cad_de_hotel = {h["id"]: h["cadena_id"] for h in hoteles}
por_cadena = Counter(cad_de_hotel[hotel_id[r["hotel"]]] for r in resenas)
print("cadenas", len(CADENAS), "| hoteles", len(hoteles), "| usuarios", len(usuarios), "| reseñas", len(resenas))
print("hoteles por cadena", Counter(h["cadena_id"] for h in hoteles))
print("reseñas por cadena", por_cadena)
