# Instrucciones para el agente · S15: forecasting con IA

> **Cómo usar este documento**
> Copia esta carpeta en tu proyecto y dile a tu agente:
> **«Lee INSTRUCCIONES_AGENTE.md y ejecuta la FASE 0. Para y espera mi confirmación al final de cada fase.»**
> El trabajo pesado se ejecuta en **Google Colab**, con GPU gratuita. El agente prepara el notebook o las celdas, y el equipo los ejecuta en Colab y revisa los resultados.

---

## Contexto para el agente

Eres el analista de datos de un equipo de producto que trabaja en modo *vibe-coding*. El equipo no lee código: necesita que **expliques cada paso en lenguaje llano** y que **demuestres** que lo has hecho bien.

Hoy hay dos objetivos:
1. **Lab guiado:** comparar un modelo fundacional de series temporales (**Chronos-2**, de Amazon, en zero-shot) con modelos sencillos sobre una serie real, con un backtest honesto.
2. **Trabajo en equipo:** decidir si el **producto del equipo** necesita una capa predictiva y, si es así, prototiparla y diseñarla.

### Archivos de esta carpeta

| Archivo | Contenido |
|---|---|
| `pernoctaciones_andalucia_mensual.csv` | `fecha, valor`: pernoctaciones hoteleras mensuales en Andalucía, de enero de 2010 a septiembre de 2026 (201 meses). Fuente: INE, Encuesta de Ocupación Hotelera, tabla 67190. |
| `pernoctaciones_provincias_mensual.csv` | `provincia, fecha, valor`: lo mismo para las 8 provincias andaluzas. |

### Lo que hay que saber de la serie

- **Estacionalidad muy marcada:** máximo en agosto (7,6 M en 2025) y mínimo en enero (2,3 M en 2025).
- **COVID:** abril de 2020 = **0** (hoteles cerrados), y 2020-2021 son muy atípicos.
- **Semana Santa** cambia de mes: marzo en 2024, abril en 2025, entre marzo y abril en 2026.
- **Listón de referencia:** el *ingenuo estacional* («el mismo mes del año anterior») tiene un **MAPE del 3,6 %** y un WAPE del 3,2 % en el backtest oficial (abajo).

### Backtest oficial (todos los modelos, sin excepción)

- **4 pruebas de 6 meses**, con cortes en 2024-09, 2025-03, 2025-09 y 2026-03.
- En cada prueba, el modelo solo ve los datos **hasta el corte** y predice los 6 meses siguientes.
- Meses evaluados: de octubre de 2024 a septiembre de 2026 (24 meses).
- Métricas: **MAPE** y **WAPE**, medias de las 4 pruebas.

---

## Reglas de trabajo

1. **Ninguna prueba puede usar datos posteriores a su corte** (fuga de datos). Explica en cada prueba dónde separas el pasado del futuro.
2. **Todos los modelos usan exactamente las mismas 4 pruebas.**
3. Si un modelo no bate al ingenuo estacional, **dilo con claridad**: es un resultado válido.
4. Explica cada celda del notebook en una frase, en un comentario o una celda de texto, en español y en lenguaje llano.
5. No uses servicios de pago ni envíes datos a terceros sin preguntar.

---

## FASE 0 · Diagnóstico de los datos (5 minutos)

Prepara una primera celda para Colab que:
1. Cargue `pernoctaciones_andalucia_mensual.csv`.
2. Compruebe: meses que faltan, duplicados, ceros y valores negativos.
3. Dibuje la serie completa.

Resume en 5 líneas lo que se ve: tendencia, estacionalidad y el shock de 2020.

**Comprobaciones:**
- [ ] 201 meses sin huecos ni duplicados.
- [ ] Detectado el cero de abril de 2020.

---

## FASE 1 · Modelos sencillos (lab guiado)

Prepara las celdas para calcular, con el backtest oficial:

| Modelo | Idea |
|---|---|
| Ingenuo | Repetir el último mes conocido |
| Ingenuo estacional | El mismo mes del año anterior |
| Suavizado exponencial (ETS) | Con estacionalidad anual (12 meses), usando la librería StatsForecast |

Muestra una tabla con el MAPE y el WAPE de cada uno.

**Comprobaciones:**
- [ ] El ingenuo estacional da ≈ 3,6 % de MAPE y ≈ 3,2 % de WAPE. Si no, hay un error en las ventanas: revísalo antes de seguir.
- [ ] ¿Bate el ETS al ingenuo estacional? ¿Por cuánto?

---

## FASE 2 · Chronos-2 en zero-shot (lab guiado)

Prepara las celdas (con la GPU T4 de Colab activada) para:

