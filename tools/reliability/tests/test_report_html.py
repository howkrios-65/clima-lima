import json
import shutil
import subprocess
import tempfile
from pathlib import Path

import numpy as np
import pytest

from reliability_kit import Ledger, fit_weibull_mle, weibull_b_life_ci_lr, weibull_beta_ci_lr
from reliability_kit import report_html as rh

HOY = "2026-10-01"


def _entrada(i, tipo="paper", acceso="fragmento", doi=None):
    e = {"id": f"E-{i:04d}", "tipo": tipo, "acceso": acceso, "via": "conector", "fecha_acceso": HOY,
         "referencia": {"autores": "Autor, A.", "anio": 2020, "titulo": f"Titulo {i}", "fuente": "Rev", "doi": doi or f"10.1000/t{i}"},
         "afirma": "x", "limites": "y"}
    if acceso in ("fragmento", "abstract", "texto_completo"):
        e["extracto"] = "texto literal"
        e["localizador"] = "p. 1"
    if tipo == "dato_usuario":
        e = {"id": f"E-{i:04d}", "tipo": "dato_usuario", "fecha_acceso": HOY, "referencia": {"titulo": "Serie aportada"},
             "afirma": "dato del caso", "limites": "origen por confirmar"}
    return e


def _ledger():
    return Ledger([_entrada(1), _entrada(2, acceso="snippet"), _entrada(3, tipo="dato_usuario"), _entrada(4, acceso="abstract")])


def _caso():
    rng = np.random.default_rng(7)
    t = np.round(rng.weibull(2.0, 12) * 1000 + 50, 1)
    c = np.zeros(12, bool); c[-3:] = True
    t = np.where(c, np.minimum(t, 900), t)
    f = fit_weibull_mle(t, c)
    return {
        "meta": {"titulo": "Caso </script><b>prueba", "fecha_evento": "2026-02-10", "origen_datos": "sintético de prueba"},
        "resumen": {"kpis": [{"label": "k", "valor": "1", "evidencia": ["E-0003"]}], "hallazgos": [{"id": "H1", "texto": "t", "evidencia": ["E-0003"]}, {"id": "H2", "texto": "sin", "evidencia": []}]},
        "linea_tiempo": [{"fecha": "2026-01-01", "tipo": "hito", "titulo": "a", "detalle": "b", "evidencia": ["E-0003"]}],
        "series": [{"id": "s", "titulo": "Vibración", "unidad": "mm/s", "base_n": 20, "k": 3, "persistencia": 3,
                    "puntos": [[f"2025-{1 + i // 28:02d}-{1 + i % 28:02d}", 2 + 0.01 * (i % 5) + (3 if i > 70 else 0)] for i in range(100)], "evidencia": ["E-0003"]}],
        "hipotesis": [
            {"id": "HIP1", "titulo": "con caso", "estado": "confirmada", "apoyo_caso": ["E-0003"], "apoyo_literatura": ["E-0001"]},
            {"id": "HIP2", "titulo": "solo literatura", "estado": "confirmada", "apoyo_caso": [], "apoyo_literatura": ["E-0001"]},
            {"id": "HIP3", "titulo": "snippet", "estado": "probable", "apoyo_caso": [], "apoyo_literatura": ["E-0002"]},
        ],
        "tecnicas": [{"id": "T1", "nombre": "5P", "raices": ["RC1"], "insumos": ["ot", "bitacora"], "evidencia": ["E-0004"]},
                     {"id": "T2", "nombre": "Ishikawa", "raices": ["RC1", "RC2"], "insumos": ["ot"], "evidencia": []}],
        "raices": [{"id": "RC1", "titulo": "r1"}, {"id": "RC2", "titulo": "r2"}],
        "vida": {"unidad": "h", "datos": [{"t": float(a), "censurado": bool(b)} for a, b in zip(t, c)],
                 "referencia": {"beta": f.beta, "eta": f.eta, "origen": "reliability_kit"}, "evidencia": ["E-0003"]},
    }


