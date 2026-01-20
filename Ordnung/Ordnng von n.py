#!/usr/bin/env python3
"""
Universelles Skript für Aufgaben mit Z_n^* (multiplikative Gruppe modulo n)

Kann u.a.:
(a) |Z_n^*| bestimmen  (das ist Euler-φ(n))
(b) (optional) Ordnung eines Elements a in Z_n^* bestimmen (falls gcd(a,n)=1)
(c) (optional) für eine Menge A = {a1,a2,...} alle Ordnungen ausgeben

Ausgabe ist als "Lösungsweg" gedruckt (ähnlich wie im Bild):
- n faktorisieren
- φ(n) mit Formel berechnen
- Teiler von φ(n) listen
- (optional) a^d mod n prüfen / reduzieren und Ordnung finden
"""

from math import gcd, isqrt
from typing import Dict, List


# ----------------------------
# Basis: Faktorisierung / Teiler
# ----------------------------
def factorint(n: int) -> Dict[int, int]:
    """Primfaktorzerlegung per Trial Division: n = ∏ p^e."""
    if n < 0:
        n = -n
    if n <= 1:
        return {}
    f: Dict[int, int] = {}
    while n % 2 == 0:
        f[2] = f.get(2, 0) + 1
        n //= 2
    d = 3
    while d * d <= n:
        while n % d == 0:
            f[d] = f.get(d, 0) + 1
            n //= d
        d += 2
    if n > 1:
        f[n] = f.get(n, 0) + 1
    return f


def format_factorization(f: Dict[int, int]) -> str:
    if not f:
        return "1"
    parts = []
    for p in sorted(f):
        e = f[p]
        parts.append(f"{p}^{e}" if e > 1 else f"{p}")
    return " · ".join(parts)


def divisors_from_factorization(f: Dict[int, int]) -> List[int]:
    """Alle positiven Teiler aus einer Primfaktorzerlegung erzeugen."""
    divs = [1]
    for p, e in f.items():
        divs = [d * (p ** k) for d in divs for k in range(e + 1)]
    return sorted(divs)


# ----------------------------
# Euler-phi und Ordnung in Z_n^*
# ----------------------------
def euler_phi(n: int) -> int:
    """Euler's Totient φ(n)."""
    if n == 0:
        return 0
    f = factorint(n)
    result = n
    for p in f:
        result = result // p * (p - 1)
    return result


def phi_with_steps(n: int, verbose: bool = True) -> int:
    """φ(n) + gedruckter Rechenweg."""
    f = factorint(n)
    phi = n
    if verbose:
        print(f"n = {n}")
        print(f"Faktorisierung: {n} = {format_factorization(f)}")
        print()
        print("Euler-φ-Formel:  φ(n) = n · Π(1 - (1/p)) über alle Primfaktoren p von n")
        print("Schrittweise:")

    for p in sorted(f):
        old = phi
        phi = phi // p * (p - 1)
        if verbose:
            print(f"  p = {p}:  {old} · (1 - (1/{p})) = {old} · ({p-1}/{p}) = {phi}")

    if verbose:
        print()
        print(f"=> φ({n}) = {phi}")
        print(f"=> |Z_{n}^*| = φ({n}) = {phi}")
    return phi


def multiplicative_order(a: int, n: int, method: str = "reduction", verbose: bool = True) -> int:
    """
    Ordnung von a modulo n in Z_n^*.
    Voraussetzung: gcd(a,n)=1.

    method:
      - "scan_divisors": prüft alle Teiler d von φ(n) aufsteigend (wie im Bild)
      - "reduction": reduziert Kandidatenordnung über Primfaktoren von φ(n) (schneller)
    """
    a %= n
    if gcd(a, n) != 1:
        raise ValueError(f"a={a} ist nicht in Z_{n}^* (gcd(a,n) != 1).")

    phi_n = euler_phi(n)
    phi_fac = factorint(phi_n)
    divs = divisors_from_factorization(phi_fac)

    if verbose:
        print(f"a = {a} (mod {n}), gcd(a,n)=1 => a ∈ Z_{n}^*")
        print(f"φ({n}) = {phi_n} = {format_factorization(phi_fac)}")
        print(f"Teiler von φ({n}): {divs}")
        print("-" * 60)

    if method == "scan_divisors":
        for d in divs:
            val = pow(a, d, n)
            if verbose:
                print(f"a^{d} ≡ {val} (mod {n})")
            if val == 1:
                if verbose:
                    print("-" * 60)
                    print(f"=> kleinster Teiler d mit a^d ≡ 1 ist d = {d}")
                    print(f"=> ord_n(a) = {d}")
                return d
        raise RuntimeError("Kein Teiler gefunden (unerwartet).")

    if method == "reduction":
        ord_candidate = phi_n
        for q in sorted(phi_fac):
            while ord_candidate % q == 0:
                test = ord_candidate // q
                val = pow(a, test, n)
                if verbose:
                    print(f"Teste Reduktion mit q={q}: prüfe a^{test} (weil {ord_candidate}/{q})")
                    print(f"  a^{test} ≡ {val} (mod {n})")
                if val == 1:
                    if verbose:
                        print(f"  -> Ja, reduziere: {ord_candidate} -> {test}\n")
                    ord_candidate = test
                else:
                    if verbose:
                        print(f"  -> Nein, bleibt: {ord_candidate}\n")
                    break

        if verbose:
            print("-" * 60)
            print(f"=> ord_n(a) = {ord_candidate}")
        return ord_candidate

    raise ValueError("method muss 'reduction' oder 'scan_divisors' sein.")


# ----------------------------
# "Aufgabenmodus": genau wie eure Angabe
# ----------------------------
def solve_task(n: int, A: List[int] | None = None, also_orders: bool = True, method: str = "reduction") -> None:
    """
    Druckt den Lösungsweg:
    (a) |Z_n^*| = φ(n)
    (optional) Ordnungen für a in A, falls also_orders=True
    """
    print("\n=== (a) Ordnung von Z_n^* (Gruppenordnung) ===\n")
    phi_n = phi_with_steps(n, verbose=True)

    if A is None:
        return

    if also_orders:
        print("\n=== (optional) Ordnung der Elemente aus A in Z_n^* ===\n")
        for a in A:
            print(f"\n--- a = {a} ---")
            d = gcd(a, n)
            print(f"gcd({a},{n}) = {d}")
            if d != 1:
                print(f"=> {a} ∉ Z_{n}^* (nicht invertierbar mod {n}) -> keine Ordnung in Z_n^*")
                continue
            multiplicative_order(a, n, method=method, verbose=True)


if __name__ == "__main__":
    # Beispiel passend zu deinem Bild:
    n = 4123
    A = [15, 21, 1024]

    # Wenn du NUR Teil (a) willst: also_orders=False setzen.
    solve_task(n, A=A, also_orders=False)

    # Wenn du zusätzlich die Elementordnungen für A willst:
    # solve_task(n, A=A, also_orders=True, method="reduction")

    # Interaktiv (optional):
    # n = int(input("n = "))
    # raw = input("A (z.B. 15,21,86 oder leer) = ").strip()
    # A = [int(x) for x in raw.split(",")] if raw else None
    # solve_task(n, A=A, also_orders=True, method="reduction")
