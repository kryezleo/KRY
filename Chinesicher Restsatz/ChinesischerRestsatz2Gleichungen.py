# ============================================================
# Universelles CRT-Skript (Chinesischer Restsatz)
# - kann teilerfremde und nicht-teilerfremde Moduli
# - gibt Rechenschritte mit Formeln + Zahlen aus
# ============================================================

from math import gcd

# ------------------- HIER ANPASSEN --------------------------
# Beispiel aus deinem Bild:
# x ≡ 7 (mod 18) vertikal unten anordnen
# x ≡ 12 (mod 17) vertikal unten anordnen
a_list = [7, 12]
m_list = [18, 17]
verbose = True
# ------------------------------------------------------------


def egcd(a, b):
    """Extended Euclid: returns (g, x, y) with ax + by = g = gcd(a,b)."""
    if b == 0:
        return a, 1, 0
    g, x1, y1 = egcd(b, a % b)
    return g, y1, x1 - (a // b) * y1

def inv_mod(a, m):
    """Modular inverse a^{-1} mod m, if gcd(a,m)=1."""
    a %= m
    g, x, _ = egcd(a, m)
    if g != 1:
        return None
    return x % m

def crt_pair(a1, m1, a2, m2, verbose=True):
    """
    Löse:
      x ≡ a1 (mod m1)
      x ≡ a2 (mod m2)
    auch wenn m1,m2 nicht teilerfremd.
    Rückgabe: (a, m) für x ≡ a (mod m) oder None wenn unlösbar.
    """
    g = gcd(m1, m2)

    if verbose:
        print("------------------------------------------------------------")
        print(f"Kombiniere:")
        print(f"  x ≡ {a1} (mod {m1})")
        print(f"  x ≡ {a2} (mod {m2})")
        print(f"  g = gcd({m1},{m2}) = {g}")

    # Konsistenzbedingung
    if (a2 - a1) % g != 0:
        if verbose:
            print(f"  Prüfe Konsistenz: (a2-a1) mod g = ({a2}-{a1}) mod {g} = {(a2-a1)%g} ≠ 0")
            print("  ⇒ Keine Lösung.")
        return None

    # Reduzieren
    m1p = m1 // g
    m2p = m2 // g
    diff = (a2 - a1) // g

    # t ≡ diff * (m1p^{-1} mod m2p) (mod m2p)
    inv = inv_mod(m1p, m2p)
    if inv is None:
        # sollte nicht passieren, da gcd(m1p,m2p)=1
        if verbose:
            print("  Fehler: Inverses existiert nicht (unerwartet).")
        return None

    t = (diff * inv) % m2p

    # Lösung:
    # x = a1 + m1 * t
    lcm = (m1 * m2) // g
    x0 = (a1 + m1 * t) % lcm

    if verbose:
        print("  Reduktion:")
        print(f"    m1' = m1/g = {m1}/{g} = {m1p}")
        print(f"    m2' = m2/g = {m2}/{g} = {m2p}")
        print(f"    diff = (a2-a1)/g = ({a2}-{a1})/{g} = {diff}")
        print("  Formel:")
        print("    t ≡ diff · (m1'^{-1} mod m2')  (mod m2')")
        print(f"    m1'^{-1} mod m2' = {m1p}^(-1) mod {m2p} = {inv}")
        print(f"    t = {diff} · {inv} mod {m2p} = {t}")
        print("  Zusammensetzen:")
        print("    x = a1 + m1·t")
        print(f"    x = {a1} + {m1}·{t} = {a1 + m1*t}")
        print(f"    modulo lcm(m1,m2) = {lcm}")
        print(f"    ⇒ x ≡ {x0} (mod {lcm})")

    return x0, lcm

def crt(a_list, m_list, verbose=True):
    """Kombiniert viele Kongruenzen per Paarweise-CRT."""
    if len(a_list) != len(m_list) or len(a_list) == 0:
        raise ValueError("Listen müssen gleich lang und nicht leer sein.")

    # Normalisieren
    a0 = a_list[0] % m_list[0]
    m0 = m_list[0]

    if verbose:
        print("============================================================")
        print("Chinesischer Restsatz (universell)")
        print("============================================================")
        print("Start:")
        print(f"  x ≡ {a0} (mod {m0})")

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
        print("\n❌ Keine Lösung für das System.")
    else:
        x, mod = sol
        print("\n✅ Lösung:")
        print(f"  x ≡ {x} (mod {mod})")
        print("  Kontrolle:", check_solution(x, a_list, m_list))
