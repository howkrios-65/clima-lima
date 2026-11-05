"""Construye evidencia.json, dossier.json, extra.json, abstract.json, trazabilidad.json y meta.json del caso.
Ejecutar: python3 -I construir_caso.py   (desde un directorio distinto; usa rutas absolutas)
Todas las fuentes externas son SOLO-SNIPPET (resumen de buscador del 2026-11-05): no respaldan cifras ni entran al dossier validado.
"""
import json, sys
from pathlib import Path
sys.path.insert(0, "/home/user/clima-lima/tools/reliability")
from reliability_kit.evidence import Ledger
from reliability_kit import dossier as dz

C = Path("/home/user/clima-lima/historial/dossiers/sello_marco_filtro_prensa_elastomeros")
F = "2026-11-05"

def usr(i, afirma, limites):
    return {"id": i, "tipo": "dato_usuario", "fecha_acceso": F, "via": "imagen_aportada",
            "referencia": {"titulo": "Material aportado por la persona (captura de una presentación interna)"}, "afirma": afirma, "limites": limites}

def snip(i, titulo, url, afirma, limites, tipo="otro", fuente=None, anio=None, autores=None):
    ref = {"titulo": titulo, "url": url}
    if fuente: ref["fuente"] = fuente
    if anio: ref["anio"] = anio
    ref["autores"] = autores or "Autor no identificado"
    return {"id": i, "tipo": tipo, "acceso": "snippet", "via": "websearch", "fecha_acceso": F, "referencia": ref, "afirma": afirma, "limites": limites}

