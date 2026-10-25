# Instrucciones para el agente · S12: NoSQL y bases de datos vectoriales

> **Cómo usar este documento**
> Copia esta carpeta en tu proyecto y dile a tu agente (Claude Code, Codex o Antigravity):
> **«Lee INSTRUCCIONES_AGENTE.md y ejecuta la FASE 0. Para y espera mi confirmación al final de cada fase.»**
> Cada fase termina con **comprobaciones** que el equipo verifica antes de seguir.

---

## Contexto para el agente

Eres el ingeniero de un equipo de producto que trabaja en modo *vibe-coding*: el equipo decide y revisa, y tú construyes y explicas.

Hoy hay dos objetivos:
1. **Lab guiado:** montar en Supabase una tabla de reseñas de hoteles con búsqueda por significado (pgvector + embeddings).
2. **Trabajo en equipo:** diseñar la base de datos del **producto del equipo** y justificar la decisión con una matriz de decisión ponderada.

### Archivos de esta carpeta

| Archivo | Para qué |
|---|---|
| `resenas_hoteles_andalucia_lab.csv` | 3.000 reseñas reales en español: `id, hotel, provincia, nota, titulo, texto` |
| `esquema_demo/` | Ejemplo de esquema con 4 tablas relacionadas (cadenas, hoteles, usuarios y reseñas) para ver un diagrama de entidades real. Tiene su propio README. |

### Lo que necesita el equipo

- Un proyecto de **Supabase** (plan gratuito, región Europa).
- Un archivo `.env` con `SUPABASE_URL`, `SUPABASE_SERVICE_ROLE_KEY` y `OPENAI_API_KEY`.
- Conectados al agente: el **Supabase MCP en solo lectura** y las **Supabase Agent Skills**.

### Modelo

`text-embedding-3-small` (OpenAI), 1.536 dimensiones. Es **el mismo** para guardar y para preguntar.

---

## Reglas de trabajo (obligatorias)

1. **Nunca muestres, imprimas ni guardes en archivos versionados ninguna clave.** Léelas del `.env` y comprueba que está en `.gitignore`.
2. **Antes de crear o cambiar algo en la base de datos, explícalo en lenguaje llano** (una frase por tabla, columna, índice o política) y espera la aprobación del equipo.
3. **Activa la seguridad por fila (RLS)** en todas las tablas que crees.
4. Si algo falla, **explica el error en lenguaje llano antes de arreglarlo**.
5. No escribas código en el chat salvo que el equipo lo pida: **explica qué has hecho y cómo comprobarlo.**

---

## FASE 0 · Diagnóstico (3 minutos)

1. Comprueba que el `.env` tiene las 3 claves, **sin mostrar sus valores**.
2. Con el MCP de solo lectura, comprueba que puedes conectarte al proyecto y lista las tablas que hay.
3. Lee `resenas_hoteles_andalucia_lab.csv` y resume: número de filas, columnas, reseñas por nota y por provincia.

**Comprobaciones:**
- [ ] Claves presentes.
- [ ] Conexión correcta.
- [ ] 3.000 reseñas con 6 columnas.

---

## FASE 1 · LAB guiado: búsqueda por significado (25 minutos)

### 1.1 · Preparar la base de datos

1. Activa la extensión **pgvector**.
2. Propón una tabla de reseñas con estas columnas:
   - `id`, `hotel`, `provincia`, `nota` (de 1 a 5, con una regla que impida otros valores), `titulo` y `texto`.
   - `embedding`: vector de 1.536 dimensiones.
   - `modelo_embedding`: qué modelo generó el vector.
3. **Explícanos cada columna en una frase** antes de crearla.
4. Activa la RLS.

### 1.2 · Cargar las reseñas

El equipo puede importar el CSV desde el panel de Supabase (Table Editor → Import data from CSV) o pedirte que lo cargues tú. En ambos casos, comprueba después que hay **3.000 filas**.

### 1.3 · Calcular los embeddings

1. Calcula el embedding de **`titulo` + `texto`** de cada reseña con `text-embedding-3-small`, en lotes de 100 y con reintentos si la API devuelve un error de límite.
2. Guárdalos en la columna `embedding` y rellena `modelo_embedding`.
3. Crea un **índice vectorial** (HNSW, distancia coseno).
4. Dinos **cuántos tokens se han usado y cuánto ha costado**. Debería rondar el céntimo.

### 1.4 · Primera búsqueda por significado

Crea una búsqueda que reciba una frase y devuelva las 5 reseñas más parecidas, con su similitud y filtros opcionales por **nota máxima** y por **provincia**. Pruébala con:

1. «no pudimos dormir por el ruido», sin filtros.
2. La misma, solo con reseñas de nota 1 o 2.
3. La misma, solo de Sevilla.

Enseña los resultados en una tabla y **señala las reseñas que no contienen las palabras "ruido" ni "dormir"**: son la prueba de que busca por significado.

