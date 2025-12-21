# ============================================================
# Aufgabe 5(b): x^4 ≡ a (mod p), p prim
# Substitution: y = x^2  ->  y^2 ≡ a (mod p)
# Dann: für jedes y die Lösungen von x^2 ≡ y (mod p)
# ============================================================

p = 83
a = 75
verbose = True


def legendre_symbol(n: int, p: int) -> int:
    """Legendre-Symbol (n/p) als Wert in {0, 1, p-1}."""
    return pow(n % p, (p - 1) // 2, p)


def tonelli_shanks(n: int, p: int, verbose: bool = False, label: str = ""):
    """
    Löst x^2 ≡ n (mod p) für ungerades Prim p.
    Gibt (x, p-x) zurück oder None (keine Lösung).
    Implementiert:
      - n=0 Spezialfall
      - p ≡ 3 (mod 4) Shortcut
      - sonst Tonelli–Shanks allgemein
    """
    n %= p
    if verbose:
        print(f"\n{label}Löse x² ≡ {n} (mod {p})")

    # Spezialfall n = 0
    if n == 0:
        if verbose:
            print("Spezialfall: n = 0 ⇒ x ≡ 0 ist Lösung.")
        return (0, 0)

    # Legendre-Test
    ls = legendre_symbol(n, p)
    if verbose:
        print("Legendre-Test:")
        print(f"  {n}^(({p}-1)/2) mod {p} = {ls}")

    if ls != 1:
        if verbose:
            print("  ⇒ Kein quadratischer Rest ⇒ keine Lösung.")
        return None

    # Shortcut p ≡ 3 (mod 4)
    if p % 4 == 3:
        e = (p + 1) // 4
        x = pow(n, e, p)
        if verbose:
            print("\nSonderfall p ≡ 3 (mod 4):")
            print(f"  x = {n}^(({p}+1)/4) mod {p} = {n}^{e} mod {p} = {x}")
            print(f"  zweite Lösung: {p-x}")
        return (x, (p - x) % p)

    # Tonelli–Shanks allgemein
    # Schreibe p-1 = q * 2^s mit q ungerade
    q = p - 1
    s = 0
    while q % 2 == 0:
        q //= 2
        s += 1

    if verbose:
        print("\nZerlegung von p−1:")
        print(f"  p−1 = {p-1} = {q} · 2^{s}")

    # Finde z = Nicht-Quadratischer Rest
    z = 2
    while legendre_symbol(z, p) != p - 1:
        z += 1

    if verbose:
        print("\nNichtquadratischer Rest z:")
        print(f"  z = {z} (weil (z/p) = -1)")

    # Initialisierung
    c = pow(z, q, p)
    x = pow(n, (q + 1) // 2, p)
    t = pow(n, q, p)
    m = s

    if verbose:
        print("\nInitialisierung:")
        print(f"  c = z^q mod p = {z}^{q} mod {p} = {c}")
        print(f"  x = n^((q+1)/2) mod p = {n}^{(q+1)//2} mod {p} = {x}")
        print(f"  t = n^q mod p = {n}^{q} mod {p} = {t}")
        print(f"  m = {m}")

    # Iteration
    step = 1
    while t != 1:
        # Finde kleinstes i: t^(2^i) = 1
        i = 0
        temp = t
        while temp != 1:
            temp = (temp * temp) % p
            i += 1
            if i == m:
                # sollte nicht passieren, wenn n QR ist
                return None

        if verbose:
            print(f"\nIteration {step}:")
            print(f"  finde i mit t^(2^i) ≡ 1: i = {i}")

        # b = c^(2^(m-i-1))
        b = pow(c, 1 << (m - i - 1), p)

        if verbose:
            print(f"  b = c^(2^(m-i-1)) = {b}")

        x = (x * b) % p
        t = (t * b * b) % p
        c = (b * b) % p
        m = i
        step += 1

        if verbose:
            print(f"  update: x={x}, t={t}, c={c}, m={m}")

    return (x, (p - x) % p)


def solve_x4_congruence(a: int, p: int, verbose: bool = True):
    """
    Löst x^4 ≡ a (mod p) über y=x^2:
      1) y^2 ≡ a (mod p)
      2) für jedes y: x^2 ≡ y (mod p)
    """
    a %= p
    if verbose:
        print("============================================================")
        print(f"Gesucht: Lösungen von x^4 ≡ {a} (mod {p})")
        print("Substitution: y = x^2  ⇒  y^2 ≡ a (mod p)")
        print("============================================================")

    # Schritt 1: y^2 ≡ a (mod p)
    if verbose:
        print("\n1) Substitution:")
        print(f"   y = x²  ⇒  y² ≡ {a} (mod {p})")

    y_roots = tonelli_shanks(a, p, verbose=verbose, label="2) ")
    if y_roots is None:
        if verbose:
            print("\n⇒ Keine y-Lösung ⇒ keine x-Lösung.")
        return set()

    y1, y2 = y_roots
    y_vals = sorted(set([y1, y2]))

    if verbose:
        if len(y_vals) == 1:
            print(f"\n✅ Lösung für y² ≡ {a} (mod {p}): y ≡ {y_vals[0]} (mod {p})")
        else:
            print(f"\n✅ Lösungen für y² ≡ {a} (mod {p}): y ≡ {y_vals[0]} oder y ≡ {y_vals[1]} (mod {p})")

    # Schritt 2: Für jedes y: x^2 ≡ y (mod p)
    solutions = set()
    for idx, y in enumerate(y_vals, start=1):
        if verbose:
            print("\n------------------------------------------------------------")
            print(f"3) Löse nun x² ≡ y (mod p) für y = {y}  (Fall {idx})")
            print("------------------------------------------------------------")

        roots = tonelli_shanks(y, p, verbose=verbose, label="   ")
        if roots is None:
            if verbose:
                print(f"⇒ Für y = {y} gibt es keine x-Lösung.")
            continue

        r1, r2 = roots
        solutions.add(r1)
        solutions.add(r2)

        if verbose:
            if r1 == r2:
                print(f"\n✅ Lösung für x² ≡ {y} (mod {p}): x ≡ {r1}")
            else:
                print(f"\n✅ Lösungen für x² ≡ {y} (mod {p}): x ≡ {r1} oder x ≡ {r2} (mod {p})")

    if verbose:
        print("\n============================================================")
        if solutions:
            sols_sorted = sorted(solutions)
            print(f"✅ Lösungsmenge für x^4 ≡ {a} (mod {p}):")
            print("   L =", sols_sorted)
            print("\nKontrolle (x^4 mod p):")
            for x in sols_sorted:
                print(f"  {x}^4 mod {p} = {pow(x, 4, p)}")
        else:
            print(f"❌ Keine Lösungen für x^4 ≡ {a} (mod {p}).")
        print("============================================================")

    return solutions


if __name__ == "__main__":
    solve_x4_congruence(a, p, verbose=verbose)