LIM = "Solo resumen de buscador (SOLO-SNIPPET): la página no se abrió; no respalda cifras ni valores. "
E = [
 usr("E-0001", "Tabla 3 aportada: comparación de NR, NBR, EPDM y SBR con estrellas de 1 a 5 o X en resistencia mecánica, química, a aceites, al ozono/intemperie y al calor, y costo relativo.",
     "Sin fuente primaria declarada; es una pista de la persona, no evidencia. Las estrellas no tienen escala, norma ni condición de ensayo declaradas."),
 usr("E-0002", "Plano de la sección del perfil del sello de marco (pieza 2): elastómero sobre base metálica; cotas legibles en mm, transcritas una por una: 36, 25, 13, 11, 9, 6, 2, 19, 19 y 44 (cota total aparte; el hueco central entre los dos tramos de 19 no tiene cota legible).",
     "Sin tolerancias, sin norma del plano y sin material indicado en la imagen; las cotas son pista de geometría."),
 usr("E-0003", "Diapositiva 'Validación de prueba de dureza': el texto visible dice que se verifica que la dureza de los sellos nuevos no exceda los 62 +/- (texto cortado).",
     "El valor completo, la tolerancia, la escala (Shore) y la norma del ensayo no se ven: SIN DATOS; no se completan."),
 snip("E-1001", "Patente: tira de sellado entre ensambles de placas adyacentes de un filtro prensa", "https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/12616923",
      "Según el resumen: por los ciclos repetidos de compresión y la naturaleza a menudo abrasiva del lodo, la tira de sellado es una pieza de desgaste que debe reemplazarse periódicamente; menciona una carga lineal de diseño del orden de 30 a 300 N/mm.",
      LIM + "Es una patente de un diseño concreto, no un estudio de campo ni una estadística de fallas.", fuente="Oficina de patentes de EE. UU."),
 snip("E-1002", "Patente: pieza de salida para filtro horizontal de placas y marcos (filtro de torre)", "https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/12496538",
      "Según el resumen: el desgaste se atribuye a la abrasividad de las partículas finas del lodo, y el lodo que llega a la interfaz placa-cuba puede viajar por debajo por capilaridad, agravado por los ciclos de compresión.",
      LIM + "Patente de una pieza distinta del sello de marco; sirve solo como plausibilidad del mecanismo.", fuente="Oficina de patentes de EE. UU."),
 snip("E-1003", "Guía de mantenimiento de placas de filtro prensa: calendario de inspección, señales de falla y cuándo reemplazar", "https://getchemready.com/?p=16469",
      "Según el resumen: el alabeo de placa por ciclos térmicos desiguales, carga parcial del paquete o sobrepresión causa paso por la superficie de sello, filtrado turbio y torta más húmeda; recomienda inspección anual del paquete completo y señala la holgura visible entre placas como indicador.",
      LIM + "Contenido de proveedor/marketing; el intervalo anual no es de un estudio.", fuente="Sitio de proveedor de insumos químicos"),
 snip("E-1004", "Preguntas frecuentes sobre filtros prensa (empaquetaduras)", "https://www.filtersource.com/blog/faqs-about-filter-presses",
      "Según el resumen: la fuga persistente a presión normal de cierre puede indicar que hay que reemplazar empaquetaduras; la vida depende de la duración del ciclo, la temperatura y la fuerza de cierre excesiva; reemplazar al delaminar o deshilacharse; estirar la junta para ajustarla abre la unión a tope; las nuevas pueden pegarse y salirse de la ranura.",
      LIM + "Texto de proveedor, sin datos de fallas ni muestra; no distingue material.", fuente="Blog de proveedor de filtros prensa"),
 snip("E-1005", "Documento de solución de problemas de filtros (fuga por anillo cuádruple del alimentador central)", "https://www.scribd.com/document/445403229/Filter-troubleshooting",
      "Según el resumen: la fuga por el sello de anillo cuádruple del alimentador central suele deberse a un contratuerca flojo; recomienda verificar fugas durante el llenado y la circulación.",
      LIM + "Sitio de documentos de terceros bloqueado en este entorno; es otro sello (alimentación), no el de marco.", fuente="Documento de terceros"),
 snip("E-1006", "Guía sobre prevención de fallas de empaquetaduras, parte 1", "https://blog.marianinc.com/blog/preventing-gasket-failure-part-1",
      "Según el resumen: lista la deformación permanente por compresión (compression set) entre las propiedades clave al elegir material, junto con abrasión y degradación UV.",
      LIM + "Guía general de sellado de gabinetes, no de filtros prensa.", fuente="Blog de proveedor de materiales"),
 snip("E-1007", "Empaquetaduras de intercambiadores de placas (artículo de revista técnica)", "https://www.pumpsandsystems.com/gaskets-plate-heat-exchangers?page=1",
      "Según el resumen: hinchamiento o ablandamiento indica incompatibilidad química; endurecimiento o decoloración indica degradación química o por temperatura; EPDM y NBR toleran limpiezas cáusticas y ácidas habituales a concentración y temperatura adecuadas; el exceso de concentración o temperatura daña rápido; menciona ASTM D6284.",
      LIM + "Intercambiadores de placas: es una analogía, no un filtro prensa; el resumen no da fecha ni autoría.", fuente="Revista técnica de bombas y sistemas"),
 snip("E-1008", "Comparación de compuestos de caucho: SBR, EPDM, nitrilo, neopreno y caucho natural", "https://rubberco.co.uk/pages/rubber-compound-comparison-guide-uk",
      "Según el resumen de la búsqueda (varias páginas de proveedores): EPDM es mucho más resistente al calor, la luz y el ozono que NR y SBR por su cadena saturada; NBR es la mejor de las cuatro frente a aceites minerales y EPDM es pobre en petróleo; NBR tiene resistencia comparativamente baja al ozono; una fuente dice que la temperatura de SBR es similar a la de EPDM, lo que contradice a otras.",
      LIM + "Atribución exacta a esta página no confirmada: el resumen mezcla varias páginas de proveedores generales; sin escala ni método de ensayo.", fuente="Sitio de proveedor de cauchos"),
 snip("E-1009", "Tabla de resistencia química de cauchos (proveedor)", "https://esrubber.com/products/chemical-resistance-table/",
      "Según el resumen: tabla de resistencia química que califica NR y SBR al fondo en combustible y aceite mineral y NBR cerca del tope; la escala de calificación no se ve en el resumen.",
      LIM + "Escala no confirmada; no se abrió la tabla.", fuente="Sitio de proveedor de cauchos"),
 snip("E-1010", "Aspectos de predicción de vida de juntas tóricas a partir de ensayos de envejecimiento de cinco años", "https://opus4.kobv.de/opus4-bam/frontdoor/index/index/docId/51060",
      "Según el resumen: juntas de HNBR, EPDM y FKM envejecidas comprimidas y sin comprimir hasta cinco años; la deformación permanente de equilibrio empeoró más rápido y más fuerte que la dureza y se usó para predecir vida por superposición tiempo-temperatura; la predicción precisa exigió más de tres años de datos.",
      LIM + "Juntas tóricas a temperaturas de 23 a 150 °C: no es un sello de marco ni lodo; no incluye NR, NBR ni SBR en el resumen.", fuente="Instituto federal alemán de materiales (repositorio)"),
 snip("E-1011", "Trabajo de fin de carrera: envejecimiento de empaquetaduras de intercambiadores de placas (EPDM y NBR)", "https://repositorio.ufsc.br/bitstream/123456789/262271/1/TCC_-_Fernando_Bernardes_Silva_Salvador.pdf",
      "Según el resumen: empaquetaduras ensayadas a temperatura elevada con superposición tiempo-temperatura y Arrhenius sobre la deformación permanente; concluye que las de EPDM resisten más el envejecimiento termo-oxidativo y tienen mayor vida que las de NBR.",
      LIM + "Trabajo de grado de universidad brasileña en intercambiadores de placas; no es un filtro prensa ni lodo; no evaluó NR ni SBR en el resumen.", fuente="Universidad Federal de Santa Catarina (repositorio)"),
 snip("E-1012", "Predicción de vida de materiales de sellado de EPDM con envejecimiento térmico bajo compresión constante", "https://ouci.dntb.gov.ua/works/42rdAzj4",
      "Según el resumen: modelo cinético con Arrhenius a partir de la deformación permanente a 80, 100 y 120 °C; la vida extrapolada a 25 °C depende mucho del criterio de fin de vida elegido para la deformación permanente.",
      LIM + "Solo EPDM, en aire y en laboratorio; la extrapolación a baja temperatura es discutida (ver E-1013).", fuente="Índice de citas de terceros"),
 snip("E-1013", "Evidencia de que el comportamiento Arrhenius de una junta tórica de EPDM a alta temperatura no se extrapola a baja temperatura", "https://www.osti.gov/biblio/917488",
      "Según el título y el resumen: la extrapolación Arrhenius desde altas temperaturas puede fallar en EPDM a baja temperatura.",
      LIM + "Solo título y resumen; actas de congreso de 1997 según el resumen.", fuente="OSTI (repositorio del Departamento de Energía de EE. UU.)"),
 snip("E-1014", "Resumen de búsqueda sobre poliuretano frente a caucho, FKM y silicona (varias páginas de proveedores)", "https://mearthane.com/polyurethane-versus-rubber/",
      "Según los resúmenes: proveedores afirman que el poliuretano resiste mucho más la abrasión que el caucho natural, que FKM tiene mejor resistencia química y térmica y abrasión moderada, y que la silicona es pobre a la abrasión; ninguna fuente probó sellos en lodo.",
      LIM + "Afirmaciones de proveedores de poliuretano y selladores, sin método ni valores verificables; la atribución a esta página concreta no se confirmó.", fuente="Sitio de proveedor de poliuretano"),
 snip("E-1015", "ASTM D2240, Rubber Property - Durometer Hardness (listado)", "https://webdesk.jsa.or.jp/link/annualbook/astm24_0901.pdf",
      "Según el listado: el título es 'Rubber Property - Durometer Hardness'; designación vista en el listado, edición NO-VERIFICADO.", LIM + "Edición no verificada en la página oficial; alcance y procedimiento no leídos.", tipo="norma", fuente="Listado de un proveedor (no es el emisor de la norma)"),
 snip("E-1016", "ASTM D395, Rubber Property - Compression Set (listado)", "https://coirubber.com/?p=64158",
      "Según el listado: título 'Standard Test Methods for Rubber Property - Compression Set'; designaciones vistas en el listado, edición NO-VERIFICADO; el método A comprime la muestra entre placas rígidas.",
      LIM + "Edición vigente no verificada en la página oficial; condiciones de ensayo no leídas.", tipo="norma", fuente="Listado de un proveedor (no es el emisor de la norma)"),
 snip("E-1017", "ASTM D471, Rubber Property - Effect of Liquids (listado)", "https://coirubber.com/rubber-property-effects-of-liquids-d471/",
      "Según el listado: título 'Rubber Property - Effect of Liquids'; evalúa la capacidad comparativa de cauchos de resistir el efecto de líquidos; designación vista en el listado, edición NO-VERIFICADO.",
      LIM + "Edición vigente no verificada en la página oficial.", tipo="norma", fuente="Listado de un proveedor (no es el emisor de la norma)"),
 snip("E-1018", "ASTM D1149, Rubber Deterioration - Cracking in an Ozone Controlled Environment (listado)", "https://webdesk.jsa.or.jp/link/annualbook/astm24_0901.pdf",
      "Según el listado: título 'Rubber Deterioration - Cracking in an Ozone Controlled Environment'; designación vista en el listado, edición NO-VERIFICADO.",
      LIM + "Edición vigente no verificada en la página oficial.", tipo="norma", fuente="Listado de un proveedor (no es el emisor de la norma)"),
]
L = Ledger(E)
L.to_json(C / "evidencia.json")

