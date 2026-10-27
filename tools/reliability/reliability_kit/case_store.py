"""Historial de casos de falla con detección de recurrencia y líneas base versionadas.

Estructura en disco (solo se agrega, nunca se sobrescribe):
    <raiz>/casos/<id>/caso.json            caso vigente; versiones anteriores en caso.v1.json, caso.v2.json...
    <raiz>/linea_base/<familia>/v0001.json  una versión por recálculo, con la diferencia frente a la anterior
    <raiz>/linea_base/<familia>/vigente.json
Una "familia" es la pareja clase de activo + modo de falla. La línea base se calcula con el kit (Weibull con censura o
NHPP multiunidad si una misma unidad falla más de una vez) y declara VACÍO cuando no hay datos suficientes.
"""
from __future__ import annotations

import datetime as _dt
import hashlib
import json
import re
import unicodedata
from pathlib import Path

from .nhpp import fit_crow_amsaa_multi, laplace_trend_test_multi
from .weibull import (bias_correct_beta, compare_models_verdict, fit_weibull_mle, weibull_b_life_ci_lr, weibull_beta_ci_lr)

ID_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_\-]{2,63}$")
OBLIGATORIOS = ("id", "titulo", "activo_clase", "modo_falla", "unidad", "fecha_falla", "mecanismos")
STOP = {"de", "la", "el", "los", "las", "por", "en", "y", "a", "con", "del", "un", "una", "al", "se", "que", "para", "sin"}


class CasoInvalido(ValueError):
    pass


def _sin_acentos(s: str) -> str:
    return "".join(c for c in unicodedata.normalize("NFD", s) if unicodedata.category(c) != "Mn")


def slug(s: str) -> str:
    return re.sub(r"[^a-z0-9]+", "_", _sin_acentos(str(s).lower())).strip("_")


def familia_de(caso: dict) -> str:
    return f"{slug(caso['activo_clase'])}__{slug(caso['modo_falla'])}"


def _tokens(textos) -> set[str]:
    t = set()
    for x in textos:
        for w in re.findall(r"[a-z0-9]+", _sin_acentos(str(x).lower())):
            if len(w) > 2 and w not in STOP:
                t.add(w)
    return t


def _hash(obj) -> str:
    return hashlib.sha256(json.dumps(obj, sort_keys=True, ensure_ascii=False, default=str).encode()).hexdigest()


def validar_caso(c: dict) -> None:
    faltan = [k for k in OBLIGATORIOS if not c.get(k)]
    if faltan:
        raise CasoInvalido(f"faltan campos obligatorios: {faltan}")
    if not ID_RE.match(str(c["id"])):
        raise CasoInvalido("id inválido: use letras, números, guiones; 3 a 64 caracteres")
    try:
        _dt.date.fromisoformat(str(c["fecha_falla"]))
    except ValueError:
        raise CasoInvalido("fecha_falla debe ser AAAA-MM-DD")
    if not isinstance(c["mecanismos"], list) or not all(isinstance(m, str) for m in c["mecanismos"]):
        raise CasoInvalido("mecanismos debe ser una lista de textos")
    t = c.get("t_operacion")
    if t is not None and not (isinstance(t, (int, float)) and t > 0):
        raise CasoInvalido("t_operacion debe ser un número > 0 (edad de la unidad al fallar, en su unidad de tiempo)")
    for cen in c.get("censuras", []):
        if not (cen.get("unidad") and isinstance(cen.get("t_operacion"), (int, float)) and cen["t_operacion"] > 0):
            raise CasoInvalido("cada censura necesita unidad y t_operacion > 0")


