# pollard_rho.py
# Universelles Pollard-ρ-Skript zur Lösung des diskreten Logarithmus g^x = h (mod p)
# ÄNDERN: p, g, h (und optional order) im __main__-Block weiter unten.

from math import gcd

def default_partition(v):
    """Standardpartition: drei Klassen per v % 3. Kann angepasst werden."""
    return v % 3

def pollard_rho_discrete_log(g, h, p, order=None, partition_func=None, max_iterations=10**6):
    """
    Versucht x zu finden mit g^x ≡ h (mod p) via Pollard's rho (Floyd cycle).
    Rückgabe: x oder None falls kein Ergebnis gefunden.
    """
    if partition_func is None:
        partition_func = default_partition
    if order is None:
        order = p - 1  # Standard: p prime -> Gruppeordnung p-1

    def step(state):
        v, a, b = state
        cls = partition_func(v)
        if cls == 0:
            v = (v * g) % p
            a = (a + 1) % order
        elif cls == 1:
            v = (v * h) % p
            b = (b + 1) % order
        else:
            v = pow(v, 2, p)
            a = (2 * a) % order
            b = (2 * b) % order
        return (v, a, b)

    # Startzustände
    tort = (1, 0, 0)
    hare = step(tort)

    iterations = 0
    while iterations < max_iterations:
        tort = step(tort)
        hare = step(step(hare))
        iterations += 1

        if tort[0] == hare[0]:
            v1, a1, b1 = tort
            v2, a2, b2 = hare
            A = (a1 - a2) % order
            B = (b2 - b1) % order
            d = gcd(B, order)
            if d == 0:
                return None
            if A % d != 0:
                return None
            B_red = B // d
            A_red = A // d
            order_red = order // d

            # Erweiterter Euklid zur Inversenberechnung
            def egcd(a, b):
                if b == 0:
                    return (a, 1, 0)
                else:
                    g0, x1, y1 = egcd(b, a % b)
                    return (g0, y1, x1 - (a // b) * y1)

            g_inv, x_inv, _ = egcd(B_red, order_red)
            if g_inv != 1:
                return None
            inv_B = x_inv % order_red
            x0 = (inv_B * A_red) % order_red

            # Allgemeine Lösungen: x = x0 + k*order_red, k=0..d-1 -> prüfe kleinste, die passt
            for k in range(d):
                cand = (x0 + k * order_red) % order
                if pow(g, cand, p) == h % p:
                    return cand
            return None
    return None

if __name__ == "__main__":
    # === PARAMETER (HIER ÄNDERN) ===
    p = 23      # Modulus (Primzahl=Z)
    g = 5       # Basis/Generator
    h = 10      # Ziel: finde x mit g^x ≡ h (mod p)
    order = 22  # Ordnung der Gruppe Z= p-1 (optional), sonst None
    # ================================

    result = pollard_rho_discrete_log(g, h, p, order=order)
    if result is None:
        print("Keine Lösung gefunden (oder Kollision führte zu keiner lösbaren Gleichung).")
    else:
        print(f"Lösung gefunden: x = {result}")
        print(f"Prüfung: {g}^{result} mod {p} = {pow(g,result,p)} (soll {h % p})")