SIN = "SIN DATOS PARA ARMARLO. "
def vac(motivo, nota=None):
    d = {"elementos": [], "vacio": motivo}
    if nota: d["nota"] = nota
    return d
D = {"modo_falla": "sello de marco de un filtro de prensa de placas: falla del elastómero (NR, NBR, EPDM, SBR y alternativas)", "secciones": {
 "mediciones": vac(SIN + "Ninguna fuente leída da variables medibles ni sus curvas para el sello de marco. Lo que lo cerraría: texto completo de una guía de inspección de sellos de filtros prensa o de ASTM D2240 y D395.",
     "Pistas SOLO-SNIPPET: holgura visible entre placas (E-1003) y fuga (E-1004), dureza y deformación permanente como indicadores (E-1006, E-1010). La dureza máxima de sellos nuevos del material aportado está cortada (E-0003)."),
 "fenomenos": vac(SIN + "Compression set, abrasión por lodos, ataque químico e hinchamiento, ozono y calor, extrusión y fatiga por ciclos de presión: solo hay resúmenes de buscador; ninguna fuente se abrió. Lo que lo cerraría: lectura de texto completo de las patentes y de un estudio de envejecimiento de elastómeros (dominios de red a habilitar).",
     "Pistas SOLO-SNIPPET: desgaste por ciclos y lodo abrasivo (E-1001, E-1002); capilaridad del lodo bajo la interfaz (E-1002); deformación permanente (E-1006, E-1010 a E-1012); hinchamiento y endurecimiento (E-1007). Extrusión del sello y fatiga por ciclos de presión: ninguna pista hallada."),
 "top_fallas": vac(SIN + "No se halló estadística publicada de modos de falla de sellos de marco con base de datos, tamaño y año. Lo que lo cerraría: órdenes de trabajo propias o un estudio de campo de filtros prensa."),
 "fmeca": vac(SIN + "Las escalas S-O-D no se inventan y no hay datos de operación ni de falla. Se lista una tabla de candidatos de modo de falla (pista, estado posible) en el informe, sin puntuación. Lo que lo cerraría: sesión de expertos con el fluido, la presión, el ciclo y el historial de cambios."),
 "confiabilidad": vac(SIN + "No hay datos propios de vida de sellos ni conjuntos abiertos citables; ningún parámetro de Weibull se calcula. Lo que lo cerraría: fechas de instalación y retiro de sellos (con los que siguen en servicio como censurados) o un conjunto abierto de vida de sellos."),
 "punto_optimo": vac(SIN + "Sin costos aportados ni vida observada. Estructura del cálculo: costo por unidad de tiempo C(T) = [Cp + Cf x F(T)] / (integral de la confiabilidad de 0 a T), con Cp costo de reemplazo preventivo y Cf costo de la falla; el modelo no se evalúa y su fuente no se leyó."),
 "lcc": vac(SIN + "Sin costo de sello, mano de obra, parada ni fuga aportados. Estructura: LCC por opción de material = costo de adquisición + reemplazos esperados x costo de reemplazo + paradas y fugas esperadas x su costo, a valor presente; todos los términos son VACÍO hasta recibir costos."),
 "vida_util": vac(SIN + "No se leyó vida de diseño ni experiencia publicada de sellos de marco. Pista: la vida depende de la duración del ciclo, la temperatura y la fuerza de cierre (E-1004, SOLO-SNIPPET)."),
 "ibr": vac(SIN + "No se encontró un marco de inspección basada en riesgo aplicable a sellos de filtros prensa en fuentes leídas. Pista: inspección anual del paquete de placas y registro de fugas (E-1003, E-1004; contenido de proveedor)."),
 "ml": vac(SIN + "No hay datos de condición ni de falla del sello ni estudios leídos de aprendizaje automático sobre sellos de filtros prensa; no se justifica un modelo sin datos."),
 "acr": vac(SIN + "Sin caso real no hay causa raíz por encima de posible. Candidatos posibles (pistas): sobrecompresión o carga desigual de cierre (E-1003, E-1004), incompatibilidad química con el lodo o el lavado (E-1007), lodo abrasivo (E-1001, E-1002), instalación con estirado de la junta (E-1004)."),
 "troubleshooting": vac(SIN + "Ningún procedimiento de diagnóstico se leyó. Pistas SOLO-SNIPPET: fuga persistente a presión normal de cierre, filtrado turbio, holgura visible entre placas, delaminado o deshilachado (E-1003, E-1004)."),
 "mpd_normas": vac(SIN + "Ninguna norma se leyó en la página oficial. Candidatas con edición vista solo en listados de terceros: ASTM D2240 (dureza), D395 (deformación permanente), D471 (efecto de líquidos), D1149 (ozono); ASTM D6284 mencionada en E-1007; ASTM D2000 (clasificación de cauchos) y ISO 815, ISO 1817, ISO 868 no verificadas.",
     "Estado: NO-VERIFICADO en las cuatro candidatas (E-1015 a E-1018: solo vistas en listados de proveedor, SOLO-SNIPPET). Ninguna está en el registro de normas del equipo y no se cita edición ni año; ISO 815, ISO 1817, ISO 868, ASTM D2000 y D6284 se mencionan sin ninguna entrada de evidencia y quedan NO-VERIFICADO."),
 "referencias": vac(SIN + "Ninguna fuente externa alcanzó VERIFICADO-ABSTRACT: no hay referencias respaldadas. Las pistas se listan en la pestaña Evidencia con su nivel SOLO-SNIPPET y su enlace."),
}}
(C / "dossier.json").write_text(json.dumps(D, ensure_ascii=False, indent=1), encoding="utf-8")
v = dz.validar_dossier(D, L)
print("validar_dossier:", v)

