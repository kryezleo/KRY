# ============================================================
# Aufgabe 5(b) (3 Punkte)
#
# Bestimmen Sie die Lösungsmenge durch modulares Wurzelziehen.
# Es müssen alle Zwischenresultate angegeben werden.
#
# (b) x^4 ≡ 75 (mod 83). Hinweis: Substituieren Sie y = x^2.
#
# Vorgehen:
#   1) Setze y = x^2  ->  y^2 ≡ 75 (mod 83)
#   2) Löse y^2 ≡ 75 (mod 83)  -> y-Werte
#   3) Für jedes y: löse x^2 ≡ y (mod 83)
#   4) Vereinigung aller x-Lösungen ist die Lösungsmenge von x^4 ≡ 75.
# ============================================================

# --- HIER ANPASSEN (Aufgabe 5b) ---
p = 83
a = 75
verbose = True
# ----------------------------------

def legendre_symbol(n, p):
    """Legendre-Symbol (n/p) als Wert in {0,1,p-1}"""
    return pow(n % p, (p - 1) // 2, p)

def sqrt_mod_prime(n, p, verbose=False, label=""):
    """
    Löst x^2 ≡ n (mod p) für ungerades Prim p.
    Gibt (x, p-x) oder None zurück.
    Hier: nutzt den schnellen Fall p ≡ 3 (mod 4), sonst bricht ab.
    """
    n %= p
    ls = legendre_symbol(n, p)
    if verbose:
        print(f"\n{label}Löse x² ≡ {n} (mod {p})")
        print("Legendre-Test:")
        print(f"  n^((p-1)/2) mod p = {n}^(({p}-1)/2) mod {p}")
        print(f"                       = {ls}")

    if ls != 1:
        if verbose:
            print("  ⇒ Kein quadratischer Rest ⇒ keine Lösung.")
        return None

    if p % 4 == 3:
        e = (p + 1) // 4
        x = pow(n, e, p)
        if verbose:
            print("\nSonderfall p ≡ 3 (mod 4):")
            print("  x = n^((p+1)/4) mod p")
            print(f"    = {n}^(({p}+1)/4) mod {p}")
            print(f"    = {n}^{e} mod {p}")
            print(f"    = {x}")
            print(f"  zweite Lösung: p - x = {p - x}")
        return x, (p - x) % p

    raise NotImplementedError("Dieser Helfer implementiert hier nur den Fall p ≡ 3 (mod 4).")

def solve_x4_congruence(a, p, verbose=True):
    """
    Löst x^4 ≡ a (mod p) über y=x^2.
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

    y_roots = sqrt_mod_prime(a, p, verbose=verbose, label="2) ")
    if y_roots is None:
        if verbose:
            print("\n⇒ Keine y-Lösung ⇒ keine x-Lösung.")
        return set()

    y1, y2 = y_roots
    if verbose:
        print(f"\n✅ Lösungen für y² ≡ {a} (mod {p}): y ≡ {y1} oder y ≡ {y2} (mod {p})")

    # Schritt 2: Für jedes y: x^2 ≡ y (mod p)
    solutions = set()
    for idx, y in enumerate([y1, y2], start=1):
        if verbose:
            print("\n------------------------------------------------------------")
            print(f"3) Löse nun x² ≡ y (mod p) für y = {y}  (Fall {idx})")
            print("------------------------------------------------------------")

        roots = sqrt_mod_prime(y, p, verbose=verbose, label="   ")
        if roots is None:
            if verbose:
                print(f"⇒ Für y = {y} gibt es keine x-Lösung.")
            continue

        r1, r2 = roots
        solutions.add(r1)
        solutions.add(r2)
        if verbose:
            print(f"\n✅ Lösungen für x² ≡ {y} (mod {p}): x ≡ {r1} oder x ≡ {r2} (mod {p})")

    if verbose:
        print("\n============================================================")
        if solutions:
            sols_sorted = sorted(solutions)
            print(f"✅ Lösungsmenge für x^4 ≡ {a} (mod {p}):")
            print("   L =", sols_sorted)
            print("\nKontrolle (x^4 mod p):")
            for x in sols_sorted:
                print(f"  {x}^4 mod {p} = {pow(x,4,p)}")
        else:
            print(f"❌ Keine Lösungen für x^4 ≡ {a} (mod {p}).")
        print("============================================================")

    return solutions

if __name__ == "__main__":
    solve_x4_congruence(a, p, verbose=verbose)