1. Instalar y cargar **Chronos-2** desde Hugging Face (`amazon/chronos-2`).
2. Predecir los 6 meses de cada prueba del backtest con **cuantiles 0,1, 0,5 y 0,9**, usando la mediana como predicción puntual.
3. Hacerlo **dos veces**:
   - **A:** con toda la historia desde 2010.
   - **B:** solo con la historia desde enero de 2022.
4. Añadir las dos versiones a la tabla de resultados.
5. Dibujar la última prueba: lo real, la predicción de Chronos-2 y la banda P10-P90, junto con el ingenuo estacional.
6. Calcular la **cobertura**: ¿qué % de los meses reales caen dentro de la banda P10-P90? Debería rondar el 80 %.

**Comprobaciones:**
- [ ] Mismas 4 pruebas que en la fase 1.
- [ ] Tabla final: ingenuo, ingenuo estacional, ETS, Chronos-2 A y Chronos-2 B.
- [ ] Conclusión en 3 líneas: ¿alguno bate el 3,6 %? ¿Qué historia funciona mejor y por qué?
- [ ] ¿En qué meses falla más cada modelo? (Pista: marzo y abril, por la Semana Santa.)

**Para quien termine antes:**
- **Variable externa:** añade a Chronos-2 una variable conocida de antemano, por ejemplo cuántos días de Semana Santa caen en cada mes, y comprueba si mejora en marzo y abril.
- **Varias series:** predice las 8 provincias a la vez con `pernoctaciones_provincias_mensual.csv` y di en cuáles bate Chronos-2 al ingenuo estacional.
- **Combinación:** prueba la media de Chronos-2 y ETS.

---

## FASE 3 · Trabajo en equipo: ¿nuestro producto necesita predecir? (45 minutos)

### 3.1 · Checklist «¿aplica?» (10 minutos)

Haz al equipo estas preguntas y anota las respuestas:

1. ¿Hay una **decisión de negocio** que cambie según el valor futuro? ¿Cuál y quién la toma?
2. ¿Habrá **historia con fechas** (al menos 2 ciclos) o datos públicos equivalentes?
3. ¿**Equivocarse es caro** (stock, personal, caja)?
4. ¿El usuario **actuaría** ante una predicción con rango?

Si la respuesta a la 1 es **no**, pasa directamente a redactar la **justificación de por qué no aplica** (una página). Es un entregable válido.

### 3.2 · Prototipo (20 minutos)

1. Identifica la serie a predecir con datos del equipo o con datos públicos equivalentes (INE, datos abiertos…). **Pregunta antes de descargar nada.**
2. Repite el lab con esa serie: diagnóstico, modelos sencillos, Chronos-2 y backtest con las mismas reglas (ajusta la frecuencia y la estacionalidad: diaria, semanal o mensual).
3. Tabla de resultados y conclusión: **¿bate al ingenuo estacional?**

### 3.3 · Diseño en el producto (10 minutos)

Redacta con el equipo:
- **Qué se predice**, con qué horizonte y para quién.
- **Qué decisión dispara** y cómo se muestra el rango P10-P90 **en lenguaje de decisión**. Ejemplo: «planifica personal para 6,7 M si no quieres quedarte corto».
- Un **boceto de la pantalla o la alerta**: descripción o maqueta HTML sencilla.

### 3.4 · Llevarlo al producto (5 minutos)

1. Propón una **tabla de predicciones** para el esquema de S12 con estas columnas:
   - organización, serie, fecha objetivo.
   - P10, P50, P90.
   - modelo y versión.
   - fecha de ejecución.
   Explica cada columna en una frase. **Se guardan todas las predicciones, no solo la última.**
2. Propón la **frecuencia** de ejecución (diaria, semanal o mensual) y cómo se vigilaría el error real frente al predicho.

---

## FASE 4 · Entregable (lunes 30 nov, 23:59)

Ayuda a preparar:

1. **Notebook de Colab** (enlace con permiso de lectura) con diagnóstico, modelos sencillos, Chronos-2 y backtest de 4 pruebas.
2. **Tabla de resultados** con el error por modelo y si bate al ingenuo estacional.
3. **Una página** con qué se predice, para quién, el horizonte, la decisión que dispara y el boceto de la pantalla.
4. La **tabla de predicciones** añadida al esquema y la frecuencia de ejecución.
5. **O BIEN:** la justificación argumentada de por qué no aplica (checklist de la fase 3.1).

Revisad juntos la lista de **errores clásicos** antes de entregar:

- [ ] No se evalúa con los datos de entrenamiento.
- [ ] Hay varias pruebas, no una sola.
- [ ] No se usa el MAPE si hay ceros (se usa el WAPE).
- [ ] Se tienen en cuenta los cambios de calendario.
- [ ] El horizonte es razonable para la historia disponible.
- [ ] Hay comparación con el ingenuo estacional.