def test_compuertas_degradan_y_listan():
    r = rh.construir_informe(_caso(), _ledger())
    est = {a["donde"]: a for a in r["ajustes"]}
    assert est["hipótesis HIP2"]["a"] == "probable"          # literatura sin caso nunca confirma
    assert est["hipótesis HIP3"]["a"] == "posible"           # snippet no respalda
    assert "hipótesis HIP1" not in est
    assert any(a["tipo"] == "sin_evidencia" for a in r["ajustes"])


def test_id_inexistente_falla():
    c = _caso(); c["plan"] = [{"id": "A1", "accion": "x", "evidencia": ["E-9999"]}]
    with pytest.raises(ValueError):
        rh.construir_informe(c, _ledger())


def test_convergencia_cuenta_fuentes_distintas():
    cv = rh.construir_informe(_caso(), _ledger())["convergencia"]
    assert cv["por_raiz"]["RC1"]["n"] == 2 and cv["por_raiz"]["RC1"]["fuentes_distintas"] == 2
    assert cv["por_raiz"]["RC2"]["fuentes_distintas"] == 1


def test_json_no_rompe_el_script_ni_usa_red():
    html = rh.construir_informe(_caso(), _ledger())["html"]
    assert html.count("</script>") == 1                       # el título hostil no cierra la etiqueta
    assert "http://" not in html.replace("http://www.w3.org", "") and "src=\"http" not in html
    assert chr(0xA7) not in html


def test_no_modifica_el_caso_del_llamador():
    c = _caso(); copia = json.dumps(c, sort_keys=True)
    rh.construir_informe(c, _ledger())
    assert json.dumps(c, sort_keys=True) == copia


def _node_ok():
    if not shutil.which("node"):
        return False
    r = subprocess.run(["node", "-e", "require('playwright')"], capture_output=True)
    return r.returncode == 0


@pytest.mark.skipif(not _node_ok(), reason="node o playwright no disponible")
def test_navegador_sin_errores_y_autoprueba():
    with tempfile.TemporaryDirectory() as d:
        out = Path(d) / "i.html"
        rh.construir_informe(_caso(), _ledger(), out)
        js = """
const {chromium}=require('playwright');
(async()=>{const b=await chromium.launch();const p=await b.newPage();const errs=[];
p.on('pageerror',e=>errs.push(String(e)));p.on('console',m=>{if(m.type()==='error')errs.push(m.text())});
p.on('request',r=>{if(!r.url().startsWith('file:')&&!r.url().startsWith('data:'))errs.push('red:'+r.url())});
await p.goto('file://'+process.argv[1]);
const tabs=await p.$$eval('#tabs button',x=>x.map(y=>y.textContent));
for(const t of tabs){await p.click('#tabs button:has-text("'+t+'")');}
await p.click('#tabs button:has-text("Vida")');
const vida=await p.textContent('#v-vid');
await p.click('#tabs button:has-text("Señales")');
const sen=await p.textContent('#v-sen');
await p.click('#tabs button:has-text("Resumen")');await p.click('.chip');
const dr=await p.textContent('#drawer');
const grid=await p.textContent('#v-vid .grid');
console.log(JSON.stringify({grid,errs,tabs,vida:vida.includes('coinciden')&&!vida.includes('NO COINCIDEN'),alarma:sen.includes('Primera alarma'),dr:dr.length>20,listo:await p.evaluate(()=>window.__listo),er:await p.evaluate(()=>window.__errores||[])}));
await b.close()})();
"""
        r = subprocess.run(["node", "-e", js, str(out)], capture_output=True, text=True, timeout=120)
        assert r.returncode == 0, r.stderr
        o = json.loads(r.stdout.strip().splitlines()[-1])
        assert o["errs"] == [] and o["er"] == [], o
        c = _caso(); t = [x["t"] for x in c["vida"]["datos"]]; cs = [x["censurado"] for x in c["vida"]["datos"]]
        lo, hi = weibull_beta_ci_lr(t, cs); b = weibull_b_life_ci_lr(t, cs, p=0.10)
        assert f"[{lo:.2f}; {hi:.2f}]" in o["grid"] and f"[{b['lower']:.1f}; {b['upper']:.1f}]" in o["grid"], o["grid"]
        assert o["vida"] and o["alarma"] and o["dr"] and o["listo"], o