def ids(*a): return list(a)
tablas = [
 {"titulo": "Contraste de la tabla de estrellas aportada contra las pistas halladas (ninguna fila queda confirmada)",
  "evidencia": ["E-0001", "E-1007", "E-1008", "E-1009", "E-1011"],
  "columnas": ["Fila de la tabla aportada", "Valores aportados (NR / NBR / EPDM / SBR)", "Qué dicen las pistas SOLO-SNIPPET", "Estado del contraste"],
  "filas": [
   ["Resistencia mecánica", "5 / 4 / 3 / 3", "Ninguna pista halló una comparación de resistencia mecánica entre los cuatro; el único dato cercano compara poliuretano con caucho natural en abrasión, y es un dicho de proveedor", "SIN RESPALDO (falta fuente)"],
   ["Resistencia química", "2 / 3 / 4 / 1", "Solo hay una pista (E-1007) según la cual EPDM y NBR toleran limpiezas cáusticas y ácidas habituales; ninguna pista compara la resistencia química de los cuatro materiales. Depende del fluido, que no se conoce", "SIN RESPALDO (ninguna pista ordena los cuatro materiales; depende del fluido)"],
   ["Resistencia a aceites", "X / 5 / X / X", "NBR es la mejor de las cuatro frente a aceites minerales; EPDM es pobre en petróleo; NR y SBR al fondo en una tabla de proveedor cuya escala no se vio", "Coincide con una pista no leída (resumen de buscador; no es contraste)"],
   ["Ozono e intemperie", "1 / 1 / 5 / 1", "EPDM mucho más resistente que NR y SBR; NBR baja en ozono", "Coincide con una pista no leída (resumen de buscador; no es contraste)"],
   ["Resistencia al calor", "2 / 3 / 4 / 2", "EPDM mejor que NR y SBR y mejor que NBR en envejecimiento termo-oxidativo (trabajo de grado en intercambiadores de placas); una fuente dice que SBR es similar a EPDM", "Pistas en conflicto para SBR; la ordenación EPDM sobre NBR viene de un trabajo en intercambiadores de placas, de otro alcance, no un contraste"],
   ["Costo", "medio / medio / medio-alto / bajo", "Ninguna pista halló costos de estos cuatro materiales", "SIN RESPALDO (y el costo real lo aporta la persona)"],
  ],
  "nota": "Las estrellas son un dato aportado sin fuente: no cuentan como evidencia. Ninguna fila se marca como confirmada porque ninguna fuente se abrió; ninguna se marca como contradicha por la misma razón. La fila de calor es la única con conflicto entre pistas."},
 {"titulo": "Otros materiales mencionados por la literatura de la búsqueda (solo pistas cualitativas; propiedades numéricas SIN DATOS PARA ARMARLO)",
  "evidencia": ["E-1014", "E-1010"],
  "columnas": ["Material", "Pista cualitativa (SOLO-SNIPPET)", "Qué cerraría el vacío numérico"],
  "filas": [
   ["FKM", "Mejor resistencia química y térmica; abrasión moderada (dicho de proveedores); incluido en el programa de envejecimiento de juntas tóricas", "Ficha técnica leída o ASTM D2000 verificada con rangos de temperatura y fluidos"],
   ["Silicona (VMQ)", "Amplio rango de temperatura pero abrasión pobre: mal ajuste para lodo abrasivo (dicho de proveedores)", "Ficha técnica leída o texto completo de una guía de selección"],
   ["Poliuretano", "Muy superior al caucho natural en abrasión según proveedores; menos adecuado a químicos agresivos; ningún ensayo en lodo", "Ensayo de abrasión DIN o Taber con la mezcla real, o estudio arbitrado leído"],
   ["HNBR", "Solo aparece en el programa de envejecimiento de juntas tóricas; sin pista sobre filtros prensa", "Fuente leída que lo compare con NBR en el fluido de la persona"],
  ],
  "nota": "No se publica ningún rango de temperatura ni dureza por material: ninguna ficha ni norma se leyó. La dureza del sello aportado (62 +/- tolerancia cortada) no se completa."},
 {"titulo": "Candidatos de modo de falla del sello de marco (estado: posible; pistas, sin puntuación S-O-D)",
  "evidencia": ["E-1001", "E-1002", "E-1003", "E-1004", "E-1006", "E-1007"],
  "columnas": ["Candidato", "Mecanismo sugerido por la pista", "Síntoma observable", "Qué confirmaría el caso"],
  "filas": [
   ["Desgaste por abrasión del lodo", "Ciclos repetidos de compresión y partículas finas abrasivas (E-1001, E-1002)", "Pérdida de perfil y fuga por el borde", "Medición del perfil contra el plano (cotas 36, 25, 13, 11, 9, 6, 2 mm aportadas) y análisis granulométrico del lodo"],
   ["Deformación permanente (compression set)", "Pérdida de recuperación elástica bajo compresión sostenida y calor (E-1006, E-1010 a E-1012)", "Fuga a presión normal de cierre; perfil aplastado", "Dureza y altura del sello usado frente a uno nuevo; ensayo ASTM D395 con edición verificada"],
   ["Ataque químico: hinchamiento o endurecimiento", "Incompatibilidad con el lodo o el lavado, o temperatura excesiva (E-1007)", "Ablandamiento, hinchamiento, endurecimiento o decoloración", "Composición del fluido, pH, temperatura y prueba de inmersión (ASTM D471)"],
   ["Instalación y carga de cierre", "Junta estirada, carga desigual o excesiva, alabeo de placa (E-1003, E-1004)", "Unión abierta, holgura entre placas, paso por un lado", "Registro de instalación y presión de cierre; planitud de placa"],
   ["Ozono e intemperie", "Agrietamiento superficial de gomas insaturadas (E-1008)", "Grietas en piezas almacenadas o expuestas", "Almacenamiento y exposición; ASTM D1149 con edición verificada"],
   ["Extrusión y fatiga por ciclos de presión", "Sin pista hallada", "SIN DATOS", "Fuente leída o inspección del sello usado"],
  ],
  "nota": "Hipótesis por encima de 'posible' exigen un caso real. Esto es síntesis del equipo a partir de pistas de buscador y de patentes, no una estadística de fallas."},
 {"titulo": "Geometría aportada del perfil del sello de marco (pista, sin tolerancias)",
  "evidencia": ["E-0002"],
  "columnas": ["Cota legible en el plano (mm)", "Nota"],
  "filas": [["36", "Cota total superior"], ["25", "Cota intermedia superior"], ["13, 11, 9, 6", "Alturas de la zona de elastómero (lectura de la imagen; su correspondencia exacta no está confirmada)"], ["2", "Probable espesor de la base metálica (lectura de la imagen, no confirmada)"], ["19, 19 y 44", "Dos tramos de 19 mm a cada lado de un hueco central y, aparte, la cota total de 44 mm. 19 + 19 = 38, no 44: el hueco central no tiene cota legible (SIN DATOS)"]],
  "nota": "Sin tolerancias, sin norma del plano y sin material indicado. La dureza del texto cortado de la diapositiva es '62 +/ ...': valor y tolerancia SIN DATOS."},
 {"titulo": "Estructura del cálculo económico (sin cifras)",
  "evidencia": ["E-0001"],
  "columnas": ["Término", "Definición", "Valor"],
  "filas": [["Cp", "Costo de reemplazo preventivo del sello de marco (pieza, mano de obra, tiempo de parada)", "VACÍO: lo aporta la persona"], ["Cf", "Costo de una falla (fuga, limpieza, parada no planificada, daño a placas o telas)", "VACÍO: lo aporta la persona"], ["F(T), R(T)", "Distribución de vida del sello (Weibull solo con datos citables o propios, con censura)", "VACÍO: sin datos de vida"], ["Material", "Costo relativo por material: la tabla aportada dice bajo/medio/medio-alto, sin cifras", "VACÍO"]],
  "nota": "Ningún cálculo se ejecutó: el kit exige costos y vida observada."},
]
vacios = [
 "Conector de artículos: no se pudo consultar la cuota (getUsageLimit no está disponible para este agente) ni usar search_wiley_fulltext; no se gastó cuota. La cuota debe comprobarse desde la sesión del LÍDER.",
 "Red: los dominios de revistas, repositorios, fabricantes, ASTM y ISO no resuelven en este entorno (ENOTFOUND o 403); ninguna página se abrió; toda fuente externa es SOLO-SNIPPET.",
 "Dureza de sellos nuevos de la diapositiva: valor y tolerancia cortados en la imagen; escala y norma de ensayo no indicadas.",
 "Propiedades numéricas por material (rangos de temperatura, dureza típica, deformación permanente, hinchamiento): SIN DATOS PARA ARMARLO.",
 "Datos de operación (fluido, pH, temperatura, presión de cierre y de filtración, abrasividad, ciclos) y de fallas (OT): ninguno aportado.",
 "Cuartiles y citas de las fuentes: no obtenibles en este entorno.",
]
supuestos = ["Sin caso real: ningún dato de planta se usó. La tabla de estrellas, el plano y la diapositiva de dureza son datos aportados sin fuente primaria (DATO-USUARIO): son pistas y no respaldan cifras.",
             "El activo se llama filtro de prensa de placas y el sello, sello de marco (sello entre placa y marco), según la lectura de las imágenes aportadas.",
             "No se recomienda ningún material definitivo: faltan fluido, pH, temperatura, presión, abrasividad y ciclos."]
