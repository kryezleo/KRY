#!/usr/bin/env python3
"""
Universelles Skript: Ordnung von g (mod p) in Z_p* (p prim).

Ausgabe ist "wie im Bild":
- p und p-1 faktorisieren
- Teiler von p-1 auflisten
- dann den Lösungsweg drucken und die Ordnung bestimmen

Zwei Wege:
1) "reduction" (empfohlen, schnell): nutzt Faktorisierung von p-1 und reduziert die Kandidatenordnung.
2) "scan_divisors" (wie im Bild): prüft Teiler aufsteigend und zeigt g^d mod p.
"""

from math import isqrt
from functools import reduce
from operator import mul


def factorint(n: int) -> dict[int, int]:
    """Einfache Primfaktorzerlegung per Trial Division: n = ∏ p^e."""
    if n <= 1:
        return {}
    f: dict[int, int] = {}
    # Faktor 2
    while n % 2 == 0:
        f[2] = f.get(2, 0) + 1
        n //= 2
    # ungerade Faktoren
    d = 3
    while d * d <= n:
        while n % d == 0:
            f[d] = f.get(d, 0) + 1
            n //= d
        d += 2
    if n > 1:
        f[n] = f.get(n, 0) + 1
    return f


def format_factorization(f: dict[int, int]) -> str:
    if not f:
        return "1"
    parts = []
    for p in sorted(f):
        e = f[p]
        parts.append(f"{p}^{e}" if e > 1 else f"{p}")
    return " · ".join(parts)


def divisors_from_factorization(f: dict[int, int]) -> list[int]:
    """Alle positiven Teiler aus Primfaktorzerlegung erzeugen."""
    divs = [1]
    for p, e in f.items():
        divs = [d * (p ** k) for d in divs for k in range(e + 1)]
    return sorted(divs)


def order_mod_prime(g: int, p: int, method: str = "reduction", verbose: bool = True) -> int:
    """
    Bestimmt ord_p(g) in Z_p* (p prim).
    - method="reduction": reduziert n=p-1 mit Faktorisierung (sehr effizient)
    - method="scan_divisors": prüft alle Teiler d von p-1 aufsteigend (wie im Bild)
    """
    g %= p
    if g == 0:
        raise ValueError("g ≡ 0 (mod p) liegt nicht in Z_p*.")

    # Optional: Prim-Check (sehr simpel). Für Aufgaben reicht meist Vertrauen in Angabe.
    # Wenn du willst, kannst du hier einen robusteren Primtest ergänzen.

    n = p - 1
    fac = factorint(n)
    divs = divisors_from_factorization(fac)

    if verbose:
        print(f"p = {p}")
        print(f"p - 1 = {n} = {format_factorization(fac)}")
        print(f"Teiler von {n}: {divs}")
        print()
        print(f"g = {g} (mod {p})")
        print("-" * 60)

    if method == "scan_divisors":
        # "wie im Bild": teste d in aufsteigender Reihenfolge bis pow(g,d,p)==1
        for d in divs:
            val = pow(g, d, p)
            if verbose:
                print(f"g^{d} ≡ {val} (mod {p})")
            if val == 1:
                if verbose:
                    print("-" * 60)
                    print(f"=> kleinster Teiler d mit g^d ≡ 1 ist d = {d}")
                    print(f"=> ord_p(g) = {d}")
                return d
        # Sollte nie passieren in Z_p* (weil d=n funktioniert immer)
        raise RuntimeError("Kein Teiler d gefunden (unerwartet).")

    elif method == "reduction":
        # Effizienter Lösungsweg: ord | (p-1). Wir reduzieren n, indem wir testen n/q.
        ord_candidate = n
        for q in sorted(fac):  # über Primfaktoren von p-1
            while ord_candidate % q == 0:
                test = ord_candidate // q
                val = pow(g, test, p)
                if verbose:
                    print(f"Teste: teilt q={q} die Ordnung? Prüfe g^{test} (weil {ord_candidate}/{q})")
                    print(f"  g^{test} ≡ {val} (mod {p})")
                if val == 1:
                    if verbose:
                        print(f"  -> Ja, also Ordnung | {test}. Reduziere Kandidat: {ord_candidate} -> {test}")
                        print()
                    ord_candidate = test
                else:
                    if verbose:
                        print(f"  -> Nein, Ordnung bleibt (vorerst) {ord_candidate}")
                        print()
                    break

        if verbose:
            print("-" * 60)
            print(f"=> ord_p(g) = {ord_candidate}")
        return ord_candidate

    else:
        raise ValueError("method muss 'reduction' oder 'scan_divisors' sein.")


if __name__ == "__main__":
    # === Beispiel wie im Bild === g= 51(mod p),p=71
    p = 71
    g = 51

    # Weg 1: wie im Bild (Teiler scannen)
    print("\n=== Methode: scan_divisors (wie im Bild) ===\n")
    order_mod_prime(g, p, method="scan_divisors", verbose=True)

    # Weg 2: schneller Reduktionsweg (auch mit gedrucktem Lösungsweg)
    print("\n\n=== Methode: reduction (schneller) ===\n")
    order_mod_prime(g, p, method="reduction", verbose=True)

    # === Eigene Werte ===
    # p = int(input("p (prim) = "))
    # g = int(input("g = "))
    # order_mod_prime(g, p, method="reduction", verbose=True)
