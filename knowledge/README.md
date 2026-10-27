# Base de conocimiento del equipo de confiabilidad

Todo lo que los agentes consultan en común vive aquí. Ningún agente inventa: cita de esta carpeta, del kit de cálculo
(`tools/reliability`) o de fuentes abiertas en la sesión.

| Archivo | Para qué sirve | Quién lo usa |
|---|---|---|
| `protocolo_comun.md` | Reglas de evidencia, formato de entrega y de preguntas que cumplen TODOS los agentes | Todos |
| `registro_normas.yaml` | Normas con edición citada y estado de verificación (por defecto NO verificadas) | Verificador, redactor, líder |
| `folklore_descartado.md` | Cifras muy repetidas sin fuente primaria: prohibido usarlas como evidencia | Todos |
| `plantillas/` | Estructura de cada tipo de informe (ACR, vida, FMECA, predictivo, tablero de KPIs) | Redactor |
| `memoria/` | Lecciones aprendidas con compuertas: `cuarentena/` (propuestas) y `aprobada/` (solo con aprobación humana) | Curador de memoria |

Cómo crece esta carpeta: los agentes **proponen**, una persona **aprueba**. Un cambio en `registro_normas.yaml` solo sube un
estado a VERIFICADO si alguien abrió la página oficial del publicador y anotó la fecha.
