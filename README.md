# Datos del bloque F3 · Datos & Crecimiento (S12-S15)

Material de datos para las sesiones S12-S15 del máster: cada carpeta contiene lo que hace falta para **resolver esa sesión** y un `INSTRUCCIONES_AGENTE.md` con lo que hay que pedirle al agente de IA (Claude Code, Codex o Antigravity) para completarla en modo *vibe-coding*.

## Cómo usarlo

1. Copia la carpeta de la sesión en el proyecto de tu equipo.
2. Abre tu agente en esa carpeta y dile:
   > «Lee INSTRUCCIONES_AGENTE.md y ejecuta la FASE 0. Para y espera mi confirmación al final de cada fase.»
3. Avanza fase a fase, revisando las **comprobaciones** de cada una antes de seguir.

Las claves (Supabase, OpenAI, Gemini) van **siempre** en un archivo `.env` que **no se sube** al repositorio (está en `.gitignore`).

## Contenido por sesión

| Carpeta | Sesión | Qué contiene |
|---|---|---|
| [`S12_nosql_vectoriales/`](S12_nosql_vectoriales/) | S12 · NoSQL y bases de datos vectoriales (jue 12 nov) | `resenas_hoteles_andalucia_lab.csv` (3.000 reseñas) · `esquema_demo/` (cadenas → hoteles → reseñas, y cadenas → usuarios, con `schema.sql`) · instrucciones |
| [`S13_rag_teoria/`](S13_rag_teoria/) | S13 · Sistemas RAG: teoría y arquitectura (lun 16 nov) | `rag_demo/`: 4 documentos ficticios de «Grupo Azahar Hoteles» y 6 preguntas de prueba con sus respuestas · instrucciones para diseñar el blueprint |
| [`S14_lab_rag/`](S14_lab_rag/) | S14 · LAB: RAG construido y evaluado (mar 17 nov) | `golden_set_plantilla.csv` (20 preguntas) · `resenas_hoteles_andalucia_lab.csv` (copia) · instrucciones por sprints |
| [`S15_forecasting/`](S15_forecasting/) | S15 · Forecasting con IA (mié 18 nov) | Pernoctaciones hoteleras mensuales de Andalucía y de sus 8 provincias (2010-2026) · instrucciones para Colab con Chronos-2 |
| [`raw/`](raw/) | — | Datos originales sin procesar (ver fuentes) |
| [`scripts/`](scripts/) | — | Scripts que generan todos los archivos a partir de `raw/` |

## Fuentes y licencias

| Datos | Fuente | Licencia / condiciones |
|---|---|---|
| Reseñas de hoteles (`raw/Big_AHR.csv`, `raw/Balanced_AHR.csv`, `raw/andalusian.zip` y la muestra de 3.000 reseñas) | [Andalusian Hotels’ Reviews](https://www.kaggle.com/datasets/chizhikchi/andalusian-hotels-reviews-unbalanced) (Kaggle, autora: chizhikchi). Reseñas de TripAdvisor (2021) y del corpus COAH del grupo SINAI, Universidad de Jaén (2014). | **CC BY-NC 4.0**: uso no comercial y citando la fuente |
| Pernoctaciones hoteleras (`raw/ine_67190.csv` y las series de S15) | [INE · Encuesta de Ocupación Hotelera, tabla 67190](https://www.ine.es/jaxiT3/Tabla.htm?t=67190) | Uso libre citando la fuente ([aviso legal del INE](https://www.ine.es/aviso_legal)) |
| Cadenas, usuarios y asignación de hoteles a cadenas (`esquema_demo/`) | Generados para el curso | **Ficticios** |
| Documentos de «Grupo Azahar Hoteles» (`rag_demo/`) | Redactados para el curso | **Ficticios**: precios, plazos y emails (`example.com`) inventados |

> ⚠️ **Sobre la muestra de reseñas:** está equilibrada a propósito (entre 500 y 800 reseñas por nota), así que **las medias no reflejan la reputación real de ningún hotel**. La pertenencia de los hoteles a las cadenas del esquema de demo es inventada.

## Regenerar los datos

Los scripts usan solo la librería estándar de Python y semillas fijas, así que siempre generan los mismos archivos:

```
python scripts/make_dataset.py           # raw/Big_AHR.csv → muestra de 3.000 reseñas (S12 y S14)
python scripts/make_schema_demo.py       # → S12_nosql_vectoriales/esquema_demo/
python scripts/make_golden_set.py        # → S14_lab_rag/golden_set_plantilla.csv
python scripts/make_forecast_dataset.py  # raw/ine_67190.csv → series de S15
```