preguntas = [
 "1. Condiciones de operación: ¿qué fluido o pulpa filtra (pH, temperatura, % sólidos y su abrasividad), qué presión de cierre y de filtración usa, y cuántos ciclos por día? Por defecto asumimos que no se conocen y el material queda sin recomendar.",
 "2. Sello actual: ¿cuál es el material y la dureza de los sellos instalados, el valor completo y la tolerancia de la diapositiva de dureza (62 +/ ...), la escala y la norma del ensayo, y la norma del plano?",
 "3. Historial: ¿tiene fechas de instalación y retiro de sellos de marco y el modo de falla observado (fuga, desgaste, aplastamiento, hinchamiento, agrietado), incluidos los que siguen en servicio? Con eso se puede estimar la vida con censura.",
 "4. Costos: ¿cuánto cuesta cada material de sello, la hora de parada, la mano de obra y una fuga o daño asociado? Sin eso el LCC y el punto óptimo quedan VACÍO.",
 "5. Acceso a fuentes: ¿puede habilitar en la red los dominios de revistas, ASTM, ISO y tesis (lista en el mapa de fuentes), o adjuntar los PDF de fichas técnicas y normas, y confirmar la cuota del conector de artículos (renovada el 2026-11-01 según las notas)?",
]
(C / "extra.json").write_text(json.dumps({"tablas": tablas, "vacios": vacios, "supuestos": supuestos, "preguntas": preguntas}, ensure_ascii=False, indent=1), encoding="utf-8")

