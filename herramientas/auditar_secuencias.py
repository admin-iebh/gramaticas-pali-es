#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Comprueba que cada paso de una secuencia cite un aforismo que haga esa clase
de operación.

    python3 herramientas/auditar_secuencias.py
    python3 herramientas/auditar_secuencias.py --seccion sara

Las secuencias de recursos/sandhi/reglas.json no están en el documento de
Nandisena: él da entrada, resultado y referencia canónica. Los pasos
intermedios y sus citas §N son reconstrucción editorial. Esta herramienta no
puede demostrar que una cita sea correcta; sólo detecta la incoherencia más
gruesa: que el paso haga una cosa —elidir, alargar, insertar— y el aforismo
citado haga otra.

Un aviso no es necesariamente un error: varias operaciones pueden coincidir
en un paso, y algunos aforismos actúan de formas que la clasificación
automática no distingue. Sirve para dirigir la revisión humana, no para
sustituirla.

Y al revés, y esto importa más: que un paso pase la comprobación no dice que
la cita sea correcta. Sólo dice que el aforismo citado hace esa CLASE de
operación. Si un paso elide y cita §12, pasa —aunque el aforismo correcto
fuera §13, que también elide.

Limitaciones conocidas, comprobadas a mano y consideradas aceptables:

  §15 en «tad ā ahaṃ → tad āhaṃ»
      Las dos vocales son ā y a; tras la operación queda una sola. No hay
      manera automática de saber cuál sobrevivió, así que el paso se
      clasifica como elisión y no como alargamiento.

  §44 y §45 en «abhi uggato → abbh uggato»
      Sustituyen un segmento entero —abhi por abbh, adhi por ajjh—, lo que
      al alinear letra a letra parece duplicación más elisión.
