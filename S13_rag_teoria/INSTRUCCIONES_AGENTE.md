# Instrucciones para el agente · S13: sistemas RAG, teoría y arquitectura

> **Cómo usar este documento**
> Copia esta carpeta en tu proyecto y dile a tu agente:
> **«Lee INSTRUCCIONES_AGENTE.md y ejecuta la FASE 0. Para y espera mi confirmación al final de cada fase.»**
> Hoy **no se construye el RAG** (eso es mañana, en S14): se **diseña** en un blueprint de una página.

---

## Contexto para el agente

Eres el arquitecto de soluciones de un equipo de producto que trabaja en modo *vibe-coding*. Hoy el equipo tiene que diseñar la **arquitectura RAG** de su producto: un asistente que responde con los documentos y datos propios del producto, citando las fuentes.

El resultado es un **blueprint**: un documento de diseño de una página que mañana usarás como especificación para construir el RAG.

### Archivos de esta carpeta

| Archivo | Para qué |
|---|---|
| `rag_demo/` | 4 documentos **ficticios** de la cadena «Grupo Azahar Hoteles» (cancelación, fidelización, preguntas frecuentes y normas) y un README con 6 preguntas de prueba y sus respuestas correctas. Son los de la demo de clase. |

### Lo que debería existir del día anterior

- El ADR, el diagrama y el esquema de S12 del producto del equipo (`entregable_S12/` o similar). Si no están, pregunta al equipo.

---

## Reglas de trabajo

1. Hoy **no se crea nada en la base de datos**: solo diseño y documentos.
2. **Pregunta antes de suponer** cualquier dato del negocio: tipos de documentos, volumen, permisos o número de clientes.
3. Cada decisión del blueprint va con **su porqué en una línea**.
4. Cuando propongas algo, ofrece **la opción más simple primero** y explica cuándo haría falta algo más complejo.
5. **Nunca muestres ni guardes claves.**

---

## FASE 0 · Contexto (5 minutos)

1. Lee los entregables de S12 del equipo y resume en 5 líneas: qué hace el producto, qué datos tiene y qué base de datos eligió.
2. Pregunta al equipo, una por una:
   - ¿Qué **documentos** consultaría el asistente (políticas, manuales, tickets, reseñas, contratos…)?
   - ¿Quién puede ver cada documento: público, empleados, solo su organización?
   - ¿Cada cuánto cambian?
   - ¿Cuántos clientes y cuántas consultas al mes esperáis?

---

## FASE 1 · Fuentes y permisos (10 minutos)

Construye con el equipo una tabla con estas columnas:

| Fuente | Tipo | Volumen aprox. | Frecuencia de cambio | Responsable | Quién puede verla |
|---|---|---|---|---|---|

Señala los **riesgos de privacidad**: datos personales en los documentos, separación entre clientes y derecho al olvido. Propón cómo tratar cada uno.

---

## FASE 2 · Router: ¿datos o documentos? (10 minutos)

1. Ayuda al equipo a escribir **al menos 10 preguntas reales** que harían sus usuarios.
2. Clasifica cada una:
   - **Datos (SQL):** cifras, recuentos, filtros exactos.
   - **Documentos (RAG):** políticas, opiniones, explicaciones.
   - **Ambos:** p. ej., «¿por qué ha bajado la nota del hotel de Málaga?».
3. Tabla final: **pregunta → camino → por qué**.
4. Recuerda la regla: **un RAG no cuenta ni suma**. Las cifras van a la base de datos, con permisos de solo lectura.

---

## FASE 3 · Pipeline (15 minutos)

Para cada caja, propón una opción, justifícala en una línea y pide al equipo que la confirme:

