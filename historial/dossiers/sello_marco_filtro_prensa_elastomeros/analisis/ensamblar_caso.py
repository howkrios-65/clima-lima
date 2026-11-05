"""Ensambla informe.html con el kit, agregando el abstract y corrigiendo el KPI cuando ninguna sección tiene evidencia leída."""
import json, sys
from pathlib import Path
sys.path.insert(0, "/home/user/clima-lima/tools/reliability")
import reliability_kit, importlib; E = importlib.import_module("reliability_kit.ensamblar")
C = Path("/home/user/clima-lima/historial/dossiers/sello_marco_filtro_prensa_elastomeros")
orig = E.construir_informe
def wrap(caso, L, salida):
    caso["abstract"] = json.loads((C / "abstract.json").read_text(encoding="utf-8"))
    for k in caso["resumen"]["kpis"]:
        if k["label"].startswith("secciones con evidencia"):
            k["valor"] = "0 de 13"
    caso["meta"]["titulo"] = "Dossier del modo de falla: sello de marco de un filtro de prensa de placas y sus elastómeros"
    return orig(caso, L, salida)
E.construir_informe = wrap
r = E.ensamblar(C, simulador=False)
print("ajustes:", json.dumps(r["ajustes"], ensure_ascii=False)); print(r["resumen_evidencia"])
