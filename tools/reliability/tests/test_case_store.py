import json

import numpy as np
import pytest

from reliability_kit import CaseStore, CasoInvalido, familia_de


def caso(id_, fecha, unidad="AG-01", t=None, mecs=("fatiga a flexión en raíz de diente", "micropitting"), **kw):
    c = {"id": id_, "titulo": f"Falla {id_}", "activo_clase": "Reductor de agitador", "modo_falla": "Rotura de diente de piñón",
         "unidad": unidad, "fecha_falla": fecha, "mecanismos": list(mecs)}
    if t is not None:
        c["t_operacion"] = t
    c.update(kw)
    return c


def test_register_validates_and_never_overwrites(tmp_path):
    s = CaseStore(tmp_path)
    r = s.registrar_caso(caso("C-001", "2026-09-28"))
    assert r["version"] == 1 and r["familia"] == "reductor_de_agitador__rotura_de_diente_de_pinon" and len(r["hash_entrada"]) == 64
    with pytest.raises(CasoInvalido):
        s.registrar_caso(caso("C-001", "2026-09-28"))                       # no se sobrescribe
    v2 = s.registrar_caso(caso("C-001", "2026-09-29"), nueva_version=True)
    assert v2["version"] == 2 and json.loads((tmp_path / "casos/C-001/caso.v1.json").read_text())["fecha_falla"] == "2026-09-28"
    for malo in ({"id": "x"}, {**caso("C-002", "28/09/2026")}, {**caso("C-003", "2026-09-28"), "mecanismos": "texto"},
                 {**caso("C-004", "2026-09-28"), "t_operacion": -5}, {**caso("C 5", "2026-09-28")}):
        with pytest.raises(CasoInvalido):
            s.registrar_caso(malo)


def test_recurrence_rules(tmp_path):
    s = CaseStore(tmp_path)
    s.registrar_caso(caso("C-001", "2026-01-10"))
    s.registrar_caso(caso("C-002", "2026-03-01", unidad="AG-02", mecs=("desgaste abrasivo de sello",),
                          modo_falla="Fuga de sello", activo_clase="Bomba de pulpa"))
    nuevo = caso("C-003", "2026-09-28")
    r = s.buscar_recurrencia(nuevo)
    assert [x["caso_previo"] for x in r] == ["C-001"]                         # el caso de la bomba no se parece
    assert r[0]["es_recurrencia"] and "misma_unidad" in r[0]["coincidencias"] and r[0]["intervalo_entre_fallas_mismo_equipo_dias"] == 261
    otra_unidad = s.buscar_recurrencia(caso("C-004", "2026-10-01", unidad="AG-09"))
    assert otra_unidad[0]["es_recurrencia"] is False or "misma_familia" in otra_unidad[0]["coincidencias"]
    assert s.buscar_recurrencia(caso("C-005", "2026-10-02", unidad="X", activo_clase="Transformador", modo_falla="Aislación",
                                      mecanismos=["descarga parcial"])) == []


def test_baseline_is_void_until_there_is_data_then_versions(tmp_path):
    s = CaseStore(tmp_path)
    fam = familia_de(caso("C-001", "2026-01-10"))
    s.registrar_caso(caso("C-001", "2026-01-10", unidad="U1", t=2000))
    v1 = s.actualizar_linea_base(fam, "primer caso")
    assert v1["estado"] == "sin_base" and "VACÍO" in v1["advertencias"][0] and v1["version"] == 1
    rng = np.random.default_rng(0)
    vidas = 3000 * rng.weibull(2.0, 12)
    cens = [{"unidad": f"S{i}", "t_operacion": float(2500 + 100 * i)} for i in range(8)]
    for i, t in enumerate(vidas[:10]):
        s.registrar_caso(caso(f"C-1{i:02d}", f"2026-02-{i + 1:02d}", unidad=f"V{i}", t=float(t), censuras=cens))
    v2 = s.actualizar_linea_base(fam, "10 fallas nuevas")
    assert v2["estado"] == "calculada" and v2["version"] == 2 and v2["metodo"] == "weibull_censura" and v2["n_fallas"] == 11
    assert v2["resultado"]["beta_ic95_lr"][0] < v2["resultado"]["beta"] < v2["resultado"]["beta_ic95_lr"][1]
    assert "beta_corregido_sesgo" in v2["resultado"]                                   # menos de 30 fallas
    assert any("exploratorio" in a or "30" in a for a in v2["advertencias"])
    assert s.linea_base_vigente(fam)["version"] == 2 and [v["version"] for v in s.versiones_linea_base(fam)] == [1, 2]
    assert (tmp_path / "linea_base" / fam / "v0001.json").exists()                      # la anterior se conserva


def test_baseline_flags_a_shift_when_new_failures_change_the_pattern(tmp_path):
    s = CaseStore(tmp_path)
    fam = familia_de(caso("C-1", "2026-01-01"))
    rng = np.random.default_rng(1)
    for i, t in enumerate(3000 * rng.weibull(3.0, 25)):
        s.registrar_caso(caso(f"A-{i:03d}", f"2025-01-{i % 28 + 1:02d}", unidad=f"U{i}", t=float(t)))
    a = s.actualizar_linea_base(fam, "línea base inicial")
    for i, t in enumerate(400 * rng.weibull(1.0, 40)):                                   # llegan fallas tempranas y aleatorias
        s.registrar_caso(caso(f"B-{i:03d}", f"2026-02-{i % 28 + 1:02d}", unidad=f"W{i}", t=float(t) + 1))
    b = s.actualizar_linea_base(fam, "recurrencias tempranas")
    c = b["cambio_respecto_version_anterior"]
    assert c["version_anterior"] == 1 and c["beta_anterior_dentro_del_ic_nuevo"] is False
    assert "posible cambio" in c["interpretacion"] and a["resultado"]["beta"] > b["resultado"]["beta"]


def test_repeated_failures_of_same_unit_use_repairable_model_and_need_end_times(tmp_path):
    s = CaseStore(tmp_path)
    fam = familia_de(caso("C-1", "2026-01-01"))
    for i, (u, t) in enumerate([("U1", 100), ("U1", 220), ("U1", 300), ("U2", 150), ("U2", 260), ("U3", 90)]):
        s.registrar_caso(caso(f"R-{i}", f"2026-01-{i + 1:02d}", unidad=u, t=float(t)))
    v = s.actualizar_linea_base(fam, "reparables sin fin de observación")
    assert v["metodo"] == "nhpp_multiunidad" and v["estado"] == "sin_base" and "fin_observacion" in v["advertencias"][0]
    s.registrar_caso(caso("R-9", "2026-02-01", unidad="U3", t=210.0, fin_observacion={"U1": 320.0, "U2": 280.0, "U3": 230.0}))
    v = s.actualizar_linea_base(fam, "con fin de observación")
    assert v["estado"] == "calculada" and "beta" in v["resultado"] and "tendencia" in v["resultado"]