| Caja | Decisiones |
|---|---|
| **Extracción** | ¿Hay PDFs, tablas o escaneos? ¿Qué herramienta (texto directo, Docling, modelo multimodal)? |
| **Troceado** | Por tipo de documento: unidad natural (reseña, ticket, FAQ), por estructura (secciones de una política) o tamaño fijo. Tamaño orientativo de 300-800 tokens. ¿Hace falta troceado contextual? |
| **Metadatos** | Fuente, versión o fecha, organización, permisos, sección y atributos de negocio para filtrar. |
| **Embeddings y base de datos** | El modelo y la base de datos de S12. Mismo modelo para guardar y preguntar. |
| **Búsqueda** | Semántica o híbrida (significado + palabras). Recomendada: híbrida si hay códigos, nombres propios o referencias. Cuántos fragmentos (5 por defecto). |
| **Reranker** | Solo si la evaluación lo justifica; en el MVP, normalmente no. |
| **Respuesta** | Modelo (Gemini 3.8 Flash), instrucciones con rol, restricción a los fragmentos, frase exacta para «no lo encuentro», citas [n] y datos separados de las instrucciones. **Redacta las instrucciones completas.** |
| **Seguridad** | Filtro por organización en la búsqueda (no después), documentos tratados como datos y no como órdenes, y datos personales. |

---

## FASE 4 · Evaluación y coste (10 minutos)

1. **Golden set inicial:** propón 5 preguntas del dominio del equipo, al menos una de cada tipo (directa, varias fuentes, con filtro, cifras y sin respuesta), con su **respuesta correcta** y la fuente. **El equipo las valida.**
2. **Notas mínimas:** propón umbrales, por ejemplo fidelidad ≥ 4/5 y ≥ 80 % de respuestas correctas.
3. **Coste por consulta:** estima tokens de entrada (instrucciones + fragmentos + pregunta) y de salida, y calcula el coste con la tarifa vigente del modelo, indicando la fuente del precio. Después:
   - Coste por cliente al mes, con las consultas estimadas.
   - Comparación con el precio del plan del producto: **¿hay margen?**

---

## FASE 5 · Redactar el blueprint (5 minutos)

Genera `blueprint_S13.md` (**una página**) con estas secciones:

1. **Fuentes y permisos** (tabla de la fase 1).
2. **Preparación:** extracción, troceado, metadatos y actualización.
3. **Búsqueda:** embeddings, base de datos, semántica o híbrida, número de fragmentos y reranker.
4. **Router:** tabla de 10 preguntas.
5. **Respuesta:** modelo e instrucciones completas.
6. **Evaluación y coste:** golden set inicial, notas mínimas y coste por consulta y por cliente.

Añade un **diagrama Mermaid** del pipeline y una lista de **riesgos** con su mitigación.

**Comprobaciones:**
- [ ] Cabe en una página (más el diagrama).
- [ ] Cada decisión tiene su porqué.
- [ ] El filtro por cliente está en la búsqueda.
- [ ] Las preguntas de cifras van a la base de datos.
- [ ] El equipo sabe defender cada decisión sin mirar al agente.

---

## FASE 6 · (Opcional) Repetir la demo de File Search

Para entender un RAG gestionado antes de construir el vuestro:

- **Sin código:** en Google AI Studio, *Build → Gallery*, remezclad la app «Ask the Manual» (o cread una con *Build → New app*), subid los 4 documentos de `rag_demo/` y lanzad las 6 preguntas del README. La app necesita una API key de Gemini con facturación activada.
- **Con el agente:** pídele que cree un pequeño script que use la herramienta **File Search de la API de Gemini** con los 4 documentos y las 6 preguntas, y que guarde las respuestas y sus citas en una tabla. La clave va en `.env` como `GEMINI_API_KEY`.

Comparad las respuestas con las correctas del README. ¿Ha inventado algo en «¿el hotel tiene spa?»?

---

## Entregable (lunes 23 nov, 23:59)

- `blueprint_S13.md` con el diagrama.
- Tabla de router con al menos 10 preguntas.
- Golden set inicial de 5 preguntas validadas por el equipo.
- Coste estimado por consulta y por cliente al mes.

Se entrega junto con S12 y S14. **El blueprint es la especificación de mañana**: cuanto mejor sea, más rápido irá el lab.
