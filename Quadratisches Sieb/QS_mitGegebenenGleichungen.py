#!/usr/bin/env python3
import re
import math

def parse_equation(line: str):
    """
    Parses a line like:
      15^2 = (-1)*2^9 (mod n)
      27^2 = -1*2^3
      31^2 = 2^5*7

    Returns:
      x: int
      factors: dict[int, int]  (prime -> exponent), includes -1 if present
    """
    # remove "(mod ...)" tail if present
    line = re.sub(r"\(mod.*?\)", "", line, flags=re.IGNORECASE).strip()

    # split at '='
    if "=" not in line:
        raise ValueError("Kein '=' gefunden.")
    left, right = [p.strip() for p in line.split("=", 1)]

    # parse x from left side like "15^2" or "15²" (we accept optional spaces)
    m = re.match(r"^\s*(-?\d+)\s*(\^2|²)\s*$", left)
    if not m:
        m = re.match(r"^\s*(-?\d+)\s*\^\s*2\s*$", left)
    if not m:
        raise ValueError(f"Linke Seite nicht erkannt: '{left}' (erwarte z.B. 15^2)")
    x = int(m.group(1))

    # normalize right: remove spaces
    r = right.replace(" ", "")

    if r == "":
        raise ValueError("Rechte Seite ist leer.")
    parts = [p for p in r.split("*") if p]

    factors = {}  # p -> exponent
    for part in parts:
        if part == "(-1)":
            p = -1
            e = 1
        else:
            mm = re.match(r"^(-?\d+)(\^(-?\d+))?$", part)
            if not mm:
                raise ValueError(f"Token nicht erkannt: '{part}' (erwarte z.B. 2^9 oder 7 oder (-1))")
            p = int(mm.group(1))
            e = int(mm.group(3)) if mm.group(3) is not None else 1

        factors[p] = factors.get(p, 0) + e

    return x, factors

def build_factor_base(all_factors):
    primes = sorted({p for p in all_factors if p not in (-1, 0, 1, -0)})
    return [-1] + primes

def vec_from_factors(factor_base, factors_dict):
    return [int(factors_dict.get(p, 0)) for p in factor_base]

def parity_vec(vec):
    return [v & 1 for v in vec]

def solve_one_dependency_gf2(rows_bits, n_cols):
    """
    Returns a nontrivial dependency as row-mask (bitmask) or None.
    Standard Gaussian elimination over GF(2).
    """
    n_rows = len(rows_bits)
    row = rows_bits[:]
    comb = [(1 << i) for i in range(n_rows)]

    r = 0
    for col in range(n_cols):
        pivot = -1
        for i in range(r, n_rows):
            if (row[i] >> col) & 1:
                pivot = i
                break
        if pivot == -1:
            continue

        # swap
        row[r], row[pivot] = row[pivot], row[r]
        comb[r], comb[pivot] = comb[pivot], comb[r]

        # eliminate
        for i in range(n_rows):
            if i != r and ((row[i] >> col) & 1):
                row[i] ^= row[r]
                comb[i] ^= comb[r]

        r += 1
        if r == n_rows:
            break

    for i in range(n_rows):
        if row[i] == 0 and comb[i] != 0:
            return comb[i]
    return None

def fmt_base(base):
    return "[" + ", ".join(str(p) for p in base) + "]"

def format_rhs_product(factor_base, exps):
    """Pretty-print product like (-1) * 2^12 * 7^2 (exps are integers, can be 0)."""
    parts = []
    for p, e in zip(factor_base, exps):
        if e == 0:
            continue
        if p == -1:
            parts.append("(-1)" if e == 1 else f"(-1)^{e}")
        else:
            parts.append(str(p) if e == 1 else f"{p}^{e}")
    return " * ".join(parts) if parts else "1"

