# Documentos para la demo de RAG (S13 · File Search)

Cuatro documentos **ficticios** de la cadena «Grupo Azahar Hoteles», la misma cadena ficticia del esquema de demo de S12. Sirven para subirlos a Google AI Studio (File Search) y hacer la demo de la sesión 13.

| Archivo | Contenido |
|---|---|
| `01_politica_cancelacion.md` | Tarifas flexible y no reembolsable, grupos, modificaciones, fuerza mayor |
| `02_programa_fidelizacion.md` | Niveles Verde/Plata/Oro, ventajas de cancelación, puntos |
| `03_faq_huespedes.md` | Check-in/out, mascotas, parking, desayuno, ruido, facturas |
| `04_normas_y_servicios.md` | Normas, servicios incluidos y de pago, accesibilidad, objetos perdidos |

## Guion de preguntas para la demo (con la respuesta correcta)

| # | Tipo | Pregunta | Respuesta correcta | Qué demuestra |
|---|---|---|---|---|
| 1 | Directa | «¿Hasta cuándo puedo cancelar gratis una reserva flexible?» | Hasta 48 horas antes de la llegada, a las 14:00 (doc. 01) | Respuesta con cita |
| 2 | Varios documentos | «Soy socio Oro: ¿hasta cuándo puedo cancelar gratis una tarifa flexible? ¿Y una no reembolsable?» | Flexible: hasta 24 h antes (doc. 02). No reembolsable: sin excepciones, no se devuelve (docs. 01 y 02) | Combinar dos fuentes |
| 3 | Con matiz | «Me han hospitalizado y tenía una tarifa no reembolsable, ¿pierdo el dinero?» | No: se emite un bono por el importe, válido 12 meses (doc. 01) | Encontrar una excepción |
| 4 | Sin respuesta | «¿El hotel tiene spa?» | No consta en la documentación | Que diga «no lo sé» en lugar de inventar |
| 5 | Cifras / contar | «¿Cuántas cancelaciones hubo en octubre?» | No está en los documentos; un RAG no cuenta | El gancho del router: las cifras van a la base de datos |
| 6 | Precio | «¿Cuánto me cuesta llevar a mi perro dos noches a Granada?» | 30 € (15 € por noche), solo en Granada Albaicín, perros de hasta 10 kg (doc. 03) | Respuesta precisa con condiciones |

Todos los datos (precios, plazos, emails `example.com`) son inventados.
