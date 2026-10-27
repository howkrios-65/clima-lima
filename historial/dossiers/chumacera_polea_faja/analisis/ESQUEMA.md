# Esquema de entrega de los especialistas (modo de falla: chumacera de polea de faja transportadora)

Base de evidencia (única que puedes citar): /home/user/clima-lima/historial/dossiers/chumacera_polea_faja/evidencia.json (63 entradas; cada una con id, nivel_evidencia, extracto, afirma y limites)
y el dossier ya validado: /home/user/clima-lima/historial/dossiers/chumacera_polea_faja/dossier.json. LEE ambos antes de escribir.

## Reglas (todas obligatorias)
1. No hay caso real ni datos de planta. Prohibido inventar cifras, tasas, costos, probabilidades, puntajes S-O-D, fechas, referencias.
2. Cada ítem lleva `nivel`: "EVIDENCIA" (la fuente respalda directamente lo que dices) o "SINTESIS" (razonamiento de ingeniería del equipo a partir de premisas citadas).
   - En ambos casos `evidencia` es una lista NO vacía de ids que existan en evidencia.json y tengan nivel VERIFICADO-TEXTO o VERIFICADO-ABSTRACT.
   - Un ítem "SINTESIS" debe decir en `nota` cuál es el razonamiento y que debe ser validado por un experto del activo.
   - Los ids SOLO-SNIPPET y NO-VERIFICADO no pueden respaldar nada; solo pueden mencionarse en `pistas` como pendientes de abrir.
3. Un número solo puede aparecer si está en el extracto de una fuente que citas. Los campos numéricos que dependan del activo (severidad, ocurrencia, detección, probabilidades, costos, tasas) se dejan en null para que la persona o un experto los ingrese en el informe interactivo.
4. Lo que no tenga respaldo: lista `vacios` con el motivo. Mejor un vacío honesto que un relleno.
5. Escribe en español, sin nombres de empresas, sin el signo de sección y sin la palabra que la persona prohibió para nombrar al coordinador (di "estratega" o "líder").
6. Estados de causa/hipótesis: "posible" por defecto; "probable" o "confirmada" solo con evidencia del propio caso, que aquí NO existe: por tanto ninguna puede pasar de "posible".

## Formas JSON
fmeca: {"funcion": "...", "items": [{"id":"FM1","modo":"...","mecanismo":"...","efecto_local":"...","efecto_sistema":"...","causa":"...","deteccion":"técnica de la que habla la evidencia","control_sugerido":"...","severidad":null,"ocurrencia":null,"deteccion_puntaje":null,"nivel":"SINTESIS","evidencia":["E-...."],"nota":"..."}], "vacios":["..."]}
arbol: {"evento_tope":"...", "nodos":[{"id":"N0","texto":"...","puerta":"OR"|"AND"|"BASE","hijos":["N1","N2"],"probabilidad":null,"nivel":"SINTESIS","evidencia":["E-...."],"nota":"..."}], "vacios":["..."]}
acr: {"hipotesis":[{"id":"H1","texto":"...","estado":"posible","prueba_para_confirmar":"qué evidencia del activo la confirmaría o descartaría","evidencia":["E-...."],"nivel":"EVIDENCIA|SINTESIS","nota":"..."}], "ishikawa":{"Máquina":[{"texto":"...","evidencia":["E-..."],"nivel":"..."}],"Método":[],"Material":[],"Mano de obra":[],"Medición":[],"Medio ambiente":[]}, "ensayos":[{"ensayo":"...","para_hipotesis":["H1"],"evidencia":["E-..."]}], "vacios":["..."]}
lcc: {"elementos":[{"id":"C1","nombre":"...","tipo":"capex|opex|falla|indisponibilidad|repuesto|disposicion","como_se_calcula":"fórmula en texto","valor":null,"unidad":null,"nivel":"SINTESIS","evidencia":["E-..."],"nota":"..."}], "formulas":[{"nombre":"...","expresion":"...","evidencia":["E-..."]}], "vacios":["..."]}
vida: {"hallazgos":[{"id":"V1","texto":"...","nivel":"EVIDENCIA|SINTESIS","evidencia":["E-..."],"nota":"..."}], "metodo_recomendado":[{"situacion":"...","metodo":"...","porque":"...","evidencia":["E-..."]}], "vacios":["..."]}
predictivo: {"hallazgos":[{"id":"P1","texto":"...","nivel":"EVIDENCIA|SINTESIS","evidencia":["E-..."],"nota":"..."}], "estrategia":[{"etapa":"...","accion":"...","condicion_para_avanzar":"...","evidencia":["E-..."]}], "riesgos_de_validacion":[{"riesgo":"...","evidencia":["E-..."]}], "vacios":["..."]}
