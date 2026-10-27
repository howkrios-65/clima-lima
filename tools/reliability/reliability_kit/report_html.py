"""Generador del informe HTML dinámico y autocontenido, con compuertas de evidencia.

El informe no calcula estadística en el navegador salvo el módulo de vida (Weibull) y la regla de detección retrospectiva, que
traen una autoprueba contra los valores calculados aquí con el kit. Cada afirmación del informe apunta a entradas del registro de
evidencia; lo que no tiene respaldo se degrada o se marca "SIN EVIDENCIA", y los ajustes quedan listados en el propio informe.
"""
from __future__ import annotations

import json
import re
from datetime import date
from pathlib import Path

from .evidence import ORDEN_NIVEL, Ledger, apa

ASSETS = Path(__file__).parent / "assets"
ESTADOS_HIP = ("confirmada", "probable", "posible", "descartada")
TIPOS_LINEA = ("bitacora", "ot", "medicion", "hito", "accion", "analisis")

NOTA_INDEPENDENCIA = ("La convergencia de técnicas no es confirmación: técnicas que parten de la misma información no son independientes. "
                      "Por eso, junto al número de técnicas se muestra cuántas fuentes de información distintas las alimentan.")

# Guía de selección de enfoque predictivo. Es SÍNTESIS del equipo (reglas del protocolo de validación), no un resultado de literatura.
GUIA_MODELOS = [
    {"id": "umbral", "nombre": "Umbral o carta de control sobre un indicador", "min_fallas": 0, "etiquetas": "no",
     "cuando_evitar": "Si el indicador no tiene relación física con el modo de falla.",
     "validacion": ["Línea base con ventana sin falla", "Tasa de falsas alarmas por activo-mes", "Costo de falso negativo y falso positivo"],
     "riesgo": "Umbral ajustado a posteriori sobre un solo evento"},
    {"id": "supervivencia", "nombre": "Weibull o Kaplan-Meier con censura", "min_fallas": 2, "etiquetas": "no",
     "cuando_evitar": "Equipos reparables con tendencia (usar NHPP); modos de falla mezclados sin separar.",
     "validacion": ["Intervalos de confianza", "Bondad de ajuste y comparación de modelos", "No extrapolar más allá de la mayor edad observada"],
     "riesgo": "Menos de 10 fallas: resultado exploratorio"},
    {"id": "cox", "nombre": "Regresión de Cox o de tiempo acelerado", "min_fallas": 30, "etiquetas": "no",
     "cuando_evitar": "Pocas fallas por covariable; riesgos no proporcionales sin comprobar.",
     "validacion": ["Prueba de proporcionalidad de riesgos", "Validación por activo", "Calibración"],
     "riesgo": "Sobreajuste con pocas fallas"},
    {"id": "arboles", "nombre": "Bosque aleatorio o gradiente de árboles (clasificación en un horizonte)", "min_fallas": 30, "etiquetas": "si",
     "cuando_evitar": "Sin etiquetas de falla confiables o con fuga temporal de variables.",
     "validacion": ["Partición por activo y por tiempo", "Precisión-recall, no exactitud", "Calibración", "Comparación con el baseline simple"],
     "riesgo": "Fuga de datos; clases extremadamente desbalanceadas"},
    {"id": "anomalias", "nombre": "Detección de anomalías (bosque de aislamiento, autoencoder)", "min_fallas": 0, "etiquetas": "no",
     "cuando_evitar": "Si no hay un periodo sano representativo para entrenar.",
     "validacion": ["Métricas por evento y no por punto", "Falsas alarmas por activo-mes", "Evaluación en activos no vistos"],
     "riesgo": "El ajuste por puntos sobrestima el desempeño"},
    {"id": "rul", "nombre": "Vida útil remanente con aprendizaje profundo", "min_fallas": 50, "etiquetas": "si",
     "cuando_evitar": "Si un baseline de supervivencia o un indicador simple no ha sido superado con evidencia.",
     "validacion": ["Varias métricas con protocolo explícito", "Incertidumbre calibrada", "Activos nunca vistos", "Plan de deriva"],
     "riesgo": "Resultados dependientes del preprocesamiento y del conjunto de prueba"},
]


