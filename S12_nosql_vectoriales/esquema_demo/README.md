# Esquema de demo · slide 11 de S12

Datos para montar en Supabase el esquema del diagrama de entidades de la slide 11 (**cadena hotelera → hoteles → reseñas**, y **cadena → usuarios**) y enseñarlo en clase.

| Archivo | Tabla | Filas | Origen |
|---|---|---|---|
| `1_cadenas.csv` | cadenas | 4 | **Ficticio** (nombres inventados y marcados como «ficticia») |
| `2_hoteles.csv` | hoteles | 669 | Nombres y provincias **reales** del dataset; la cadena asignada es **inventada** |
| `3_usuarios.csv` | usuarios | 16 | **Ficticio** (4 por cadena; emails en el dominio reservado `example.com`) |
| `4_resenas.csv` | resenas | 3.000 | **Reales**: las mismas reseñas del lab (Andalusian Hotels’ Reviews, Kaggle, CC BY-NC 4.0) |
| `schema.sql` | — | — | Crea las 4 tablas, sus relaciones, los índices y la seguridad por fila |

> ⚠️ **Antes de enseñarlo:**
> - **Las medias no reflejan la reputación real de ningún hotel.** La muestra se equilibró a propósito (500-800 reseñas por cada nota), así que sobran reseñas negativas respecto al original.
> - **La pertenencia de cada hotel a una cadena es inventada.**
>
> Conviene decirlo en voz alta si se muestran rankings de hoteles.

## Cómo montarlo en Supabase (≈ 5 minutos)

1. Crea un proyecto nuevo en supabase.com (región Europa).
2. **SQL Editor** → pega y ejecuta `schema.sql`.
3. **Table Editor** → importa los CSV **en este orden**: cadenas → hoteles → usuarios → reseñas. En cada tabla: *Insert → Import data from CSV*. El orden importa por las relaciones: no puede existir un hotel sin su cadena.
4. Comprueba los recuentos: 4 cadenas, 669 hoteles, 16 usuarios y 3.000 reseñas.
5. (Opcional) Pide a tu agente que calcule los embeddings de `titulo + texto` de cada reseña con text-embedding-3-small y los guarde en la columna `embedding`.

**Alternativa en modo vibe-coding:** dale esta carpeta a tu agente con el Supabase MCP y pídele:
> «Ejecuta schema.sql en mi proyecto, importa los cuatro CSV en orden (cadenas, hoteles, usuarios, reseñas) y comprueba los recuentos. Explícame cada tabla y cada relación en una frase.»

## Qué enseñar en clase

- **El diagrama, de verdad.** En Supabase, *Database → Schema Visualizer* dibuja las tablas y sus relaciones: es el diagrama de la slide 11 generado a partir de la base real.
- **Las claves foráneas.** Abre la tabla de reseñas y señala `hotel_id`; abre hoteles y señala `cadena_id`.
- **El borrado en cascada.** Si se borra una cadena, desaparecen sus hoteles, sus reseñas y sus usuarios. Es el «derecho al olvido» del diseño.
- **La seguridad por fila.** Está activada en las 4 tablas y sin políticas, así que desde una web pública no se leería nada. Es el punto de partida seguro.

## Preguntas de demo para el agente (con el Supabase MCP de solo lectura)

| Pregunta en lenguaje natural | Respuesta esperada (para verificar) |
|---|---|
| «¿Cuántas reseñas y qué nota media tiene cada cadena?» | Grupo Azahar 832 · 3,13 — Costa Luz 833 · 3,29 — Sierra y Mar 895 · 3,23 — Patio Andaluz 440 · 3,35 |
| «¿Qué nota media hay por provincia?» | Almería 2,91 · Córdoba 3,30 · Granada 3,35 · Huelva 2,89 · Jaén 2,90 · Málaga 3,37 · Sevilla 3,25 (Cádiz tiene solo 4 reseñas) |
| «¿Cuántas reseñas de nota 1 tienen los hoteles de Costa Luz en Sevilla?» | 22 |
| «¿Qué 5 hoteles tienen más reseñas y a qué cadena pertenecen?» | El primero, con 29 reseñas, pertenece a Grupo Azahar |
| «¿Qué usuarios tiene Grupo Azahar y con qué rol?» | 4 usuarios: un admin, dos analistas y un lector |

Estas preguntas recorren las relaciones (reseña → hotel → cadena), que es justo lo que explica la slide 11. Si el agente acierta los números, el esquema está bien montado.

## Regenerar los datos

```
python scripts/make_schema_demo.py   (desde la raíz del repositorio)
```

Parte de `S12_nosql_vectoriales/resenas_hoteles_andalucia_lab.csv` y usa una semilla fija, así que siempre genera los mismos datos.