abstract = {"titulo": "Falla del sello de marco de un filtro de prensa de placas y comparación de elastómeros (NR, NBR, EPDM, SBR): qué se pudo leer y qué falta",
 "autor": "HOWK RIOS - CONFIABILIDAD",
 "parrafos": [
  "Problema. El sello de marco sella el paquete de placas de un filtro de prensa; su falla produce fuga, filtrado turbio y parada. La persona aportó una tabla de estrellas que compara NR, NBR, EPDM y SBR, el plano de la sección del perfil y una diapositiva de dureza cortada; son datos sin fuente primaria y no cuentan como evidencia {E-0001} {E-0002} {E-0003}.",
  "Lo hallado. En este entorno ninguna página científica, de norma o de fabricante pudo abrirse; todo lo externo es resumen de buscador (SOLO-SNIPPET) y no respalda cifras. Las pistas apuntan a desgaste por ciclos de compresión y lodo abrasivo {E-1001} {E-1002}, deformación permanente {E-1006} {E-1010}, ataque químico con hinchamiento o endurecimiento {E-1007} y errores de instalación y de carga de cierre {E-1003} {E-1004}.",
  "Comparación de materiales. Frente a esas pistas, las filas de aceites y de ozono de la tabla aportada coinciden con pistas no leídas {E-1008} {E-1009}, lo que no es contraste; la de calor tiene pistas en conflicto para SBR {E-1008} {E-1011}; la química, la resistencia mecánica y el costo no tienen respaldo. Ninguna fila queda confirmada. FKM, silicona y poliuretano aparecen solo como pistas cualitativas de proveedores {E-1014}.",
  "Vacíos y decisión. Las 14 secciones del dossier quedan VACÍO declarado: sin datos de operación, de fallas ni de costos no se calcula vida, punto óptimo ni LCC, y no se recomienda un material. La dureza máxima de sellos nuevos está cortada en la imagen. Para decidir material, dureza, inspección y reemplazo se necesitan el fluido y las condiciones, el historial de cambios con censura, los costos y acceso a las fuentes; las preguntas están al final."],
 "palabras_clave": ["sello de marco", "filtro de prensa de placas", "elastómeros", "deformación permanente", "EPDM", "NBR", "desgaste abrasivo"],
 "criterio": "Ninguna fuente se leyó más allá del resumen de buscador; no hay citas ni cuartiles obtenibles."}
