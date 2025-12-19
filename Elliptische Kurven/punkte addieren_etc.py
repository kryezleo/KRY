#!/usr/bin/env python3
"""
Elliptische Kurve über GF(p) - Batch-Rechner für Aufgaben wie:
  "y^2 = x^3 + a*x + b over GF(p). Berechne (x1,y1)+(x2,y2), ..."

Anpassbar:
  p, a, b         -> Feld und Kurve
  queries         -> Liste von Tupeln ((x1,y1),(x2,y2))
  SHOW_STEPS      -> True/False für detaillierte Zwischenschritte
"""

from typing import Optional, Tuple, List

Point = Optional[Tuple[int,int]]  # None repräsentiert O (unendlich)

# ---------------------------
# === Konfiguration (anpassen)
# ---------------------------
p = 11        # Primzahl (GF(p))
a = 4
b = 1        # Kurve: y^2 = x^3 + a*x + b  (mod p)

# Liste der Rechnungen, die das Skript ausführen soll, anpassen für jede Aufgabe:
# Beispiel-Aufgabe 6:
queries = [
    ((5,5),(7,8)),   # a)
    ((2,4),(2,7)),   # b)
    ((2,4),(3,5)),   # c)
]

SHOW_STEPS = True   # True -> zeigt m, Zähler, Nenner, modulare Inverse etc.

# ---------------------------
# === Hilfsfunktionen
# ---------------------------
def mod_inv(x: int, p: int) -> Optional[int]:
    """Modulare Inverse von x mod p. None falls nicht invertierbar."""
    x %= p
    if x == 0:
        return None
    # p prim -> Fermat
    return pow(x, p-2, p)

def is_on_curve(P: Point, a: int, b: int, p: int) -> bool:
    """Prüft, ob P auf der Kurve liegt. None (O) ist immer auf der Kurve."""
    if P is None:
        return True
    x,y = P
    return (y*y - (x*x*x + a*x + b)) % p == 0

def inverse_point(P: Point, p: int) -> Point:
    if P is None:
        return None
    x,y = P
    return (x, (-y) % p)

def fmt(P: Point) -> str:
    return "O" if P is None else f"({P[0]},{P[1]})"

# ---------------------------
# === Punktaddition
# ---------------------------
def point_add(P: Point, Q: Point, a: int, p: int, show_steps: bool=False) -> Point:
    """Addiert P + Q auf E: y^2 = x^3 + a x + b über GF(p)."""
    if P is None:
        if show_steps: print("P = O -> Ergebnis = Q")
        return Q
    if Q is None:
        if show_steps: print("Q = O -> Ergebnis = P")
        return P

    x1,y1 = P
    x2,y2 = Q

    # P + (-P) = O
    if x1 == x2 and (y1 + y2) % p == 0:
        if show_steps: print(f"P + (-P) erkannt: ({x1},{y1}) + ({x2},{y2}) = O")
        return None

    # Steigung m bestimmen
    if P == Q:
        denom = (2*y1) % p
        inv = mod_inv(denom, p)
        if show_steps:
            print(f"Verdopplung: x1={x1}, y1={y1}")
            print(f"Zähler = 3*x1^2 + a = {3*x1*x1 + a}")
            print(f"Nenner = 2*y1 mod p = {denom}")
            print(f"inv(Nenner) mod {p} = {inv}")
        if inv is None:
            if show_steps: print("Nenner nicht invertierbar -> Ergebnis = O")
            return None
        num = (3 * x1 * x1 + a) % p
        m = (num * inv) % p
    else:
        denom = (x2 - x1) % p
        inv = mod_inv(denom, p)
        if show_steps:
            print(f"P != Q: x1={x1}, y1={y1}, x2={x2}, y2={y2}")
            print(f"Zähler = y2 - y1 = {(y2 - y1)}")
            print(f"Nenner = x2 - x1 mod p = {denom}")
            print(f"inv(Nenner) mod {p} = {inv}")
        if inv is None:
            if show_steps: print("Nenner nicht invertierbar -> Ergebnis = O")
            return None
        num = (y2 - y1) % p
        m = (num * inv) % p

    # Koordinaten des Ergebnisses
    x3 = (m*m - x1 - x2) % p
    y3 = (m*(x1 - x3) - y1) % p

    if show_steps:
        print(f"m = {m} (mod {p})")
        print(f"x3 = m^2 - x1 - x2 = {x3} (mod {p})")
        print(f"y3 = m*(x1 - x3) - y1 = {y3} (mod {p})")
        print(f"Ergebnispunkt: ({x3},{y3})\n")

    return (x3, y3)

# ---------------------------
# === Hauptprogramm
# ---------------------------
if __name__ == "__main__":
    # 1) Kurve prüfen (Diskriminante)
    disc = (4 * a*a*a + 27 * (b*b)) % p
    print(f"Kurve: y^2 = x^3 + {a}x + {b}  über GF({p})")
    print(f"Diskriminante mod {p} = {disc}  (soll ≠ 0 mod p für nonsingular)\n")

    # 2) Prüfe alle Punkte (optional schnell)
    pts = []
    for x in range(p):
        rhs = (x**3 + a*x + b) % p
        for y in range(p):
            if (y*y) % p == rhs:
                pts.append((x,y))
    print("Gefundene endliche Punkte (x,y):")
    print(sorted(pts))
    print(f"Anzahl (ohne O): {len(pts)}\n")

    # 3) Bearbeite die Queries
    for i,(A,B) in enumerate(queries, start=1):
        print(f"Query {i}: {fmt(A)} + {fmt(B)}")
        # Prüfen, ob Punkte gültig sind:
        okA = is_on_curve(A,a,b,p)
        okB = is_on_curve(B,a,b,p)
        if not okA:
            print(f"  Achtung: {fmt(A)} liegt NICHT auf der Kurve!")
        if not okB:
            print(f"  Achtung: {fmt(B)} liegt NICHT auf der Kurve!")
        # Addition durchführen
        res = point_add(A, B, a, p, show_steps=SHOW_STEPS)
        print(f"  -> Ergebnis: {fmt(res)}\n")

    print("Fertig.")
