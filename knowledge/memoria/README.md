# Memoria del equipo de confiabilidad, con compuertas

Principio: **el agente propone, una persona aprueba.** Ninguna lección entra a `aprobada/` por su cuenta.

## Flujo
```
agente  →  cuarentena/  →  G1 procedencia  →  G2 verificador independiente  →  G3 reglas  →  G4 persona  →  aprobada/
              (propone)     fuente + extracto    ¿contradice lo aprobado?       esquema,        obligatoria si
                                                 ¿lo soporta la fuente?         unidades,       cambia criterios
                                                                                duplicados      o acciones
```
Cualquier falla en una compuerta = rechazo con motivo. Los rechazos se destilan como lección separada.

## Esquema de un candidato (un archivo por memoria)
```
id: L-0000                  # correlativo
version: 1
tipo: semantica | episodica | procedimental | preferencia | referencia | leccion
enunciado: una frase verificable
alcance: tipo de activo o ámbito (sin nombres de empresa ni de planta)
fuente: archivo, URL, DOI o prueba del kit
extracto: cita literal o resultado reproducible
nivel_evidencia: VERIFICADO | CÁLCULO | SÍNTESIS ...
fecha_hecho: AAAA-MM-DD
valido_hasta: AAAA-MM-DD    # los estados de equipo caducan rápido
revisar_antes_de: AAAA-MM-DD
estado: propuesta | aprobada | retractada | reemplazada
propuesto_por: agente
aprobado_por: (persona)     # obligatorio para pasar a aprobada/
reemplaza: (id)             # no se sobrescribe, se reemplaza
```

## Reglas
- Memorias **procedimentales** (criterios, escalas, umbrales) siempre requieren aprobación humana y correr las pruebas del kit.
- Preferencias de formato pueden aprobarse citando la instrucción literal del usuario.
- Cada respuesta que use una memoria debe registrar su id y versión, para poder retractarla y re-evaluar.
- Ningún contenido recuperado de órdenes de trabajo, PDF o correos se guarda como memoria directa.
- La eficacia de esta política no está demostrada en mantenimiento: es una hipótesis de diseño que se valida con las pruebas del equipo.
