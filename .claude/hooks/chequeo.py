#!/usr/bin/env python3
"""Compuertas deterministas del equipo de confiabilidad (sin costo de tokens).

Uso: chequeo.py post   -> PostToolUse (Write|Edit): revisa el archivo recién escrito.
     chequeo.py stop   -> Stop: revisa los archivos modificados en git.
     chequeo.py todo   -> revisa todo lo versionado en las carpetas vigiladas.

Reglas duras (bloquean al cerrar): término prohibido para el coordinador, símbolo de párrafo, JSON inválido.
Aviso (no bloquea): nombres de empresas fabricantes o proveedores.
"""
import json, os, re, subprocess, sys

RAIZ = os.environ.get("CLAUDE_PROJECT_DIR") or subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True).stdout.strip() or "."
VIGILADO = ("historial/", "docs/", "knowledge/", ".claude/agents/", ".claude/commands/", "CLAUDE.md", "research_notes/", "reports/")
EXT = (".md", ".json", ".jsonl", ".html", ".yaml", ".yml", ".txt", ".js")
# El término prohibido se arma por partes para que este archivo no se marque a sí mismo.
PROHIBIDO = re.compile("orq" + "uest" + r"\w*", re.I)
PARRAFO = chr(0xA7)
EMPRESAS = re.compile(r"\b(SKF|FAG|NSK|NTN|NTT|KSB|ABB|Timken|Schaeffler|Emerson|Flowserve|Sulzer|Goulds|Grundfos|Hitachi|Siemens|Garlock|Chesterton|AESSEAL|John Crane|Burgmann|Antamina|Hivimar|Fabrico|Darley|Nash Pumps|Reliabilityweb|Machinery Lubrication)\b")


def vigilado(ruta):
    r = os.path.relpath(ruta, RAIZ).replace(os.sep, "/")
    return r.startswith(VIGILADO) and r.endswith(EXT) and not r.startswith(".claude/hooks/")


def revisar(ruta):
    duro, aviso = [], []
    try:
        txt = open(ruta, encoding="utf-8", errors="replace").read()
    except OSError:
        return duro, aviso
    rel = os.path.relpath(ruta, RAIZ)
    for n, linea in enumerate(txt.splitlines(), 1):
        if PROHIBIDO.search(linea):
            duro.append(f"{rel}:{n}: término prohibido para el coordinador (usa LÍDER o ESTRATEGA)")
        if PARRAFO in linea:
            duro.append(f"{rel}:{n}: símbolo de párrafo")
        m = EMPRESAS.search(linea)
        if m:
            aviso.append(f"{rel}:{n}: posible nombre de empresa «{m.group(1)}» (la regla es no nombrar empresas)")
    if ruta.endswith((".json",)):
        try:
            json.loads(txt)
        except ValueError as e:
            duro.append(f"{rel}: JSON inválido ({str(e)[:60]})")
    return duro, aviso


def cambiados():
    out = subprocess.run(["git", "-C", RAIZ, "status", "--porcelain"], capture_output=True, text=True).stdout
    return [os.path.join(RAIZ, l[3:].strip().strip('"')) for l in out.splitlines() if len(l) > 3]


def versionados():
    out = subprocess.run(["git", "-C", RAIZ, "ls-files"], capture_output=True, text=True).stdout
    return [os.path.join(RAIZ, l) for l in out.splitlines()]


def main():
    modo = sys.argv[1] if len(sys.argv) > 1 else "stop"
    if modo == "post":
        try:
            ruta = json.load(sys.stdin).get("tool_input", {}).get("file_path", "")
        except ValueError:
            return 0
        archivos = [ruta] if ruta else []
    elif modo == "todo":
        archivos = versionados()
    else:
        try:
            if json.load(sys.stdin).get("stop_hook_active"):
                return 0
        except ValueError:
            pass
        archivos = cambiados()
    duros, avisos = [], []
    for a in archivos:
        if os.path.isfile(a) and vigilado(a):
            d, w = revisar(a)
            duros += d; avisos += w
    if modo == "todo":
        print(f"{len(duros)} problemas duros, {len(avisos)} avisos")
        for x in (duros + avisos)[:40]:
            print(" ", x)
        return 1 if duros else 0
    if duros or (modo == "post" and avisos):
        sys.stderr.write("Compuerta de lenguaje del equipo:\n" + "\n".join(("- " + x) for x in (duros + (avisos if modo == "post" else []))[:12]) + "\nCorrige y vuelve a guardar.\n")
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
