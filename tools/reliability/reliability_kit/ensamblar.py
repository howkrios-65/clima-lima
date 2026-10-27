"""Ensamblador del informe de un modo de falla a partir de una carpeta de historial.

Entradas (todas generadas por los agentes y validadas aquí):
    evidencia.json      registro de evidencia (lista de entradas para Ledger)
    dossier.json        {"modo_falla", "secciones": {id: {"elementos": [...], "vacio", "nota"}}}
    analisis/*.json     fmeca, arbol, acr, lcc, vida, predictivo (opcionales)
    extra.json          opcional: tablas, supuestos, preguntas, vacios adicionales
Salida: informe.html autocontenido. Las compuertas de evidencia se aplican en `construir_informe`; el dossier se valida antes.
"""
from __future__ import annotations

import datetime as _dt
import json
from pathlib import Path

from . import dossier as _dz
from .evidence import Ledger
from .report_html import construir_informe

ANALISIS = ("fmeca", "arbol", "acr", "lcc", "vida", "predictivo")


def _cargar(p: Path):
    return json.loads(p.read_text(encoding="utf-8")) if p.exists() else None


def ensamblar(carpeta: str | Path, salida: str | Path | None = None, simulador: bool = True) -> dict:
    c = Path(carpeta)
    L = Ledger.from_json(c / "evidencia.json")
    D = _cargar(c / "dossier.json")
    if D is None:
        raise FileNotFoundError("falta dossier.json")
    val = _dz.validar_dossier(D, L)
    if val["errores"]:
        raise ValueError("dossier inválido: " + "; ".join(val["errores"][:5]))
    titulos = {s[0]: s[1] for s in _dz.SECCIONES}
    hall, k = [], 0
    for sid, sec in D["secciones"].items():
        if sid == "referencias":
            continue
        for el in sec.get("elementos", []):
            k += 1
            hall.append({"id": f"H{k}", "texto": f"[{titulos[sid]}] {el['titulo']}. Límite: {el.get('limite', 'no declarado')}", "evidencia": el["evidencia"]})
    vac = [f"{titulos[s]}: {x['vacio']}" for s, x in D["secciones"].items() if x.get("vacio")]
    vac += [f"{titulos[s]}: {x['nota']}" for s, x in D["secciones"].items() if x.get("nota")]
    an = {n: _cargar(c / "analisis" / f"{n}.json") for n in ANALISIS}
    an = {k_: v for k_, v in an.items() if v}
    for v in an.values():
        vac += v.get("vacios", [])
    an["herramientas"] = True
    extra = _cargar(c / "extra.json") or {}
    primero = next(iter(L.entradas))
    caso = {
        "meta": {"titulo": f"Dossier del modo de falla: {D['modo_falla']}", "activo": D["modo_falla"], "origen_datos": "literatura leída por el equipo; sin datos de planta", "n_fallas": 0},
        "resumen": {"kpis": [{"label": "entradas en el registro (incluye pistas)", "valor": str(len(L.entradas)), "evidencia": [primero]},
                             {"label": "secciones con evidencia leída (sin Referencias)", "valor": f"{val['cobertura']['con_evidencia'] - 1} de {len(_dz.SECCIONES) - 1}", "evidencia": [primero]},
                             {"label": "secciones VACÍO declarado", "valor": str(val["cobertura"]["vacias"]), "evidencia": [primero]}], "hallazgos": hall},
        "tablas": extra.get("tablas", []), "vacios": vac + extra.get("vacios", []),
        "supuestos": extra.get("supuestos", ["Sin caso real: ningún dato de planta se usó."]),
        "preguntas": extra.get("preguntas", []),
        "historial": [{"version": "v1", "fecha": _dt.date.today().isoformat(), "cambio": "Informe ensamblado", "baseline": "VACÍO: sin datos de falla del activo"}],
        "dossier": {"orden": [s[0] for s in _dz.SECCIONES], "titulos": titulos, "frentes": {s[0]: s[2] for s in _dz.SECCIONES}, "secciones": D["secciones"]},
        "analisis": an, "simulador": simulador,
    }
    return construir_informe(caso, L, salida or c / "informe.html")