"""

import argparse
import json
import os
import re
import sys
import unicodedata
from collections import Counter
from difflib import SequenceMatcher

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REGLAS = os.path.join(RAIZ, "recursos", "sandhi", "reglas.json")

# ── Qué hace cada aforismo ──────────────────────────────────────────────
# Derivado de la glosa y del vutti de kaccayana/01-sandhi-kappa.md, y
# revisado a mano. Si una traducción cambia, hay que revisar esta tabla.
OPERACIONES = {
    10: {"separacion"},
    11: {"union"},
    12: {"elision"},
    13: {"elision"},
    14: {"sustitucion"},
    15: {"alargamiento"},
    16: {"alargamiento"},
    17: {"sustitucion"},
    18: {"sustitucion"},
    19: {"sustitucion", "duplicacion"},
    20: {"sustitucion"},
    21: {"sustitucion"},
    22: {"sustitucion", "acortamiento"},
    23: {"sin_cambio"},
    24: {"sin_cambio"},
    25: {"alargamiento"},
    26: {"acortamiento"},
    27: {"elision", "sustitucion"},
    28: {"duplicacion"},
    29: {"sustitucion", "duplicacion"},
    30: {"sustitucion"},
    31: {"sustitucion"},
    32: {"sustitucion", "duplicacion"},
    33: {"sustitucion", "duplicacion"},
    34: {"sustitucion"},
    35: {"insercion"},
    36: {"insercion"},
    37: {"insercion"},
    38: {"elision"},
    39: {"elision"},
    40: {"elision"},
    41: {"sustitucion", "elision"},
    42: {"insercion"},
    43: {"insercion", "acortamiento"},
    44: {"sustitucion"},
    45: {"sustitucion"},
    46: {"sin_cambio"},
    47: {"sin_cambio"},
    48: {"sustitucion"},
    49: {"sustitucion"},
    50: {"sustitucion"},
}

NOMBRE = {"separacion": "separación", "union": "unión", "elision": "elisión",
          "insercion": "inserción", "alargamiento": "alargamiento",
          "acortamiento": "acortamiento", "sustitucion": "sustitución",
          "duplicacion": "duplicación", "sin_cambio": "sin cambio"}

LARGAS = {"ā": "a", "ī": "i", "ū": "u"}
CORTAS = {v: k for k, v in LARGAS.items()}


def texto(paso):
    return re.sub(r'\s*\(([^)]*)\)\s*$', '', paso).strip()


def citas(paso):
    m = re.search(r'\(([^)]*)\)\s*$', paso)
    return [int(x) for x in re.findall(r'§(\d+)', m.group(1))] if m else []


def clasificar(antes, despues):
    """Qué clases de operación median entre dos pasos.

    Un paso puede hacer varias cosas a la vez —elidir la vocal anterior y
    alargar la siguiente, por ejemplo—, así que se alinean las dos cadenas y
    se clasifica cada tramo que cambia, no sólo el saldo de longitud.
    """
    ops = set()
    if despues.count(" ") > antes.count(" "):
        ops.add("separacion")
    if despues.count(" ") < antes.count(" "):
        ops.add("union")

    limpia = lambda t: unicodedata.normalize("NFC", t.replace(" ", "").replace("’", ""))
    a, b = limpia(antes), limpia(despues)
    if a == b:
        if not ops:
            ops.add("sin_cambio")
        return ops

    for tag, i1, i2, j1, j2 in SequenceMatcher(None, a, b).get_opcodes():
        if tag == "equal":
            continue
        orig, dest = a[i1:i2], b[j1:j2]
        if tag == "delete":
            ops.add("elision")
        elif tag == "insert":
            previo = b[j1 - 1] if j1 else ""
            siguiente = b[j2] if j2 < len(b) else ""
            if dest and (dest[0] == previo or dest[-1] == siguiente):
                ops.add("duplicacion")
            else:
                ops.add("insercion")
        else:                                   # replace
            if len(orig) == len(dest):
                for x, y in zip(orig, dest):
                    if x == y:
                        continue
                    if LARGAS.get(y) == x:
                        ops.add("alargamiento")
                    elif CORTAS.get(y) == x:
                        ops.add("acortamiento")
                    else:
                        ops.add("sustitucion")
            elif len(dest) == 1 and LARGAS.get(dest) and LARGAS[dest] in orig:
                # la vocal anterior se elide y la siguiente se alarga
                ops.add("elision")
                ops.add("alargamiento")
            elif len(dest) == 1 and CORTAS.get(dest) and dest in [LARGAS.get(c, c) for c in orig]:
                ops.add("elision")
                ops.add("acortamiento")
            else:
                ops.add("sustitucion")
                if len(dest) < len(orig):
                    ops.add("elision")
                elif len(dest) > len(orig):
                    ops.add("insercion")
    return ops


def auditar(seccion=None):
    d = json.load(open(REGLAS, encoding="utf-8"))
    avisos, revisados, pasos_con_cita = [], 0, 0
    sin_tabla = Counter()

    for c in d["ce"]:
        if seccion and c["sec"] != seccion:
            continue
        revisados += 1
        for antes, despues in zip(c["s"], c["s"][1:]):
            nums = citas(despues)
            if not nums:
                continue
            pasos_con_cita += 1
            ops = clasificar(texto(antes), texto(despues))
            for n in nums:
                esperado = OPERACIONES.get(n)
                if esperado is None:
                    sin_tabla[n] += 1
                    continue
                if not (ops & esperado):
                    avisos.append({
                        "forma": "{0} {1} · {2}".format(c["sec"], c["rule"], c["f"]),
                        "paso": "{0} → {1}".format(texto(antes), texto(despues)),
                        "cita": n,
                        "hace": sorted(NOMBRE[o] for o in ops),
                        "esperado": sorted(NOMBRE[o] for o in esperado),
                    })
    return avisos, revisados, pasos_con_cita, sin_tabla


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--seccion", help="sara, byanjana, niggahita o pakati")
    a = ap.parse_args()

    avisos, revisados, pasos, sin_tabla = auditar(a.seccion)

    print("{0} formas · {1} pasos con cita §N".format(revisados, pasos))
    if sin_tabla:
        print("  aforismos sin entrada en la tabla de operaciones: {0}".format(
            ", ".join("§{0}".format(k) for k in sorted(sin_tabla))))
    print()

    if not avisos:
        print("Ningún paso contradice la operación de su aforismo.")
        return 0

    por_seccion = Counter(x["forma"].split()[0] for x in avisos)
    print("{0} pasos que merecen revisión, en {1} formas:".format(
        len(avisos), len({x["forma"] for x in avisos})))
    print("  por sección: {0}".format(dict(por_seccion)))
    print()
    for x in avisos:
        print("  §{0} — {1}".format(x["cita"], x["forma"]))
        print("      {0}".format(x["paso"]))
        print("      el paso hace: {0}   ·   §{1} hace: {2}".format(
            ", ".join(x["hace"]), x["cita"], ", ".join(x["esperado"])))
        print()
    return 1


if __name__ == "__main__":
    sys.exit(main())
