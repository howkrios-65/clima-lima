from reliability_kit import Ledger, dossier

def _l():
    return Ledger([{"id": "E-0001", "tipo": "paper", "acceso": "fragmento", "via": "conector", "fecha_acceso": "2026-10-01",
                    "referencia": {"autores": "A, B.", "anio": 2020, "titulo": "T", "doi": "10.1000/x"}, "extracto": "texto", "localizador": "p. 1",
                    "afirma": "a", "limites": "b"},
                   {"id": "E-0002", "tipo": "paper", "acceso": "snippet", "via": "websearch", "fecha_acceso": "2026-10-01",
                    "referencia": {"autores": "A, B.", "anio": 2021, "titulo": "U", "doi": "10.1000/y"}, "afirma": "a", "limites": "b"}])

def _base(**kw):
    d = {"modo_falla": "x", "secciones": {s[0]: {"vacio": "no se halló", "elementos": []} for s in dossier.SECCIONES}}
    d["secciones"].update(kw)
    return d

def test_todo_vacio_con_motivo_es_valido():
    r = dossier.validar_dossier(_base(), _l())
    assert r["errores"] == [] and r["cobertura"]["vacias"] == 14

def test_elemento_sin_fuente_se_rechaza():
    r = dossier.validar_dossier(_base(fmeca={"elementos": [{"tipo": "tabla", "titulo": "t", "evidencia": []}]}), _l())
    assert any("sin fuente" in e for e in r["errores"])

def test_snippet_no_alcanza_y_id_inexistente_falla():
    r = dossier.validar_dossier(_base(fmeca={"elementos": [{"tipo": "valor", "titulo": "v", "evidencia": ["E-0002"]},
                                                          {"tipo": "figura", "titulo": "f", "evidencia": ["E-9"]}]}), _l())
    assert len(r["errores"]) == 2

def test_seccion_ok_cuenta_cobertura_y_vacio_sin_motivo_falla():
    r = dossier.validar_dossier(_base(fenomenos={"elementos": [{"tipo": "afirmacion", "titulo": "a", "evidencia": ["E-0001"]}]},
                                      ml={"elementos": []}), _l())
    assert r["cobertura"]["con_evidencia"] == 1 and any(e.startswith("ml") for e in r["errores"])
