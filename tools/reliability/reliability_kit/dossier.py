"""Dossier por modo de falla: catálogo de secciones y compuerta de referencias.

Regla del usuario: no se coloca tabla, valor, referencia ni imagen que no lleve su fuente. Cada elemento de una sección declara
los ids del registro de evidencia que lo respaldan; una sección sin elementos con fuente se declara VACÍO con su motivo.
"""
from __future__ import annotations

from .evidence import Ledger

# (id, título, frente que la investiga, qué exige para no quedar vacía)
SECCIONES = [
    ("mediciones", "Mediciones y curvas", "monitoreo", "Variables medibles del modo de falla y su comportamiento típico, citado"),
    ("fenomenos", "Fenómenos físicos", "mecanismo", "Mecanismo físico del modo de falla con fuente primaria o revisión"),
    ("top_fallas", "Top de fallas y modos de falla", "modos", "Frecuencias o rankings publicados, con base de datos, tamaño y año"),
    ("fmeca", "FMECA y RCM", "modos", "Modos, efectos y causas respaldados; las escalas S-O-D no se inventan"),
    ("confiabilidad", "Confiabilidad (Weibull y vida)", "datos", "Datos públicos de vida o parámetros publicados con su origen; si no hay, VACÍO"),
    ("punto_optimo", "Punto óptimo de reemplazo", "economia", "Fórmula del modelo con su fuente y costos aportados por la persona"),
    ("lcc", "Costo-riesgo y LCC", "economia", "Método y datos de costo con fuente; sin costos no hay cifras"),
    ("vida_util", "Vida útil y obsolescencia", "mecanismo", "Vida de diseño o experiencia publicada del componente"),
    ("ibr", "Inspección basada en riesgo (IBR o RBI)", "normas", "Marco normativo o publicado aplicable al componente"),
    ("ml", "Modelos de aprendizaje automático y profundo", "ml", "Estudios con validación explícita; se registran sus límites y comparabilidad"),
    ("acr", "Causa raíz (ACR)", "modos", "Causas raíz típicas publicadas para el modo de falla"),
    ("troubleshooting", "Diagnóstico y troubleshooting", "monitoreo", "Síntomas y pruebas de diagnóstico respaldados"),
    ("mpd_normas", "Mantenimiento predictivo y normas", "normas", "Normas y guías con su estado de verificación"),
    ("referencias", "Referencias", "normas", "Lista APA de las fuentes realmente usadas, generada desde el registro"),
]
IDS = [s[0] for s in SECCIONES]
FRENTES = sorted({s[2] for s in SECCIONES})
TIPOS_ELEMENTO = {"tabla", "valor", "figura", "afirmacion", "referencia"}


def validar_dossier(dossier: dict, ledger: Ledger, minimo: str = "VERIFICADO-ABSTRACT") -> dict:
    """Devuelve {'errores', 'vacios', 'cobertura', 'por_seccion'}. Un elemento sin fuente suficiente es un error, no se publica.

    dossier = {"modo_falla": str, "secciones": {id: {"vacio": "motivo" | None, "elementos": [{"tipo","titulo","evidencia":[ids]}]}}}
    """
    errores, vacios, por = [], [], {}
    secs = dossier.get("secciones", {})
    for sid in secs:
        if sid not in IDS:
            errores.append(f"sección desconocida: {sid}")
    for sid, titulo, _, _ in SECCIONES:
        s = secs.get(sid)
        if s is None:
            errores.append(f"{sid}: falta; use vacio con motivo si no hay evidencia")
            continue
        els = s.get("elementos", [])
        if not els:
            if not (s.get("vacio") or "").strip():
                errores.append(f"{sid}: sin elementos y sin motivo de VACÍO")
            else:
                vacios.append(sid)
            por[sid] = 0
            continue
        ok = 0
        for i, e in enumerate(els):
            if e.get("tipo") not in TIPOS_ELEMENTO:
                errores.append(f"{sid}[{i}]: tipo inválido {e.get('tipo')!r}")
                continue
            ids = e.get("evidencia") or []
            if not ids:
                errores.append(f"{sid}[{i}] {e.get('titulo', '')!r}: {e['tipo']} sin fuente; no se publica")
                continue
            falta = [x for x in ids if x not in ledger.entradas]
            if falta:
                errores.append(f"{sid}[{i}]: ids inexistentes {falta}")
                continue
            good, bad = ledger.puede_afirmar(ids, minimo)
            if not good:
                errores.append(f"{sid}[{i}] {e.get('titulo', '')!r}: fuentes bajo {minimo}: {bad}")
                continue
            ok += 1
        por[sid] = ok
    n = len(SECCIONES)
    return {"errores": errores, "vacios": vacios, "por_seccion": por,
            "cobertura": {"con_evidencia": sum(1 for v in por.values() if v > 0), "vacias": len(vacios), "total": n}}