def _json_seguro(obj) -> str:
    s = json.dumps(obj, ensure_ascii=False, separators=(",", ":"), default=str)
    return s.replace("</", "<\\/").replace("\u2028", "\\u2028").replace("\u2029", "\\u2029")


def convergencia(tecnicas: list[dict], raices: list[dict]) -> dict:
    """Matriz técnica × raíz con el recuento y las fuentes de información distintas detrás de cada raíz."""
    ids = [r["id"] for r in raices]
    out = {"raices": ids, "tecnicas": [t["id"] for t in tecnicas], "matriz": {}, "por_raiz": {}, "nota": NOTA_INDEPENDENCIA}
    for t in tecnicas:
        out["matriz"][t["id"]] = {rid: (rid in t.get("raices", [])) for rid in ids}
    n = len(tecnicas)
    for rid in ids:
        sop = [t for t in tecnicas if rid in t.get("raices", [])]
        insumos = set()
        for t in sop:
            insumos |= set(t.get("insumos", []))
        out["por_raiz"][rid] = {"tecnicas": [t["id"] for t in sop], "n": len(sop), "de": n,
                                "fuentes_distintas": len(insumos), "insumos": sorted(insumos)}
    return out


def aplicar_compuertas(caso: dict, ledger: Ledger) -> list[dict]:
    """Degrada lo que no tiene respaldo y devuelve la lista de ajustes. Un id de evidencia inexistente es un error."""
    ajustes: list[dict] = []

    def ids_existen(ids, donde):
        malos = [i for i in ids if i not in ledger.entradas]
        if malos:
            raise ValueError(f"{donde}: ids de evidencia inexistentes {malos}")

    for h in caso.get("hipotesis", []):
        ids_existen(h.get("apoyo_caso", []) + h.get("apoyo_literatura", []) + h.get("contradice", []), f"hipótesis {h['id']}")
        lit_ok, lit_malas = [], []
        for i in h.get("apoyo_literatura", []):
            (lit_ok if ledger.puede_afirmar([i], "VERIFICADO-ABSTRACT")[0] else lit_malas).append(i)
        if lit_malas:
            ajustes.append({"donde": f"hipótesis {h['id']}", "tipo": "fuente_retirada",
                            "detalle": f"se quitó el respaldo científico {lit_malas}: no alcanza VERIFICADO-ABSTRACT"})
        h["apoyo_literatura"] = lit_ok
        caso_ok = [i for i in h.get("apoyo_caso", []) if ledger.nivel_de(i) == "DATO-USUARIO"]
        if len(caso_ok) != len(h.get("apoyo_caso", [])):
            ajustes.append({"donde": f"hipótesis {h['id']}", "tipo": "evidencia_de_caso_invalida",
                            "detalle": "una evidencia del caso no es un dato aportado: se movió a respaldo científico"})
            lit_ok += [i for i in h["apoyo_caso"] if i not in caso_ok and ledger.puede_afirmar([i], "VERIFICADO-ABSTRACT")[0]]
            h["apoyo_literatura"] = lit_ok
        h["apoyo_caso"] = caso_ok
        estado = h.get("estado", "posible")
        if estado not in ESTADOS_HIP:
            raise ValueError(f"hipótesis {h['id']}: estado inválido {estado!r}")
        if estado == "confirmada" and not caso_ok:
            nuevo = "probable" if lit_ok else "posible"
            ajustes.append({"donde": f"hipótesis {h['id']}", "tipo": "degradada", "de": "confirmada", "a": nuevo,
                            "detalle": "una causa solo se confirma con evidencia del propio caso; la literatura respalda plausibilidad, no ocurrencia"})
            h["estado"] = nuevo
            h["degradada"] = True
        if estado == "probable" and not caso_ok and not lit_ok:
            ajustes.append({"donde": f"hipótesis {h['id']}", "tipo": "degradada", "de": "probable", "a": "posible",
                            "detalle": "sin evidencia del caso ni respaldo científico verificado"})
            h["estado"] = "posible"
            h["degradada"] = True
    for sec in ("hallazgos",):
        for x in caso.get("resumen", {}).get(sec, []):
            ids_existen(x.get("evidencia", []), f"hallazgo {x.get('id', '?')}")
            if not x.get("evidencia"):
                x["sin_evidencia"] = True
                ajustes.append({"donde": f"hallazgo {x.get('id', '?')}", "tipo": "sin_evidencia", "detalle": "afirmación sin ninguna fuente"})
    for k in caso.get("resumen", {}).get("kpis", []):
        ids_existen(k.get("evidencia", []), f"KPI {k.get('label', '?')}")
    for t in caso.get("tecnicas", []):
        ids_existen(t.get("evidencia", []), f"técnica {t['id']}")
    for sid, sec in (caso.get("dossier") or {}).get("secciones", {}).items():
        for el in sec.get("elementos", []):
            ids_existen(el.get("evidencia", []), f"dossier {sid}")
            if not el.get("evidencia"):
                raise ValueError(f"dossier {sid}: elemento sin fuente")
    for p in caso.get("plan", []):
        ids_existen(p.get("evidencia", []), f"acción {p.get('id', '?')}")
        if not p.get("evidencia"):
            ajustes.append({"donde": f"acción {p.get('id', '?')}", "tipo": "sin_evidencia", "detalle": "acción de plan sin fuente que la respalde"})
    for e in caso.get("linea_tiempo", []):
        ids_existen(e.get("evidencia", []), f"evento {e.get('fecha')}")
        if e.get("tipo") not in TIPOS_LINEA:
            raise ValueError(f"evento {e.get('fecha')}: tipo {e.get('tipo')!r} no válido {TIPOS_LINEA}")
    return ajustes


