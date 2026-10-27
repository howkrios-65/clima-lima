"""Registro de evidencia científica (ledger) con compuertas que impiden presentar como verificado lo que no se leyó.

Cada entrada describe UNA fuente y lo que el investigador realmente pudo leer de ella. El nivel de evidencia no lo
escribe nadie a mano: se deriva del tipo de acceso. Una fuente solo puede ser VERIFICADO si trae un extracto literal y
su localizador; un cuartil de revista solo se admite con la fuente del cuartil.
"""
from __future__ import annotations

import datetime as _dt
import json
import re
from collections import Counter
from pathlib import Path
from typing import Iterable

TIPOS = {"paper", "tesis", "libro", "norma", "reporte_tecnico", "repositorio", "preprint", "dato_usuario", "otro"}
ACCESOS = {"texto_completo", "fragmento", "abstract", "snippet", "solo_referencia"}
# acceso -> nivel de evidencia. 'abstract' es verificado a nivel de abstract, no del artículo.
NIVEL_POR_ACCESO = {
    "texto_completo": "VERIFICADO-TEXTO",
    "fragmento": "VERIFICADO-TEXTO",
    "abstract": "VERIFICADO-ABSTRACT",
    "snippet": "SOLO-SNIPPET",
    "solo_referencia": "NO-VERIFICADO",
}
ORDEN_NIVEL = {"NO-VERIFICADO": 0, "SOLO-SNIPPET": 1, "VERIFICADO-ABSTRACT": 2, "VERIFICADO-TEXTO": 3}
# vías que por su naturaleza solo entregan resúmenes de buscador
VIAS_SOLO_SNIPPET = {"websearch"}
DOI_RE = re.compile(r"^10\.\d{4,9}/\S+$")
ID_RE = re.compile(r"^E-\d{4}$")
MAX_EXTRACTO = 800


class EvidenciaInvalida(ValueError):
    pass


def nivel(entry: dict) -> str:
    """Nivel de evidencia derivado del acceso (fuente del usuario: DATO-USUARIO)."""
    if entry.get("tipo") == "dato_usuario":
        return "DATO-USUARIO"
    return NIVEL_POR_ACCESO.get(entry.get("acceso"), "NO-VERIFICADO")


def validar_entrada(e: dict, hoy: _dt.date | None = None) -> tuple[list[str], list[str]]:
    """Devuelve (errores, avisos). Un error impide guardar la entrada."""
    hoy = hoy or _dt.date.today()
    err, warn = [], []
    if not ID_RE.match(str(e.get("id", ""))):
        err.append("id debe tener el formato E-0001")
    if e.get("tipo") not in TIPOS:
        err.append(f"tipo inválido: {e.get('tipo')!r}")
    if e.get("acceso") not in ACCESOS and e.get("tipo") != "dato_usuario":
        err.append(f"acceso inválido: {e.get('acceso')!r}")
    ref = e.get("referencia") or {}
    if e.get("tipo") in {"paper", "tesis", "libro", "preprint", "reporte_tecnico"}:
        for k in ("autores", "anio", "titulo"):
            if not ref.get(k):
                err.append(f"referencia.{k} es obligatorio para {e.get('tipo')}")
    anio = ref.get("anio")
    if anio is not None and not (isinstance(anio, int) and 1800 <= anio <= hoy.year + 1):
        err.append(f"referencia.anio fuera de rango: {anio!r}")
    doi = ref.get("doi")
    if doi and not DOI_RE.match(doi):
        err.append("referencia.doi con formato inválido (use solo '10.xxxx/...', sin https://doi.org/)")
    if e.get("tipo") == "paper" and not doi:
        warn.append("paper sin DOI: verifique que exista antes de citarlo")
    try:
        fa = _dt.date.fromisoformat(str(e.get("fecha_acceso")))
        if fa > hoy:
            err.append("fecha_acceso en el futuro")
    except ValueError:
        err.append("fecha_acceso debe ser AAAA-MM-DD")
    acc = e.get("acceso")
    if acc in {"texto_completo", "fragmento", "abstract"}:
        ex = (e.get("extracto") or "").strip()
        if not ex:
            err.append("acceso con lectura exige extracto literal")
        elif len(ex) > MAX_EXTRACTO:
            err.append(f"extracto demasiado largo ({len(ex)} > {MAX_EXTRACTO}): cite solo lo que respalda la afirmación")
        if not (e.get("localizador") or "").strip():
            err.append("acceso con lectura exige localizador (sección, página, figura o fragmento)")
    if str(e.get("via", "")).lower() in VIAS_SOLO_SNIPPET and acc in {"texto_completo", "fragmento", "abstract"}:
        err.append("una búsqueda web solo entrega resúmenes: use acceso 'snippet' o abra la página con otra vía")
    if not (e.get("afirma") or "").strip():
        err.append("afirma es obligatorio: qué respalda exactamente esta fuente")
    if not (e.get("limites") or "").strip():
        err.append("limites es obligatorio: qué NO respalda (tipo de estudio, material, condiciones)")
    q = e.get("revista_cuartil")
    if q:
        if q.get("valor") is not None:
            if q["valor"] not in (1, 2, 3, 4):
                err.append("revista_cuartil.valor debe ser 1 a 4")
            if not q.get("fuente"):
                err.append("un cuartil solo se admite con su fuente (p. ej. 'SJR 2024'): sin fuente, déjelo en null")
    if e.get("estado_retractado"):
        warn.append("fuente retractada: no puede respaldar afirmaciones")
    if not ref.get("pais") and e.get("tipo") in {"paper", "tesis"}:
        warn.append("sin país o institución: no se podrá resumir la cobertura geográfica")
    return err, warn


