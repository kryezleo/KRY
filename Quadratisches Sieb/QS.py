#!/usr/bin/env python3
"""
Simple quadratic sieve implementation in pure Python.

Educational version:
- No external libraries
- Works for mittelgroße n (z.B. bis ein paar Millionen / Milliarden),
  nicht für echte RSA-Größen :)
"""

import math
from itertools import count


# ---------- Hilfsfunktionen ----------

def primes_up_to(limit: int):
    """Sieve of Eratosthenes: list of primes <= limit."""
    if limit < 2:
        return []
    sieve = [True] * (limit + 1)
    sieve[0] = sieve[1] = False
    for p in range(2, int(limit ** 0.5) + 1):
        if sieve[p]:
            step = p
            start = p * p
            sieve[start:limit + 1:step] = [False] * len(range(start, limit + 1, step))
    return [p for p, is_p in enumerate(sieve) if is_p]


def is_quadratic_residue(n: int, p: int) -> bool:
    """Check if n is a quadratic residue mod p (Legendre symbol == 1)."""
    return pow(n, (p - 1) // 2, p) == 1


def trial_factor_with_base(m: int, factor_base):
    """
    Try to factor integer m completely over the given factor base.
    Returns (sign, exponents, remaining).
      sign: +1 or -1 (from factor -1)
      exponents: list of exponents for primes in factor_base (without -1)
      remaining: leftover factor (>1 if not smooth)
    """
    sign = 1
    if m < 0:
        sign = -1
        m = -m

    exponents = [0] * len(factor_base)

    for i, p in enumerate(factor_base):
        if p == -1:
            # -1 ist nur im sign enthalten
            continue
        while m % p == 0:
            m //= p
            exponents[i] += 1

    return sign, exponents, m


# ---------- Lineare Algebra mod 2 ----------

def find_dependencies_mod2(matrix):
    """
    Find linear dependencies between rows of a 0/1-matrix over GF(2).
    matrix: list of lists (rows)
    Returns a list of bitmasks; each mask describes a nontrivial combination
    of rows that sums to the zero vector.
    """
    if not matrix:
        return []

    n_rows = len(matrix)
    n_cols = len(matrix[0])

    # represent each row as bit-int over columns
    row_bits = []
    for row in matrix:
        bits = 0
        for c, val in enumerate(row):
            if val & 1:
                bits |= (1 << c)
        row_bits.append(bits)

    # combination bits: which original rows make up this current row
    comb_bits = [1 << r for r in range(n_rows)]

    dependencies = []

    # Gaussian elimination over GF(2)
    for col in range(n_cols):
        # find pivot row with bit set in this col
        pivot = None
        for r in range(n_rows):
            if (row_bits[r] >> col) & 1:
                pivot = r
                break
        if pivot is None:
            continue

        # use pivot to eliminate this column from other rows
        for r in range(n_rows):
            if r != pivot and ((row_bits[r] >> col) & 1):
                row_bits[r] ^= row_bits[pivot]
                comb_bits[r] ^= comb_bits[pivot]

    # Any row that is now zero gives a dependency
    for r in range(n_rows):
        if row_bits[r] == 0 and comb_bits[r] != 0:
            dependencies.append(comb_bits[r])

    return dependencies


# ---------- Quadratisches Sieb ----------

def quadratic_sieve(n: int, B: int = 50, max_relations: int | None = None):
    """
    Factor n using a simple quadratic sieve.
    B    = smoothness bound (creates factor base of primes <= B)
    max_relations = optional upper bound for collected relations
    Returns a nontrivial factor of n, or None if it fails.
    """

    if n % 2 == 0:
        return 2

    # 1) Factor base bauen: -1 plus alle kleinen p mit (n|p)=1
    primes = primes_up_to(B)
    factor_base = [-1]
    for p in primes:
        if is_quadratic_residue(n, p):
            factor_base.append(p)

    # number of primes (without -1 for exponents)
    fb_primes = factor_base[1:]
    fb_size = len(fb_primes)

    # Wie viele Relationen brauchen wir? mindestens fb_size + 1
    if max_relations is None:
        max_relations = fb_size + 10

    relations = []      # list of dicts: {x, v, sign, exponents}
    exponent_rows = []  # exponents mod 2 (including -1)

    # 2) B-smooth Relationen sammeln: x^2 - n ist glatt
    x0 = math.isqrt(n) + 1
    for x in count(x0):
        v = x * x - n
        sign, exps, rem = trial_factor_with_base(v, factor_base)

        if rem == 1:  # komplett glatt
            # exponents incl -1 als erste Komponente (für die Matrix)
            row = [0] * (1 + fb_size)  # index 0 für -1, 1.. für primes
            if sign == -1:
                row[0] = 1
            for i, e in enumerate(exps[1:], start=1):
                row[i] = e % 2

            relations.append({
                "x": x,
                "v": v,
                "sign": sign,
                "exponents": exps,
                "row": row,
            })
            exponent_rows.append(row)

            if len(relations) >= max_relations:
                break

    if len(relations) <= fb_size:
        print("Not enough relations collected.")
        return None

    # 3) Lineare Abhängigkeiten im Exponentenraum mod 2 finden
    deps = find_dependencies_mod2(exponent_rows)
    if not deps:
        print("No dependencies found.")
        return None

    # 4) Jede gefundene Abhängigkeit liefert einen Kandidaten (X, Y)
    for mask in deps:
        X = 1
        V = 1
        used_indices = []
        for i, rel in enumerate(relations):
            if (mask >> i) & 1:
                used_indices.append(i)
                X = (X * rel["x"]) % n
                V *= rel["v"]

        # V sollte perfektes Quadrat sein:
        Y = math.isqrt(abs(V))
        if Y * Y != abs(V):
            # Something went wrong; skip this dependency
            continue

        # 5) gcd(|X - Y|, n) liefert einen Faktor (hoffentlich nicht trivial)
        for cand in (abs(X - Y), abs(X + Y)):
            g = math.gcd(cand, n)
            if 1 < g < n:
                return g

    return None


def factor_with_quadratic_sieve(n: int, B: int = 50):
    """Convenience wrapper: returns (p, q) with p*q = n, or None."""
    f = quadratic_sieve(n, B=B)
    if f is None:
        return None
    return f, n // f


if __name__ == "__main__":
    # kleines Beispiel
    n = 737
    factors = factor_with_quadratic_sieve(n, B=50)
    print(f"n = {n}, factors = {factors}")