def main():
    print("=== QS: Gleichungen eingeben -> Faktor finden (mit Zwischenschritten) ===\n")
    n = int(input("n eingeben (z.B. 737): ").strip())

    print("\nGib jetzt deine Kongruenzen ein, eine pro Zeile.")
    print("Beispiele:")
    print("  15^2 = (-1)*2^9 (mod n)")
    print("  27^2 = (-1)*2^3")
    print("  31^2 = 2^5*7")
    print("Beende mit einer leeren Zeile.\n")

    eq_lines = []
    while True:
        line = input("> ").strip()
        if not line:
            break
        eq_lines.append(line)

    if len(eq_lines) < 2:
        print("\nZu wenige Gleichungen (mindestens 2 sinnvoll).")
        return

    # parse equations
    relations_raw = []
    all_factors_keys = set()
    for i, line in enumerate(eq_lines, start=1):
        x, factors = parse_equation(line)
        relations_raw.append({"x": x, "factors": factors, "line": line})
        all_factors_keys |= set(factors.keys())

    # build factor base automatically
    factor_base = build_factor_base(all_factors_keys)
    n_cols = len(factor_base)

    print("\n=== Eingelesene Gleichungen ===")
    for i, rel in enumerate(relations_raw, start=1):
        print(f"R{i}: {rel['line']}   (x={rel['x']}, RHS-Faktoren={rel['factors']})")

    print("\n=== Automatisch erkannte Faktorbase ===")
    print("Faktorbase =", fmt_base(factor_base))

    # build exponent vectors + parity matrix
    relations = []
    rows_bits = []
    for rel in relations_raw:
        exp_vec = vec_from_factors(factor_base, rel["factors"])
        par = parity_vec(exp_vec)

        bits = 0
        for j, v in enumerate(par):
            if v:
                bits |= (1 << j)

        relations.append({
            "x": rel["x"],
            "exp_vec": exp_vec,
            "par": par,
            "line": rel["line"],
        })
        rows_bits.append(bits)

    print("\n=== Exponenten & Parity (mod 2) pro Relation ===")
    for i, rel in enumerate(relations, start=1):
        print(f"R{i}: x={rel['x']}")
        print(f"    Exponenten: {dict(zip(factor_base, rel['exp_vec']))}")
        print(f"    Parity:     {dict(zip(factor_base, rel['par']))}")

    print("\n=== Parity-Matrix (Zeilen=Relationen, Spalten=Faktorbase) ===")
    header = "       " + "  ".join(f"{p:>4}" for p in factor_base)
    print(header)
    for i, rel in enumerate(relations, start=1):
        row_str = "  ".join(f"{v:>4}" for v in rel["par"])
        print(f"R{i:>2}:   {row_str}")

    dep = solve_one_dependency_gf2(rows_bits, n_cols)
    if dep is None:
        print("\nKeine lineare Abhängigkeit gefunden. (Mehr Gleichungen nötig.)")
        return

    used = [i for i in range(len(relations)) if (dep >> i) & 1]
    print("\n=== Gefundene lineare Abhängigkeit (mod 2) ===")
    print("Kombiniere:", ", ".join(f"R{idx+1}" for idx in used))

    # -----------------------------
    # NEW: Build "numbers inserted" strings for X and RHS
    # -----------------------------
    x_list = [relations[idx]["x"] for idx in used]
    X_formula = " · ".join(str(x) for x in x_list) if x_list else "1"

    # compute X and sum of exponents over Z
    X = 1
    sum_exps = [0] * n_cols
    for idx in used:
        X = (X * relations[idx]["x"]) % n
        for j in range(n_cols):
            sum_exps[j] += relations[idx]["exp_vec"][j]

    print("\nSumme der Exponenten (über Z):")
    print(dict(zip(factor_base, sum_exps)))

    # check evenness
    odd = [factor_base[j] for j, e in enumerate(sum_exps) if e % 2 != 0]
    if odd:
        print("\nWARNUNG: Diese Exponenten-Summen sind ungerade -> kein perfektes Quadrat:", odd)
        print("Dann passen die Gleichungen nicht zu einer gültigen Dependency (oder Parsing/Inputs).")
        return

    half = [e // 2 for e in sum_exps]

    # compute Y mod n from half exponents; (-1) ignored because even exponent => +1
    Y = 1
    for j, p in enumerate(factor_base):
        if p == -1:
            continue
        Y = (Y * pow(p, half[j], n)) % n

    # -----------------------------
    # NEW: Pretty RHS product string
    # -----------------------------
    rhs_prod_str = format_rhs_product(factor_base, sum_exps)

    print("\nHalbe Exponenten (für Y):")
    print(dict(zip(factor_base, half)))

    # -----------------------------
    # UPDATED OUTPUT: show formula + numbers
    # -----------------------------
    print(f"\nX ≡ ({X_formula}) (mod {n}) = {X}")
    print(f"Y ≡ sqrt({rhs_prod_str}) (mod {n}) = {Y}")

    print("\n=== gcd-Schritte ===")
    raw_diff = abs(X - Y)
    raw_sum  = abs(X + Y)

    a = raw_diff % n
    b = raw_sum % n

    g1 = math.gcd(a, n)
    g2 = math.gcd(b, n)

    # Optional: show raw |X-Y| too
    print(f"|X - Y| = {raw_diff}")
    print(f"|X - Y| mod n = {a}")
    print(f"gcd(|X - Y|, n) = gcd({a}, {n}) = {g1}")

    if 1 < g1 < n:
        print(f"\n>>> Faktor gefunden: {g1}")
        print(f">>> Anderer Faktor: {n // g1}")
        return

    print(f"\n|X + Y| = {raw_sum}")
    print(f"|X + Y| mod n = {b}")
    print(f"gcd(|X + Y|, n) = gcd({b}, {n}) = {g2}")

    if 1 < g2 < n:
        print(f"\n>>> Faktor gefunden: {g2}")
        print(f">>> Anderer Faktor: {n // g2}")
        return

    print("\nNur triviale Teiler (1 oder n). Versuch: mehr/andere Gleichungen eingeben.")

if __name__ == "__main__":
    main()
