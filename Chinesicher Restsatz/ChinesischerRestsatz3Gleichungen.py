# ============================================================
# CRT (Chinesischer Restsatz) – für 3 (oder mehr) Gleichungen
# ============================================================

from math import gcd

# ------------------- HIER ANPASSEN --------------------------
# Beispiel mit 3 Kongruenzen:
# x ≡ 2  (mod 3) vertikal unten anordnen
# x ≡ 3  (mod 5) vertikal unten anordnen
# x ≡ 2  (mod 7) vertikal unten anordnen
a_list = [2, 3, 2]
m_list = [3, 5, 7]
verbose = True
# ------------------------------------------------------------


def egcd(a, b):
    if b == 0:
        return a, 1, 0
    g, x1, y1 = egcd(b, a % b)
    return g, y1, x1 - (a // b) * y1

def inv_mod(a, m):
    a %= m
    g, x, _ = egcd(a, m)
    if g != 1:
        return None
    return x % m

def crt_pair(a1, m1, a2, m2, verbose=True):
    """
    Kombiniert:
      x ≡ a1 (mod m1)
      x ≡ a2 (mod m2)
    auch falls m1,m2 nicht teilerfremd.
    """
    g = gcd(m1, m2)

    if verbose:
        print("------------------------------------------------------------")
        print(f"Kombiniere:")
        print(f"  x ≡ {a1} (mod {m1})")
        print(f"  x ≡ {a2} (mod {m2})")
        print(f"  g = gcd({m1},{m2}) = {g}")

    if (a2 - a1) % g != 0:
        if verbose:
            print(f"  Konsistenztest: ({a2}-{a1}) mod {g} = {(a2-a1)%g} ≠ 0")
            print("  ⇒ Keine Lösung.")
        return None

    m1p = m1 // g
    m2p = m2 // g
    diff = (a2 - a1) // g

    inv = inv_mod(m1p, m2p)
    if inv is None:
        return None

    t = (diff * inv) % m2p

    lcm = (m1 * m2) // g
    x0 = (a1 + m1 * t) % lcm

    if verbose:
        print("  Reduktion:")
        print(f"    m1' = {m1p}, m2' = {m2p}, diff = {diff}")
        print("  Formel:")
        print("    t ≡ diff · (m1'^{-1} mod m2')  (mod m2')")
        print(f"    m1'^{-1} mod m2' = {m1p}^(-1) mod {m2p} = {inv}")
        print(f"    t = {diff} · {inv} mod {m2p} = {t}")
        print("  Zusammensetzen:")
        print(f"    x = a1 + m1·t = {a1} + {m1}·{t} = {a1 + m1*t}")
        print(f"    ⇒ x ≡ {x0} (mod {lcm})")

    return x0, lcm

def crt(a_list, m_list, verbose=True):
    if len(a_list) != len(m_list) or len(a_list) == 0:
        raise ValueError("Listen müssen gleich lang und nicht leer sein.")

    a0 = a_list[0] % m_list[0]
    m0 = m_list[0]

    if verbose:
        print("============================================================")
        print("Chinesischer Restsatz")
        print("============================================================")
        print(f"Start: x ≡ {a0} (mod {m0})")

    for i in range(1, len(a_list)):
        ai = a_list[i] % m_list[i]
        mi = m_list[i]
        res = crt_pair(a0, m0, ai, mi, verbose=verbose)
        if res is None:
            return None
        a0, m0 = res
        if verbose:
            print(f"Zwischenergebnis: x ≡ {a0} (mod {m0})")

    if verbose:
        print("============================================================")
        print(f"ENDRESULTAT: x ≡ {a0} (mod {m0})")
        print("============================================================")
    return a0, m0

def check_solution(x, a_list, m_list):
    return all(x % m_list[i] == (a_list[i] % m_list[i]) for i in range(len(a_list)))


if __name__ == "__main__":
    sol = crt(a_list, m_list, verbose=verbose)
    if sol is None:
        print("\n❌ Keine Lösung.")
    else:
        x, mod = sol
        print("\n✅ Lösung:")
        print(f"  x ≡ {x} (mod {mod})")
        print("  Kontrolle:", check_solution(x, a_list, m_list))
