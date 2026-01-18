#!/usr/bin/env python3
"""
Quadratisches Sieb (didaktisch / universell für Übungsaufgaben)
- Rechnet die typischen Schritte wie in Aufgabenblättern durch
- Gibt Zwischenschritte aus: m, q(x), Faktorbase F, Sieben/Glattheit, Matrix (mod 2),
  lineares Gleichungssystem lösen, Abhängigkeit -> gcd -> Faktor

Hinweis:
- Das ist ein "Lern-/Übungsskript", nicht die performante QS-Implementierung für große n.
- Für Aufgaben wie n=91 etc. funktioniert es sehr gut.
"""

import math
from dataclasses import dataclass
from typing import List, Tuple, Dict, Optional

# -----------------------------
# Hilfsfunktionen
# -----------------------------

def is_square(a: int) -> bool:
    if a < 0:
        return False
    r = int(math.isqrt(a))
    return r * r == a

def legendre_symbol(a: int, p: int) -> int:
    """Legendre-Symbol (a|p) für ungerades Prim p. Rückgabe: 0, 1 oder -1."""
    a %= p
    if a == 0:
        return 0
    # pow(a, (p-1)//2, p) ist 1 oder p-1
    ls = pow(a, (p - 1) // 2, p)
    return -1 if ls == p - 1 else ls

def primes_up_to(B: int) -> List[int]:
    """Einfache Sieb-Primliste bis B."""
    if B < 2:
        return []
    sieve = bytearray(b"\x01") * (B + 1)
    sieve[0:2] = b"\x00\x00"
    for i in range(2, int(B**0.5) + 1):
        if sieve[i]:
            step = i
            start = i * i
            sieve[start:B+1:step] = b"\x00" * (((B - start) // step) + 1)
    return [i for i in range(2, B + 1) if sieve[i]]

def fmt_factorization(exps: Dict[int, int], sign: int) -> str:
    parts = []
    if sign < 0:
        parts.append("-1")
    for p in sorted(exps):
        e = exps[p]
        if e == 1:
            parts.append(str(p))
        else:
            parts.append(f"{p}^{e}")
    return " · ".join(parts) if parts else "1"

def gcd(a: int, b: int) -> int:
    while b:
        a, b = b, a % b
    return abs(a)

# -----------------------------
# QS Datenstrukturen
# -----------------------------

@dataclass
class SmoothRelation:
    x: int                 # der x-Wert
    a: int                 # a = m+x
    q: int                 # q(x) = (m+x)^2 - n
    sign: int              # Vorzeichen von q
    exps: Dict[int, int]   # Primexponenten (ohne -1), nur aus Faktorbase

# -----------------------------
# Quadratisches Sieb (didaktisch)
# -----------------------------

def build_factor_base(n: int, B: int) -> List[int]:
    """
    Faktorbase:
    - enthält die Primzahlen p <= B, für die n quadratischer Rest mod p ist,
      also (n|p)=1 (plus p=2, wenn sinnvoll)
    - -1 wird separat über sign behandelt
    """
    fb = []
    for p in primes_up_to(B):
        if p == 2:
            # Für 2 nehmen wir meist mit (ist in Übungsaufgaben oft enthalten)
            fb.append(2)
        else:
            if legendre_symbol(n, p) == 1:
                fb.append(p)
    return fb

def trial_factor_over_base(q: int, factor_base: List[int]) -> Tuple[int, Dict[int,int], int]:
    """
    Versucht |q| vollständig über factor_base zu faktorisieren.
    Rückgabe: (rest, exps, sign)
      - rest==1 => vollständig glatt (B-glatt)
      - exps: Primexponenten (nur aus FB)
      - sign: -1 wenn q<0 sonst +1
    """
    sign = -1 if q < 0 else 1
    v = abs(q)
    exps: Dict[int,int] = {}
    for p in factor_base:
        if p == 0:
            continue
        cnt = 0
        while v % p == 0:
            v //= p
            cnt += 1
        if cnt:
            exps[p] = cnt
        if v == 1:
            break
    return v, exps, sign

def collect_relations(n: int, B: int, x_min: int, x_max: int, verbose: bool=True) -> Tuple[int, List[int], List[SmoothRelation]]:
    """
    Schritt (a): q(x) berechnen und diejenigen q(x) finden, die B-glatt sind.
    """
    m = int(math.isqrt(n))
    fb = build_factor_base(n, B)

    if verbose:
        print("=== Eingaben ===")
        print(f"n = {n}")
        print(f"B = {B}")
        print(f"m = floor(sqrt(n)) = {m}")
        print()
        print("=== Faktorbase F (ohne -1; Vorzeichen wird separat behandelt) ===")
        print(f"F = {fb}")
        print()

    relations: List[SmoothRelation] = []
    if verbose:
        print("=== q(x) Tabelle & Glattheit ===")
        print("x | a=m+x | q(x)=(m+x)^2-n | Faktorisierung über F | glatt?")
        print("-"*88)

    for x in range(x_min, x_max + 1):
        a = m + x
        q = a*a - n
        rest, exps, sign = trial_factor_over_base(q, fb)
        smooth = (rest == 1)

        if verbose:
            fac_str = fmt_factorization(exps, sign)
            print(f"{x:>2} | {a:>6} | {q:>16} | {fac_str:<28} | {'JA' if smooth else 'NEIN'}")

        if smooth:
            relations.append(SmoothRelation(x=x, a=a, q=q, sign=sign, exps=exps))

    if verbose:
        print()
        print(f"Gefundene B-glatte q(x): {len(relations)} Stück")
        for r in relations:
            print(f"  x={r.x:>2}, a={r.a}, q={r.q},  q-Faktoren: {fmt_factorization(r.exps, r.sign)}")
        print()

    return m, fb, relations

def build_matrix_mod2(relations: List[SmoothRelation], factor_base: List[int], verbose: bool=True):
    """
    Schritt (b): Matrix mod 2 aufstellen:
    - Spalten: [-1] + factor_base
    - Zeilen: Relation i, Einträge = Exponent mod 2
    """
    cols = [-1] + factor_base
    col_index = {p:i for i,p in enumerate(cols)}
    matrix = []

    for r in relations:
        row = [0]*len(cols)
        # -1-Spalte
        if r.sign < 0:
            row[col_index[-1]] = 1
        # Primspalten
        for p, e in r.exps.items():
            row[col_index[p]] = e % 2
        matrix.append(row)

    if verbose:
        print("=== Lineares Gleichungssystem mod 2 ===")
        print("Spalten (in dieser Reihenfolge):")
        print("  ", cols)
        print("Zeilen = Relationen (x, q(x)) mit Exponenten mod 2:")
        for i, r in enumerate(relations):
            print(f"  R{i}: x={r.x:>2}, q={r.q:>6}  ->  {matrix[i]}")
        print()

    return cols, matrix

def gaussian_elim_find_dependency(matrix: List[List[int]], verbose: bool=True) -> Optional[List[int]]:
    """
    Findet eine nichttriviale Abhängigkeit der Zeilen (Nullspace der transponierten Sicht):
    Wir suchen einen Vektor c (über GF(2)), so dass XOR-Summe der ausgewählten Zeilen = 0.

    Implementiert per Gauß-Elimination über GF(2) mit "Augment" = Identität,
    dann ist jede "freie Variable" eine Abhängigkeit. Für Übungsgrößen reicht das.

    Rückgabe: Auswahlvektor sel (0/1) der Zeilen, oder None.
    """
    if not matrix:
        return None
    m = len(matrix)        # Zeilen
    n = len(matrix[0])     # Spalten

    # Kopie + augment identity
    A = [row[:] for row in matrix]
    aug = [[1 if i==j else 0 for j in range(m)] for i in range(m)]

    pivot_col_for_row = [-1]*m
    row = 0
    for col in range(n):
        # Pivot suchen
        pivot = None
        for r in range(row, m):
            if A[r][col] == 1:
                pivot = r
                break
        if pivot is None:
            continue
        # tauschen
        A[row], A[pivot] = A[pivot], A[row]
        aug[row], aug[pivot] = aug[pivot], aug[row]
        pivot_col_for_row[row] = col

        # eliminieren
        for r in range(m):
            if r != row and A[r][col] == 1:
                # r = r XOR row
                A[r] = [A[r][c] ^ A[row][c] for c in range(n)]
                aug[r] = [aug[r][c] ^ aug[row][c] for c in range(m)]

        row += 1
        if row == m:
            break

    # Eine Abhängigkeit existiert, wenn es eine Zeile gibt mit A[r]=0,
    # dann liefert aug[r] eine Linearkombination der Originalzeilen, die 0 ergibt.
    for r in range(m):
        if all(v == 0 for v in A[r]):
            dep = aug[r][:]
            if any(dep):  # nicht-trivial
                if verbose:
                    print("=== Gefundene Abhängigkeit (Zeilenkombination) ===")
                    print("Auswahlvektor über Relationen (1 = Relation benutzen):")
                    print("  ", dep)
                    idxs = [i for i,b in enumerate(dep) if b==1]
                    print("Benutzte Relationen:", idxs)
                    print()
                return dep

    if verbose:
        print("Keine Abhängigkeit gefunden (zu wenige Relationen). Range erweitern oder B erhöhen.")
        print()
    return None

def combine_and_factor(n: int, m_sqrt: int, factor_base: List[int], relations: List[SmoothRelation], dep: List[int], verbose: bool=True) -> Optional[int]:
    """
    Schritt (c): Abhängigkeit nutzen:
    - A = Produkt(a_i) mod n
    - Q = Produkt(q_i) ist ein Quadrat (bzgl. Exponenten mod 2)
    - B = sqrt(Q) mod n (über Exponenten/2)
    - gcd(A-B, n) liefert hoffentlich Faktor
    """
    chosen = [relations[i] for i,b in enumerate(dep) if b==1]
    if not chosen:
        return None

    # A = product(a) mod n
    A = 1
    for r in chosen:
        A = (A * (r.a % n)) % n

    # Exponenten aufsummieren (inkl. -1 über sign)
    sign_exp = 0
    total: Dict[int,int] = {p:0 for p in factor_base}
    for r in chosen:
        if r.sign < 0:
            sign_exp += 1
        for p,e in r.exps.items():
            total[p] += e

    # Da es eine Abhängigkeit ist, sind alle total[p] gerade und sign_exp gerade.
    # B = product(p^(total[p]/2)) mod n, und (-1)^(sign_exp/2) = 1 mod n, also ignorierbar.
    B = 1
    for p,e in total.items():
        half = e // 2
        if half:
            B = (B * pow(p, half, n)) % n

    if verbose:
        print("=== Kombination & gcd ===")
        print("Gewählte Relationen:")
        for r in chosen:
            print(f"  x={r.x:>2}, a={r.a:>3}, q={r.q:>4}, q-Faktoren: {fmt_factorization(r.exps, r.sign)}")

        print()
        print(f"A = Π(a) mod n = {A}")
        print(f"B = sqrt(Π(q)) mod n = {B}")
        diff = (A - B) % n
        print(f"A - B (mod n) = {diff}")
        print()

    g1 = gcd(A - B, n)
    g2 = gcd(A + B, n)

    if verbose:
        print(f"gcd(A - B, n) = {g1}")
        print(f"gcd(A + B, n) = {g2}")
        print()

    # Nichttrivialen Faktor zurückgeben
    for g in (g1, g2):
        if 1 < g < n:
            return g
    return None

def quadratic_sieve_educational(n: int, B: int, x_min: int, x_max: int, verbose: bool=True) -> None:
    """
    Komplettdurchlauf: (a) glatte q(x) finden, (b) Matrix, (c) Faktor berechnen.
    """
    m_sqrt, fb, relations = collect_relations(n, B, x_min, x_max, verbose=verbose)

    # Für ein Gleichungssystem brauchen wir mindestens #Spalten+1 Relationen (grob).
    needed = len(fb) + 1  # +1 für -1-Spalte
    if verbose:
        print(f"Faustregel: Benötige ungefähr >= {needed+1} glatte Relationen für sichere Abhängigkeit.")
        print()

    cols, mat = build_matrix_mod2(relations, fb, verbose=verbose)
    dep = gaussian_elim_find_dependency(mat, verbose=verbose)
    if dep is None:
        print("➡️ Tipp: Range für x vergrößern (z.B. -20..20) oder B erhöhen.")
        return

    factor = combine_and_factor(n, m_sqrt, fb, relations, dep, verbose=verbose)
    if factor is None:
        print("Keine nichttriviale Zerlegung gefunden mit dieser Abhängigkeit.")
        print("➡️ Tipp: Mehr Relationen sammeln und/oder andere Abhängigkeit suchen (Range/B erhöhen).")
        return

    other = n // factor
    print("=== Ergebnis ===")
    print(f"n = {n} = {factor} · {other}")

# -----------------------------
# CLI / Konsole
# -----------------------------

def main():
    print("Quadratisches Sieb – Übungsmodus (mit Zwischenschritten)")
    print("------------------------------------------------------")
    try:
        n = int(input("n eingeben (zusammengesetzt, ungerade empfohlen): ").strip())
        B = int(input("B eingeben (z.B. 5, 7, 11, ...): ").strip())
        x_min = int(input("x_min eingeben (z.B. -4): ").strip())
        x_max = int(input("x_max eingeben (z.B. 4): ").strip())
    except ValueError:
        print("❌ Bitte gültige ganze Zahlen eingeben.")
        return

    if n <= 1:
        print("❌ n muss > 1 sein.")
        return
    if x_min > x_max:
        print("❌ x_min muss <= x_max sein.")
        return

    quadratic_sieve_educational(n, B, x_min, x_max, verbose=True)

if __name__ == "__main__":
    main()
