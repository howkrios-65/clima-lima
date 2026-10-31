"""Higiene del equipo de agentes: encabezados válidos, permisos mínimos, neutralidad y reglas de la base de conocimiento."""
import re
from pathlib import Path

import pytest
import yaml

import reliability_kit

ROOT = Path(__file__).resolve().parents[3]
AGENTS = ROOT / ".claude" / "agents"
KNOW = ROOT / "knowledge"
LEAD = "reliability-engineer"
SPECIALISTS = {
    "reliability-data-auditor", "reliability-life-analyst", "reliability-rca-investigator", "reliability-fmeca-rcm",
    "reliability-predictive-analyst", "reliability-economics-kpi", "reliability-evidence-verifier",
    "reliability-report-writer", "reliability-memory-curator", "reliability-literature-researcher", "reliability-case-historian", "reliability-dataset-scout", "reliability-feedback-learner", "reliability-integrator", "reliability-paper-analyst", "reliability-replicator", "reliability-citation-ranker", "reliability-ux-designer", "reliability-standards-researcher",
}
VALID_TOOLS = {"Read", "Write", "Edit", "Glob", "Grep", "Bash", "WebSearch", "WebFetch", "Skill"}
# Empresas y productos que no deben aparecer en agentes, base de conocimiento, catálogo ni kit
BANNED = re.compile(r"orquest|antamina|larox|komatsu|reliability mining|shiploader|codelco|southern copper|rio tinto|"
                    r"\bbhp\b|\bppl\b|\bibm\b|siemens|aspen|ge vernova|augury|uptake|cognite|power ?bi|maximo|"
                    r"mlflow|roboflow|\bsap\b|\brmes\b|oxmaint|verdantix|fiix|maintainx|senseye|mtell", re.I)


def split(path):
    text = path.read_text(encoding="utf-8")
    m = re.match(r"---\n(.*?)\n---\n(.*)", text, re.S)
    assert m, f"{path.name}: sin encabezado"
    return yaml.safe_load(m.group(1)), m.group(2), text


def agent_files():
    return sorted(AGENTS.glob("*.md"))


def text_files(*bases):
    for b in bases:
        b = ROOT / b
        yield from (p for p in ([b] if b.is_file() else b.rglob("*")) if p.is_file() and p.suffix in {".md", ".yaml", ".py", ".html", ".txt"}
                    and "__pycache__" not in p.parts and ".pytest_cache" not in p.parts)


def test_ten_agents_present_and_headers_valid():
    names = set()
    for p in agent_files():
        fm, body, _ = split(p)
        assert fm["name"] == p.stem, p.name
        assert fm["description"] and "\n" not in fm["description"].strip()
        assert fm["model"] == "inherit"
        names.add(fm["name"])
    assert names == SPECIALISTS | {LEAD}


def test_lead_allowlist_matches_specialists_exactly():
    fm, _, _ = split(AGENTS / f"{LEAD}.md")
    m = re.match(r"Agent\(([^)]*)\)", fm["tools"])
    assert m
    assert {x.strip() for x in m.group(1).split(",")} == SPECIALISTS


def test_specialists_use_least_privilege_tools():
    for name in SPECIALISTS:
        fm, _, _ = split(AGENTS / f"{name}.md")
        tools = {t.strip() for t in fm["tools"].split(",")}
        assert {t for t in tools if not t.startswith("mcp__")} <= VALID_TOOLS, (name, tools - VALID_TOOLS)
        assert not any(t.startswith("Agent") for t in tools), f"{name} no debe invocar a otros agentes"
    tools = lambda n: {t.strip() for t in split(AGENTS / f"{n}.md")[0]["tools"].split(",")}
    assert not (tools("reliability-evidence-verifier") & {"Write", "Edit", "Bash"})     # verificador de solo lectura
    assert "Bash" not in tools("reliability-memory-curator")                            # curador solo escribe archivos
    assert "Write" in tools("reliability-memory-curator")
    for n in ("reliability-rca-investigator", "reliability-fmeca-rcm", "reliability-predictive-analyst"):
        assert "Write" not in tools(n)                                                   # los analistas no escriben informes


def test_every_agent_reads_common_protocol_and_is_neutral():
    for p in agent_files():
        _, _, text = split(p)
        assert "knowledge/protocolo_comun.md" in text or p.stem == LEAD, p.name
        if p.stem != LEAD:
            assert re.search(r"No nombres empresas", text), f"{p.name} sin regla de neutralidad"


