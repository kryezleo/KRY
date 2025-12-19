#!/usr/bin/env python3
"""
Elliptische Kurve über GF(p) - universelles Skript.

Das Skript:
 - findet alle Punkte (x,y) mit 0 <= x,y < p für y^2 = x^3 + a*x + b (mod p)
 - wählt automatisch Beispielpunkte (erste 2 gefundene Punkte)
 - berechnet: P+Q, P+P (Verdopplung), P + (-P) (soll O ergeben)
 - optional: alle paarweisen Additionen ausgeben (aktivierbar)
"""

from typing import List, Tuple, Optional

# === Parameter (anpassen für jede Aufgabe) ===
p = 43   # Primzahl für GF(p)
a = 22
b = 17  # Kurve: y^2 = x^3 + a*x + b  (mod p)

# === Hilfsfunktionen ===
Point = Optional[Tuple[int,int]]  # None repräsentiert den Punkt im Unendlichen O

def mod_inv(x: int, p: int) -> Optional[int]:
    """Modulare Inverse von x mod p (gibt None zurück, wenn nicht invertierbar)."""
    x = x % p
    if x == 0:
        return None
    # p sollte prim sein -> Fermat's little theorem
    return pow(x, p-2, p)

def quadratic_residues(value: int, p: int) -> List[int]:
    """Alle y in 0..p-1 mit y^2 ≡ value (mod p)."""
    value %= p
    return [y for y in range(p) if (y*y) % p == value]

def find_points(a: int, b: int, p: int) -> List[Point]:
    """Finde alle Punkte (x,y) auf der Kurve plus None für O nicht hier (wird separat behandelt)."""
    pts = []
    for x in range(p):
        rhs = (x**3 + a*x + b) % p
        ys = quadratic_residues(rhs, p)
        for y in ys:
            pts.append((x,y))
    return pts

def point_add(P: Point, Q: Point, a: int, p: int) -> Point:
    """Addiere P + Q in E: returns None für O."""
    if P is None:
        return Q
    if Q is None:
        return P

    x1, y1 = P
    x2, y2 = Q

    # P + (-P) = O
    if x1 == x2 and (y1 + y2) % p == 0:
        return None

    if P == Q:
        denom = (2 * y1) % p
        inv = mod_inv(denom, p)
        if inv is None:
            return None  # Tangentensteigung nicht definierbar -> O
        m = ((3 * x1 * x1 + a) * inv) % p
    else:
        denom = (x2 - x1) % p
        inv = mod_inv(denom, p)
        if inv is None:
            return None
        m = ((y2 - y1) * inv) % p

    x3 = (m*m - x1 - x2) % p
    y3 = (m*(x1 - x3) - y1) % p
    return (x3, y3)

def inverse_point(P: Point, p: int) -> Point:
    """Inverse -P (mod p)."""
    if P is None:
        return None
    x,y = P
    return (x, (-y) % p)

def fmt(P: Point) -> str:
    return "O" if P is None else f"({P[0]},{P[1]})"

# === Hauptprogramm ===
if __name__ == "__main__":
    # 1) Punkte finden
    points = find_points(a, b, p)
    points_sorted = sorted(points)
    print("Gefundene Punkte (ohne O):")
    print(points_sorted)
    print("Anzahl Punkte (ohne O):", len(points_sorted))
    print("Punkt im Unendlichen: O\n")

    # 2) Automatische Auswahl von Beispielen
    if len(points_sorted) == 0:
        print("Keine endlichen Punkte gefunden (nur O).")
    elif len(points_sorted) == 1:
        P = points_sorted[0]
        print("Nur ein Punkt vorhanden:", fmt(P))
        print("Doppelt rechnen: P+P =", fmt(point_add(P,P,a,p)))
    else:
        P = points_sorted[0]
        Q = points_sorted[1]
        print("Automatisch gewählte Beispielpunkte:")
        print("P =", fmt(P))
        print("Q =", fmt(Q))
        print()
        # Rechnungen
        print("P + Q =", fmt(point_add(P, Q, a, p)))
        print("P + P =", fmt(point_add(P, P, a, p)))
        print("P + (-P) =", fmt(point_add(P, inverse_point(P, p), a, p)))  # sollte O sein

        # zusätzlich: wenn Q == -P dann Hinweis
        if Q == inverse_point(P, p):
            print("\nHinweis: Q ist die Inverse von P -> P+Q = O")

    # 3) Optional: alle paarweisen Additionen ausgeben (setze flag True/False)
    show_all_pairs = False
    if show_all_pairs and len(points_sorted) > 0:
        print("\nAlle paarweisen Additionen (endliche Punkte):")
        for i, A in enumerate(points_sorted):
            for j, B in enumerate(points_sorted[i:], start=i):
                print(f"{fmt(A)} + {fmt(B)} = {fmt(point_add(A,B,a,p))}")
