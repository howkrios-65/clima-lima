import datetime as dt
import json

import pytest

from reliability_kit import EvidenciaInvalida, Ledger, apa, validar_entrada


def base(**kw):
    e = {"id": "E-0001", "tipo": "paper", "acceso": "fragmento", "via": "wiley_scholar_gateway", "fecha_acceso": "2026-10-27",
         "referencia": {"autores": "Prajapati, D. K., & Tiwari, M.", "anio": 2019, "titulo": "Experimental investigation on evolution of surface damage",
                        "fuente": "Fatigue & Fracture of Engineering Materials & Structures", "volumen": "43(2)", "paginas": "355-370",
                        "doi": "10.1111/ffe.13150", "pais": "India", "institucion": "IIT Delhi"},
         "extracto": "micropitting is perceived as one of the most dominant failure mechanisms", "localizador": "Introducción, fragmento 1",
         "afirma": "El micropitting es un mecanismo de fatiga por contacto dominante en engranajes endurecidos.",
         "limites": "Ensayos de disco; no engranajes cónicos de planta."}
    e.update(kw)
    return e


def test_valid_entry_gets_derived_level():
    L = Ledger([base()])
    assert L.nivel_de("E-0001") == "VERIFICADO-TEXTO"
    assert L.avisos["E-0001"] == []


@pytest.mark.parametrize("campo,valor,frag", [
    ("extracto", "", "extracto literal"), ("localizador", "", "localizador"), ("afirma", "", "afirma"), ("limites", "", "limites"),
    ("fecha_acceso", "27/10/2026", "AAAA-MM-DD"), ("fecha_acceso", "2999-01-01", "futuro"), ("id", "E-1", "formato"),
    ("tipo", "blog", "tipo inválido"), ("acceso", "leido", "acceso inválido"), ("extracto", "x" * 900, "demasiado largo"),
])
def test_gates_block_unverifiable_claims(campo, valor, frag):
    err, _ = validar_entrada(base(**{campo: valor}))
    assert any(frag in x for x in err), err


def test_web_search_cannot_claim_reading():
    err, _ = validar_entrada(base(via="websearch"))
    assert any("resúmenes" in x for x in err)
    ok = Ledger([base(via="websearch", acceso="snippet", extracto=None, localizador=None)])
    assert ok.nivel_de("E-0001") == "SOLO-SNIPPET"


def test_quartile_requires_its_source_and_range():
    err, _ = validar_entrada(base(revista_cuartil={"valor": 1, "fuente": None}))
    assert any("fuente" in x for x in err)
    err, _ = validar_entrada(base(revista_cuartil={"valor": 7, "fuente": "SJR 2024"}))
    assert any("1 a 4" in x for x in err)
    L = Ledger([base(revista_cuartil={"valor": 1, "fuente": "SJR 2024", "anio": 2024})])
    assert L.resumen()["cuartil_verificado"] == {"Q1": 1}
    assert Ledger([base()]).resumen()["sin_cuartil_verificado"] == 1


def test_doi_format_and_duplicates():
    err, _ = validar_entrada(base(referencia={**base()["referencia"], "doi": "https://doi.org/10.1111/x"}))
    assert any("doi" in x.lower() for x in err)
    L = Ledger([base()])
    with pytest.raises(EvidenciaInvalida):
        L.add(base(id="E-0002"))            # mismo DOI
    with pytest.raises(EvidenciaInvalida):
        L.add(base(referencia={**base()["referencia"], "doi": "10.1000/otro"}))   # mismo id


def test_paper_requires_core_reference_fields_and_warns_without_doi():
    r = base()["referencia"]
    err, _ = validar_entrada(base(referencia={k: v for k, v in r.items() if k != "autores"}))
    assert any("autores" in x for x in err)
    _, warn = validar_entrada(base(referencia={k: v for k, v in r.items() if k != "doi"}))
    assert any("sin DOI" in x for x in warn)


def test_claim_support_gate():
    L = Ledger([base(), base(id="E-0002", acceso="snippet", via="websearch", extracto=None, localizador=None,
                             referencia={**base()["referencia"], "doi": "10.1000/b"}),
                base(id="E-0003", acceso="abstract", referencia={**base()["referencia"], "doi": "10.1000/c"})])
    assert L.puede_afirmar(["E-0001", "E-0003"], "VERIFICADO-ABSTRACT") == (True, [])
    assert L.puede_afirmar(["E-0001", "E-0003"], "VERIFICADO-TEXTO") == (False, ["E-0003"])
    assert L.puede_afirmar(["E-0001", "E-0002"]) == (False, ["E-0002"])
    assert L.puede_afirmar(["E-9999"])[0] is False
    with pytest.raises(EvidenciaInvalida):
        L.exigir(["E-0002"])


def test_retracted_source_cannot_support_and_user_data_level(tmp_path):
    L = Ledger([base(estado_retractado=True)])
    assert L.puede_afirmar(["E-0001"]) == (False, ["E-0001"])
    d = {"id": "E-0002", "tipo": "dato_usuario", "fecha_acceso": "2026-10-27", "via": "usuario", "afirma": "Registro de mantenimiento aportado",
         "limites": "No verificado de forma independiente", "referencia": {}}
    L.add(d)
    assert L.nivel_de("E-0002") == "DATO-USUARIO"
    p = tmp_path / "l.json"
    L.to_json(p)
    assert [e["id"] for e in json.loads(p.read_text())] == ["E-0001", "E-0002"]
    assert Ledger.from_json(p).nivel_de("E-0002") == "DATO-USUARIO"


def test_apa_uses_only_present_fields():
    s = apa(base())
    assert s.startswith("Prajapati, D. K., & Tiwari, M. (2019).") and "https://doi.org/10.1111/ffe.13150" in s
    sin = apa({"referencia": {"titulo": "Informe interno"}})
    assert "(s. f.)" in sin and "Autor no identificado" in sin


def test_summary_counts_by_level_type_country():
    L = Ledger([base(), base(id="E-0002", referencia={**base()["referencia"], "doi": "10.1000/b", "pais": "Alemania"}, tipo="tesis")])
    r = L.resumen()
    assert r["total"] == 2 and r["por_nivel"] == {"VERIFICADO-TEXTO": 2} and r["por_tipo"] == {"paper": 1, "tesis": 1}
    assert r["por_pais"] == {"India": 1, "Alemania": 1}