(C / "abstract.json").write_text(json.dumps(abstract, ensure_ascii=False, indent=1), encoding="utf-8")

traz = [
 {"agente": "reliability-engineer", "rol": "LÍDER del equipo (ESTRATEGA)", "hizo": "Leyó las imágenes, comprobó el acceso de red, ejecutó seis búsquedas de frentes distintos, armó el registro, el dossier, las tablas y las preguntas. No pudo lanzar investigadores en paralelo porque un subagente no crea otros: hizo él mismo cada frente.", "entrada": "Solicitud, dos imágenes y notas de pendientes", "salida": "Dossier validado, informe HTML y preguntas finales", "aprendio": "Con la red bloqueada todo queda SOLO-SNIPPET y el dossier se entrega con VACÍO declarado en lugar de rellenar."},
 {"agente": "reliability-case-historian", "rol": "Recurrencia (hecho por el LÍDER por búsqueda de texto)", "hizo": "Buscó en el historial: no hay caso previo de sellos de filtros prensa; los dossiers de bombas y de chumacera solo sirvieron como molde de estructura.", "entrada": "Carpeta historial", "salida": "Sin recurrencia", "aprendio": "Los sellos mecánicos de bombas figuran como VACÍO en dossiers previos, no como evidencia."},
 {"agente": "reliability-evidence-verifier", "rol": "Verificador independiente", "hizo": "PENDIENTE: no estaba disponible como subagente desde esta ejecución; el LÍDER hizo solo autochequeos automáticos.", "entrada": "Dossier e informe", "salida": "Verificación posterior lanzada desde la sesión principal: NO APTO (1 bloqueante, 4 altos); corregidos en el script y reensamblado", "aprendio": "La verificación independiente debe lanzarla quien pueda crear subagentes."},
]
(C / "trazabilidad.json").write_text(json.dumps(traz, ensure_ascii=False, indent=1), encoding="utf-8")
(C / "meta.json").write_text(json.dumps({"modo_falla": D["modo_falla"], "fecha": F, "version": 1, "secciones_con_evidencia": v["cobertura"]["con_evidencia"], "secciones_vacias": v["vacios"], "entradas_registro": len(L.entradas), "nota": "Pistas SOLO-SNIPPET no respaldan afirmaciones; ver evidencia.json"}, ensure_ascii=False, indent=1), encoding="utf-8")