class CaseStore:
    def __init__(self, raiz: str | Path):
        self.raiz = Path(raiz)
        (self.raiz / "casos").mkdir(parents=True, exist_ok=True)
        (self.raiz / "linea_base").mkdir(parents=True, exist_ok=True)

    # ---------- casos ----------
    def _dir(self, id_: str) -> Path:
        return self.raiz / "casos" / id_

    def registrar_caso(self, caso: dict, nueva_version: bool = False) -> dict:
        validar_caso(caso)
        d = self._dir(caso["id"])
        c = dict(caso)
        c["familia"] = familia_de(c)
        c["registrado_en"] = _dt.datetime.now(_dt.timezone.utc).isoformat(timespec="seconds")
        c["hash_entrada"] = _hash(caso)
        if d.exists():
            if not nueva_version:
                raise CasoInvalido(f"el caso {caso['id']} ya existe; use nueva_version=True para versionarlo sin perder el anterior")
            prev = json.loads((d / "caso.json").read_text(encoding="utf-8"))
            c["version"] = int(prev.get("version", 1)) + 1
            (d / f"caso.v{prev.get('version', 1)}.json").write_text(json.dumps(prev, ensure_ascii=False, indent=1), encoding="utf-8")
        else:
            d.mkdir(parents=True)
            c["version"] = 1
        (d / "caso.json").write_text(json.dumps(c, ensure_ascii=False, indent=1), encoding="utf-8")
        return c

    def cargar(self, id_: str) -> dict:
        return json.loads((self._dir(id_) / "caso.json").read_text(encoding="utf-8"))

    def listar(self) -> list[dict]:
        out = []
        for p in sorted((self.raiz / "casos").glob("*/caso.json")):
            out.append(json.loads(p.read_text(encoding="utf-8")))
        return sorted(out, key=lambda c: c["fecha_falla"])

    # ---------- recurrencia ----------
    def buscar_recurrencia(self, caso: dict, umbral_similitud: float = 0.35) -> list[dict]:
        """Casos previos que se parecen al nuevo. Regla explícita (no una caja negra):
        - misma_familia: igual clase de activo y modo de falla
        - misma_unidad: la misma unidad ya había fallado
        - mecanismo_similar: coeficiente de Jaccard de términos de mecanismos y causas >= umbral
        'es_recurrencia' si (misma_familia y misma_unidad) o (misma clase de activo y similitud >= umbral).
        """
        validar_caso(caso)
        fam = familia_de(caso)
        tk = _tokens(caso["mecanismos"] + [r.get("titulo", "") for r in caso.get("causas_raiz", [])])
        res = []
        for c in self.listar():
            if c["id"] == caso["id"]:
                continue
            tk2 = _tokens(c["mecanismos"] + [r.get("titulo", "") for r in c.get("causas_raiz", [])])
            jac = len(tk & tk2) / len(tk | tk2) if (tk | tk2) else 0.0
            misma_fam = c["familia"] == fam
            misma_uni = c["unidad"] == caso["unidad"]
            misma_clase = slug(c["activo_clase"]) == slug(caso["activo_clase"])
            tipos = [t for t, ok in (("misma_familia", misma_fam), ("misma_unidad", misma_uni),
                                     (f"mecanismo_similar(j={jac:.2f})", jac >= umbral_similitud)) if ok]
            if not tipos:
                continue
            dias = (_dt.date.fromisoformat(caso["fecha_falla"]) - _dt.date.fromisoformat(c["fecha_falla"])).days
            res.append({"caso_previo": c["id"], "titulo": c["titulo"], "fecha_falla": c["fecha_falla"], "coincidencias": tipos,
                        "similitud_mecanismo": round(jac, 3), "dias_desde_la_falla_previa": dias,
                        "es_recurrencia": bool((misma_fam and misma_uni) or (misma_clase and jac >= umbral_similitud)),
                        "intervalo_entre_fallas_mismo_equipo_dias": dias if (misma_fam and misma_uni) else None})
        return sorted(res, key=lambda r: (not r["es_recurrencia"], -r["similitud_mecanismo"], r["dias_desde_la_falla_previa"]))

    # ---------- línea base ----------
    def eventos_familia(self, familia: str) -> dict:
        casos = [c for c in self.listar() if c["familia"] == familia]
        fallas = [{"unidad": c["unidad"], "t": c["t_operacion"], "caso": c["id"], "fecha": c["fecha_falla"]}
                  for c in casos if c.get("t_operacion")]
        falladas = {f["unidad"] for f in fallas}
        ult = casos[-1] if casos else {}
        cens = [{"unidad": x["unidad"], "t": x["t_operacion"]} for x in ult.get("censuras", []) if x["unidad"] not in falladas]
        fin = ult.get("fin_observacion", {})
        return {"casos": [c["id"] for c in casos], "fallas": fallas, "censuras": cens, "fin_observacion": fin}

    def _dir_lb(self, familia: str) -> Path:
        d = self.raiz / "linea_base" / familia
        d.mkdir(parents=True, exist_ok=True)
        return d

    def linea_base_vigente(self, familia: str) -> dict | None:
        p = self._dir_lb(familia) / "vigente.json"
        return json.loads(p.read_text(encoding="utf-8")) if p.exists() else None

    def actualizar_linea_base(self, familia: str, motivo: str) -> dict:
        ev = self.eventos_familia(familia)
        if not ev["casos"]:
            raise CasoInvalido(f"no hay casos en la familia {familia}")
        por_unidad: dict[str, list] = {}
        for f in ev["fallas"]:
            por_unidad.setdefault(f["unidad"], []).append(f["t"])
        repetidas = [u for u, v in por_unidad.items() if len(v) >= 2]
        prev = self.linea_base_vigente(familia)
        version = (prev["version"] + 1) if prev else 1
        reg = {"version": version, "familia": familia, "fecha": _dt.date.today().isoformat(), "motivo": motivo,
               "casos_incluidos": ev["casos"], "hash_datos": _hash(ev), "n_fallas": len(ev["fallas"]),
               "n_unidades": len({f["unidad"] for f in ev["fallas"]} | {c["unidad"] for c in ev["censuras"]}),
               "advertencias": []}
        if repetidas:
            reg["metodo"] = "nhpp_multiunidad"
            falladas_t = {u: sorted(v) for u, v in por_unidad.items()}
            fin = ev["fin_observacion"]
            faltan = [u for u in falladas_t if u not in fin]
            if faltan:
                reg.update(estado="sin_base", resultado=None,
                           advertencias=[f"VACÍO: falta 'fin_observacion' de las unidades {faltan} para el modelo de reparables"])
            else:
                evs = [falladas_t[u] for u in falladas_t] + [[] for _ in ev["censuras"]]
                ends = [fin[u] for u in falladas_t] + [c["t"] for c in ev["censuras"]]
                f = fit_crow_amsaa_multi(evs, ends)
                reg.update(estado="calculada", resultado={"beta": f.beta, "beta_ic95": list(f.beta_ci), "tendencia": f.trend,
                                                          "laplace": laplace_trend_test_multi(evs, ends)})
                reg["advertencias"] += f.warnings
        else:
            reg["metodo"] = "weibull_censura"
            t = [f["t"] for f in ev["fallas"]] + [c["t"] for c in ev["censuras"]]
            cens = [False] * len(ev["fallas"]) + [True] * len(ev["censuras"])
            if len(ev["fallas"]) < 2 or len(set(f["t"] for f in ev["fallas"])) < 2:
                reg.update(estado="sin_base", resultado=None,
                           advertencias=[f"VACÍO: {len(ev['fallas'])} falla(s) con tiempo registrado; se necesitan al menos 2 distintas "
                                         "para estimar una distribución de vida"])
            else:
                f = fit_weibull_mle(t, cens)
                ci = weibull_beta_ci_lr(t, cens)
                b10 = weibull_b_life_ci_lr(t, cens, 0.10)
                res = {"beta": f.beta, "beta_ic95_lr": list(ci), "eta": f.eta, "mttf": f.mttf, "b10": b10["estimate"],
                       "b10_ic95_lr": [b10["lower"], b10["upper"]], "loglik": f.loglik,
                       "veredicto_modelos": compare_models_verdict(t, cens)["verdict"]}
                if f.r < 30:
                    res["beta_corregido_sesgo"] = bias_correct_beta(t, cens, n_boot=500)["beta_bc"]
                reg.update(estado="calculada", resultado=res)
                reg["advertencias"] += f.warnings
        if prev and prev.get("estado") == "calculada" and reg["estado"] == "calculada" and reg["metodo"] == prev["metodo"]:
            a, b = prev["resultado"], reg["resultado"]
            ci = b.get("beta_ic95_lr") or b.get("beta_ic95")
            reg["cambio_respecto_version_anterior"] = {
                "version_anterior": prev["version"], "delta_beta": b["beta"] - a["beta"],
                "beta_anterior_dentro_del_ic_nuevo": bool(ci[0] <= a["beta"] <= ci[1]),
                "interpretacion": ("la nueva evidencia es compatible con la línea base anterior"
                                   if ci[0] <= a["beta"] <= ci[1] else
                                   "el β anterior queda fuera del IC nuevo: posible cambio del patrón de falla; revisar causas y datos"),
            }
        elif prev:
            reg["cambio_respecto_version_anterior"] = {"version_anterior": prev["version"],
                                                       "interpretacion": "método o estado distinto: no comparable con la versión anterior"}
        d = self._dir_lb(familia)
        (d / f"v{version:04d}.json").write_text(json.dumps(reg, ensure_ascii=False, indent=1), encoding="utf-8")
        (d / "vigente.json").write_text(json.dumps(reg, ensure_ascii=False, indent=1), encoding="utf-8")
        return reg

    def versiones_linea_base(self, familia: str) -> list[dict]:
        return [json.loads(p.read_text(encoding="utf-8")) for p in sorted(self._dir_lb(familia).glob("v[0-9]*.json"))]