def _filtrar_items(items, ledger, donde, ajustes, clave_id="id"):
    """Quita ids de evidencia que no alcanzan VERIFICADO-ABSTRACT; un ítem sin ninguna fuente válida se elimina y queda listado."""
    out = []
    for it in items or []:
        ids = it.get("evidencia") or []
        ok = [i for i in ids if i in ledger.entradas and ledger.puede_afirmar([i], "VERIFICADO-ABSTRACT")[0]]
        if len(ok) != len(ids):
            ajustes.append({"donde": f"{donde} {it.get(clave_id, '')}".strip(), "tipo": "fuente_retirada",
                            "detalle": f"se quitaron fuentes que no alcanzan VERIFICADO-ABSTRACT o no existen: {[i for i in ids if i not in ok]}"})
        if not ok:
            ajustes.append({"donde": f"{donde} {it.get(clave_id, '')}".strip(), "tipo": "item_eliminado", "detalle": "ítem sin ninguna fuente válida"})
            continue
        it["evidencia"] = ok
        if it.get("nivel") not in ("EVIDENCIA", "SINTESIS"):
            it["nivel"] = "SINTESIS"
        out.append(it)
    return out


def aplicar_compuertas_analisis(an: dict, ledger: Ledger) -> list[dict]:
    """Compuertas del análisis de ingeniería (FMECA, árbol, ACR, LCC, vida, predictivo)."""
    aj: list[dict] = []
    if not an:
        return aj
    f = an.get("fmeca")
    if f:
        f["items"] = _filtrar_items(f.get("items"), ledger, "FMECA", aj)
        for it in f["items"]:
            for k in ("severidad", "ocurrencia", "deteccion_puntaje"):
                if it.get(k) is not None:
                    aj.append({"donde": f"FMECA {it['id']}", "tipo": "puntaje_retirado", "detalle": f"{k} sin fuente: lo asigna un experto en la pestaña"})
                    it[k] = None
    a = an.get("arbol")
    if a:
        a["nodos"] = _filtrar_items(a.get("nodos"), ledger, "árbol", aj)
        ids = {n["id"] for n in a["nodos"]}
        for n in a["nodos"]:
            n["hijos"] = [h for h in n.get("hijos", []) if h in ids]
            if n.get("probabilidad") is not None:
                aj.append({"donde": f"árbol {n['id']}", "tipo": "probabilidad_retirada", "detalle": "probabilidad sin fuente: la ingresa quien la conozca"})
                n["probabilidad"] = None
            if n.get("puerta") not in ("OR", "AND", "BASE"):
                n["puerta"] = "BASE" if not n["hijos"] else "OR"
    r = an.get("acr")
    if r:
        r["hipotesis"] = _filtrar_items(r.get("hipotesis"), ledger, "ACR hipótesis", aj)
        for h in r["hipotesis"]:
            if h.get("estado") != "posible":
                aj.append({"donde": f"ACR {h['id']}", "tipo": "degradada", "de": h.get("estado"), "a": "posible",
                           "detalle": "sin evidencia del propio caso ninguna causa pasa de posible"})
                h["estado"] = "posible"
        for cat, lst in list((r.get("ishikawa") or {}).items()):
            r["ishikawa"][cat] = _filtrar_items(lst, ledger, f"Ishikawa {cat}", aj, clave_id="texto")
        r["ensayos"] = _filtrar_items(r.get("ensayos"), ledger, "ensayo", aj, clave_id="ensayo")
    l = an.get("lcc")
    if l:
        l["elementos"] = _filtrar_items(l.get("elementos"), ledger, "LCC", aj)
        for e in l["elementos"]:
            if e.get("valor") is not None:
                aj.append({"donde": f"LCC {e['id']}", "tipo": "valor_retirado", "detalle": "costo sin fuente: lo ingresa la persona o se obtiene de una tesis o paper"})
                e["valor"] = None
        l["formulas"] = _filtrar_items(l.get("formulas"), ledger, "fórmula", aj, clave_id="nombre")
    v = an.get("vida")
    if v:
        v["hallazgos"] = _filtrar_items(v.get("hallazgos"), ledger, "vida", aj)
        v["metodo_recomendado"] = _filtrar_items(v.get("metodo_recomendado"), ledger, "método de vida", aj, clave_id="situacion")
    pr = an.get("predictivo")
    if pr:
        pr["hallazgos"] = _filtrar_items(pr.get("hallazgos"), ledger, "predictivo", aj)
        pr["estrategia"] = _filtrar_items(pr.get("estrategia"), ledger, "estrategia", aj, clave_id="etapa")
        pr["riesgos_de_validacion"] = _filtrar_items(pr.get("riesgos_de_validacion"), ledger, "riesgo", aj, clave_id="riesgo")
    return aj


