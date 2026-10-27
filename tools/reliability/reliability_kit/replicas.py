"""Compuertas de cifras y réplicas: un número solo se publica si aparece literal en el extracto de la fuente que se cita.

`cifras`:   [{"id","valor","unidad","mide","condiciones","evidencia":[ids]}]
`replicas`: [{"id","titulo","tipo":"barras_ic"|"barras"|"tabla","unidad","condiciones","replica_de","evidencia":[ids],"limites",
              "series":[{"etiqueta","valor","ic":[lo,hi]}]  o  "columnas","filas"}]
Todos los números van como cadenas, tal como aparecen en el texto original.
"""
from __future__ import annotations

import re

from .evidence import Ledger

NUM = re.compile(r"^[+-]?\d+(?:[.,]\d+)?$")


def numero_en_texto(valor, texto: str) -> bool:
    v = str(valor).strip()
    if not v:
        return False
    for cand in {v, v.replace(".", ","), v.replace(",", ".")}:
        if re.search(r"(?<![\d.,])" + re.escape(cand) + r"(?![\d])", texto):
            return True
    return False


def _extractos(ids, ledger: Ledger):
    out, malos = [], []
    for i in ids or []:
        e = ledger.entradas.get(i)
        if e is None or not ledger.puede_afirmar([i], "VERIFICADO-ABSTRACT")[0]:
            malos.append(i)
        else:
            out.append(e.get("extracto") or "")
    return " ".join(out), malos


def validar_cifras(cifras: list[dict], ledger: Ledger):
    """Devuelve (cifras_validas, errores). Una cifra con número ausente del extracto se elimina."""
    ok, err = [], []
    for c in cifras or []:
        txt, malos = _extractos(c.get("evidencia"), ledger)
        if malos or not c.get("evidencia"):
            err.append(f"cifra {c.get('id')}: fuentes inexistentes o sin lectura suficiente {malos}")
        elif not numero_en_texto(c.get("valor"), txt):
            err.append(f"cifra {c.get('id')}: el valor {c.get('valor')!r} no está literal en el extracto")
        else:
            ok.append(c)
    return ok, err


def validar_replicas(replicas: list[dict], ledger: Ledger):
    ok, err = [], []
    for r in replicas or []:
        txt, malos = _extractos(r.get("evidencia"), ledger)
        fallos = []
        if malos or not r.get("evidencia"):
            fallos.append(f"fuentes inválidas {malos}")
        if r.get("tipo") not in ("barras", "barras_ic", "tabla"):
            fallos.append(f"tipo inválido {r.get('tipo')!r}")
        if r.get("tipo") == "tabla":
            for fila in r.get("filas", []):
                for cel in fila:
                    if NUM.match(str(cel).strip()) and not numero_en_texto(cel, txt):
                        fallos.append(f"celda {cel!r} ausente del extracto")
        else:
            for s in r.get("series", []):
                for v in [s.get("valor")] + list(s.get("ic") or []):
                    if v is not None and not numero_en_texto(v, txt):
                        fallos.append(f"valor {v!r} de {s.get('etiqueta')!r} ausente del extracto")
        if fallos:
            err.append(f"réplica {r.get('id')}: " + "; ".join(fallos[:4]))
        else:
            ok.append(r)
    return ok, err