**Comprobaciones:**
- [ ] 3.000 reseñas, todas con embedding.
- [ ] RLS activada en la tabla.
- [ ] Aparecen reseñas relevantes sin las palabras de la pregunta (p. ej., «paredes de papel», «se oía la calle»).
- [ ] Los filtros de nota y provincia se respetan.
- [ ] Coste anotado para el entregable.

**Para quien termine antes:**
- Prueba «habitación sucia» y busca si aparece alguna reseña con negación («no estaba nada sucia»). Es una trampa típica de los embeddings.
- Compara con una búsqueda por la palabra literal «ruido»: ¿qué reseñas se pierden?

---

## FASE 2 · (Opcional) Explorar el esquema de demo

Para ver un diagrama de entidades real antes de diseñar el vuestro:

1. En un **proyecto aparte** o en el mismo, ejecuta `esquema_demo/schema.sql` y carga los 4 CSV en orden: cadenas → hoteles → usuarios → reseñas.
2. Explícanos cada tabla y cada relación en una frase. Ejemplo: «una cadena tiene muchos hoteles».
3. Responde con el MCP de solo lectura a estas preguntas y compara con las respuestas esperadas del README:
   - Nota media por cadena.
   - Nota media por provincia.
   - Reseñas de nota 1 de Costa Luz en Sevilla.

---

## FASE 3 · Trabajo en equipo: la base de datos de NUESTRO producto (45 minutos)

### 3.1 · Preguntas de negocio (10 minutos)

Ayuda al equipo a listar **8-10 preguntas** que su producto hará a los datos y clasifícalas en cuatro tipos:

| Tipo | Ejemplo |
|---|---|
| Exacta | «Reseñas de este hotel con nota 1 o 2» |
| Agregada | «Nota media por provincia» |
| Por palabras | «Reseñas que contienen "parking"» |
| Por significado | «Quejas por ruido» |

Si ninguna pregunta es de significado, dilo: quizá el producto no necesita vectores, y eso también es una conclusión válida.

### 3.2 · Matriz de decisión ponderada (10 minutos)

Construye con el equipo la matriz para elegir entre **Supabase + pgvector**, **Firestore** y **una base vectorial dedicada**:

1. Criterios de partida:
   - Datos de negocio y vectores juntos.
   - Filtros exactos + significado.
   - Informes y cruces de datos.
   - Que cada cliente vea solo lo suyo.
   - Tiempo real y modo offline en móvil.
   - Más de 50 M de vectores.
   - Coste para el MVP.
   - Facilidad para el equipo.
2. **El equipo fija los pesos (1-5) ANTES de puntuar.** Tú no los propongas: pregunta.
3. Puntuad cada opción de 1 a 5 en cada criterio, con una justificación de una línea.
4. Calcula peso × puntuación, los totales y el máximo posible.
5. Si dos opciones quedan a menos de un 10 % de diferencia, señálalo y pregunta qué criterio debería desempatar.

### 3.3 · Esquema del producto (20 minutos)

Con las Supabase Agent Skills:

1. Propón las **entidades** del producto, sus **atributos** y sus **relaciones** (1:1, 1:N, N:M; las N:M necesitan una tabla intermedia).
2. Indica **qué textos llevan embedding y por qué** (y cuáles no: las notas, fechas o provincias van como filtros).
3. Propón la **separación por cliente**: un identificador de organización en cada tabla y políticas de seguridad por fila. Explica cada política en una frase.
4. Genera un **diagrama de entidades en Mermaid**.
5. Genera el **esquema propuesto** (archivo SQL o descripción tabla a tabla), sin aplicarlo todavía en la base de datos.

### 3.4 · Pitch (5 minutos)

Redacta con el equipo un pitch de 60 segundos: «elegimos X porque…», con los dos criterios que más pesaron.

**Comprobaciones:**
- [ ] Las preguntas de negocio justifican (o descartan) los vectores.
- [ ] Pesos fijados por el equipo antes de puntuar.
- [ ] Diagrama con relaciones correctas y separación por cliente.
- [ ] El equipo sabe explicar cada tabla sin mirar al agente.

---

## FASE 4 · Entregable (lunes 23 nov, 23:59)

Ayuda a preparar:

1. **ADR de una página** (Architecture Decision Record):
   - **Contexto:** producto, datos y las 8-10 preguntas.
   - **Opciones:** las tres, con la matriz.
   - **Decisión:** base de datos y modelo de embeddings, en 5 líneas como máximo.
   - **Consecuencias:** qué se gana, qué riesgos se asumen y cuándo se revisaría la decisión.
2. La **matriz de decisión ponderada**.
3. El **diagrama de entidades** (Mermaid o imagen).
4. El **esquema propuesto**: tablas, qué textos llevan embedding y reglas de seguridad por cliente.
5. Una **captura de la primera búsqueda por significado** (fase 1.4).

El equipo revisa y firma el ADR: **el criterio es suyo, no del agente.**