class Ledger:
    """Colección de entradas validadas. Los errores bloquean; los avisos se acumulan."""

    def __init__(self, entradas: Iterable[dict] | None = None):
        self.entradas: dict[str, dict] = {}
        self.avisos: dict[str, list[str]] = {}
        for e in entradas or []:
            self.add(e)

    def add(self, entry: dict) -> dict:
        err, warn = validar_entrada(entry)
        if entry.get("id") in self.entradas:
            err.append("id duplicado")
        doi = ((entry.get("referencia") or {}).get("doi") or "").lower()
        if doi and any(((o.get("referencia") or {}).get("doi") or "").lower() == doi for o in self.entradas.values()):
            err.append(f"el DOI {doi} ya está registrado")
        if err:
            raise EvidenciaInvalida(f"{entry.get('id', '?')}: " + "; ".join(err))
        e = dict(entry)
        e["nivel_evidencia"] = nivel(e)
        self.entradas[e["id"]] = e
        self.avisos[e["id"]] = warn
        return e

    def get(self, id_: str) -> dict:
        return self.entradas[id_]

    def nivel_de(self, id_: str) -> str:
        return self.entradas[id_]["nivel_evidencia"]

    def puede_afirmar(self, ids: Iterable[str], minimo: str = "VERIFICADO-ABSTRACT") -> tuple[bool, list[str]]:
        """¿Todas las fuentes alcanzan el nivel mínimo? Devuelve (ok, ids que no alcanzan)."""
        if minimo not in ORDEN_NIVEL:
            raise ValueError(f"nivel mínimo desconocido: {minimo}")
        malos = []
        for i in ids:
            e = self.entradas.get(i)
            if e is None or e.get("estado_retractado") or ORDEN_NIVEL.get(e["nivel_evidencia"], -1) < ORDEN_NIVEL[minimo]:
                malos.append(i)
        return (not malos), malos

    def exigir(self, ids: Iterable[str], minimo: str = "VERIFICADO-ABSTRACT") -> None:
        ok, malos = self.puede_afirmar(ids, minimo)
        if not ok:
            raise EvidenciaInvalida(f"fuentes que no alcanzan {minimo}: {malos}")

    def resumen(self) -> dict:
        es = list(self.entradas.values())
        quart = Counter((e.get("revista_cuartil") or {}).get("valor") for e in es if (e.get("revista_cuartil") or {}).get("valor"))
        return {
            "total": len(es),
            "por_nivel": dict(Counter(e["nivel_evidencia"] for e in es)),
            "por_tipo": dict(Counter(e["tipo"] for e in es)),
            "por_pais": dict(Counter((e.get("referencia") or {}).get("pais") for e in es if (e.get("referencia") or {}).get("pais"))),
            "cuartil_verificado": {f"Q{k}": v for k, v in sorted(quart.items())},
            "sin_cuartil_verificado": sum(1 for e in es if not (e.get("revista_cuartil") or {}).get("valor")),
            "retractadas": sum(1 for e in es if e.get("estado_retractado")),
        }

    def to_json(self, path: str | Path | None = None) -> str:
        s = json.dumps(list(self.entradas.values()), ensure_ascii=False, indent=1)
        if path:
            Path(path).write_text(s, encoding="utf-8")
        return s

    @classmethod
    def from_json(cls, path_or_text: str | Path) -> "Ledger":
        p = Path(str(path_or_text))
        txt = p.read_text(encoding="utf-8") if len(str(path_or_text)) < 500 and p.exists() else str(path_or_text)
        return cls(json.loads(txt))


def apa(entry: dict) -> str:
    """Referencia en formato APA 7 usando SOLO los campos presentes (no inventa nada)."""
    r = entry.get("referencia") or {}
    autores = r.get("autores") or "Autor no identificado"
    anio = r.get("anio")
    partes = [f"{autores} ({anio if anio else 's. f.'}). {r.get('titulo', 'Sin título')}."]
    if r.get("fuente"):
        vol = r.get("volumen")
        pag = r.get("paginas")
        det = r["fuente"] + (f", {vol}" if vol else "") + (f", {pag}" if pag else "")
        partes.append(det + ".")
    if r.get("doi"):
        partes.append(f"https://doi.org/{r['doi']}")
    elif r.get("url"):
        partes.append(r["url"])
    return " ".join(partes)