def test_kit_functions_cited_by_agents_exist():
    cited = {"audit", "temporal_split", "group_split", "assert_no_overlap", "pr_metrics", "recall_at_precision",
             "cost_optimal_threshold", "brier_and_calibration", "laplace_trend_test", "fit_crow_amsaa",
             "mean_cumulative_function", "fit_crow_amsaa_multi", "laplace_trend_test_multi", "unit_heterogeneity_test",
             "compare_models_verdict", "bias_correct_beta", "gof_censored_bootstrap", "weibull_beta_ci_lr",
             "weibull_b_life_ci_lr", "km_failure_quantile", "weibull_bootstrap_ci", "optimal_age_replacement", "npv",
             "eac", "inherent_availability", "audit_recurrent"}
    text = "\n".join(p.read_text(encoding="utf-8") for p in agent_files()) + (KNOW / "metodos_lider.md").read_text(encoding="utf-8")
    for fn in cited:
        assert hasattr(reliability_kit, fn), fn
        assert fn in text, f"{fn} ya no lo cita ningún agente"


def test_no_section_sign_anywhere():
    sign = chr(0xA7)      # signo de sección: se arma con su código para que este archivo no lo contenga
    offenders = [str(p.relative_to(ROOT)) for p in text_files(".claude", "knowledge", "docs", "reports", "research_notes", "tools")
                 if sign in p.read_text(encoding="utf-8", errors="ignore")]
    assert not offenders, offenders


def test_no_company_or_product_names_in_agents_knowledge_docs_and_kit():
    offenders = []
    skip = {Path(__file__).resolve(), (ROOT / ".claude" / "hooks" / "chequeo.py").resolve()}   # el hook necesita la lista de nombres para vigilarlos
    for p in text_files(".claude", "knowledge", "docs/agentes", "tools/reliability"):
        if p.resolve() in skip:
            continue
        for i, line in enumerate(p.read_text(encoding="utf-8", errors="ignore").splitlines(), 1):
            if BANNED.search(line):
                offenders.append(f"{p.relative_to(ROOT)}:{i}: {line.strip()[:80]}")
    assert not offenders, "\n".join(offenders[:15])


def test_registro_normas_rules():
    data = yaml.safe_load((KNOW / "registro_normas.yaml").read_text(encoding="utf-8"))["normas"]
    assert len(data) > 40
    ids = [n["id"] for n in data]
    assert len(ids) == len(set(ids)), "ids duplicados"
    for n in data:
        assert n["verificacion"] in {"VERIFICADO", "SOLO-SNIPPET", "NO-VERIFICADO"}, n["id"]
        if n["verificacion"] == "VERIFICADO":      # solo se sube de nivel con persona y fecha
            assert n.get("verificado_por") and n.get("fecha_verificacion"), n["id"]
        assert n.get("tema") and "estado_segun_notas" in n, n["id"]


def test_memory_gates_hold():
    approved = [p for p in (KNOW / "memoria" / "aprobada").glob("*.md")]
    for p in approved:      # nada aprobado sin persona
        assert re.search(r"^aprobado_por:\s*\S+", p.read_text(encoding="utf-8"), re.M) and "aprobado_por: null" not in p.read_text(encoding="utf-8"), p.name
    for p in (KNOW / "memoria" / "cuarentena").glob("L-*.md"):
        t = p.read_text(encoding="utf-8")
        for field in ("id:", "fuente:", "extracto:", "estado:", "propuesto_por:", "revisar_antes_de:"):
            assert field in t, (p.name, field)
        assert "estado: propuesta" in t or "estado: retractada" in t, p.name


FICHA = ["ROL Y NIVEL", "CONTEXTO", "OBJETIVO Y DECISIÓN", "INSUMOS", "TAREA", "MÉTODO Y ESTÁNDARES", "HONESTIDAD",
         "FORMATO DE SALIDA", "CALIDAD", "RESTRICCIONES Y DUDAS", "FEEDBACK", "ALMACENAMIENTO"]


def test_ficha_de_10_bloques_mas_2_operativos_en_los_20_agentes():
    import re
    for p in agent_files():
        t = p.read_text(encoding="utf-8")
        a = t.index("## FICHA DEL AGENTE")
        bloque = t[a:a + 6000]
        titulos = re.findall(r"^(\d+)\. \*\*([^:*]+):\*\*", bloque, re.M)[:12]
        assert [n for n, _ in titulos] == [str(i) for i in range(1, 13)], p.name
        assert [x for _, x in titulos] == FICHA, p.name
        assert "knowledge/protocolo_comun.md" in bloque, f"{p.name}: el bloque de honestidad debe apuntar al protocolo común"