def construir_informe(caso: dict, ledger: Ledger, salida: str | Path | None = None) -> dict:
    """Devuelve {'html', 'ajustes', 'resumen_evidencia'} y, si se da `salida`, escribe el archivo HTML autocontenido."""
    c = json.loads(json.dumps(caso, default=str))        # copia profunda; no se modifica el caso del llamador
    c.setdefault("meta", {})
    for k in ("hipotesis", "tecnicas", "raices", "linea_tiempo", "series", "tablas", "plan", "preguntas", "vacios", "supuestos"):
        c.setdefault(k, [])
    c.setdefault("resumen", {"kpis": [], "hallazgos": []})
    if not c["meta"].get("titulo"):
        raise ValueError("meta.titulo es obligatorio")
    ajustes = aplicar_compuertas(c, ledger) + aplicar_compuertas_analisis(c.get("analisis"), ledger)
    for t in c["tecnicas"]:
        t.setdefault("insumos", [])
    conv = convergencia(c["tecnicas"], c["raices"]) if c["tecnicas"] and c["raices"] else None
    ev = []
    for e in ledger.entradas.values():
        d = dict(e)
        d["apa"] = apa(e)
        d["avisos"] = ledger.avisos.get(e["id"], [])
        ev.append(d)
    ev.sort(key=lambda e: e["id"])
    datos = {"caso": c, "evidencia": ev, "resumen_evidencia": ledger.resumen(), "convergencia": conv, "ajustes": ajustes,
             "guia_modelos": GUIA_MODELOS, "generado": date.today().isoformat(), "orden_nivel": ORDEN_NIVEL}
    tpl = (ASSETS / "informe_template.html").read_text(encoding="utf-8")
    html = tpl.replace("__TITULO__", re.sub(r"[<>&]", "", c["meta"]["titulo"])).replace("/*__INFORME_JSON__*/null", _json_seguro(datos))
    if salida:
        Path(salida).write_text(html, encoding="utf-8")
    return {"html": html, "ajustes": ajustes, "resumen_evidencia": ledger.resumen(), "convergencia": conv}
