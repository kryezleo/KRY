# ================================================
# Baby-Step-Giant-Step auf elliptischer Kurve
# ================================================
# Kurve:  y^2 = x^3 + a*x + b  (mod p)
# Ziel:   x finden mit  x*P = A
#
# Dieses Skript:
#  - berechnet m = ceil(sqrt(n))
#  - erzeugt die Baby-Step-Tabelle
#  - führt Giant-Steps aus
#  - gibt alle Zwischenschritte aus
# ================================================

import math

# -------- Parameter HIER anpassen (Beispiel: Aufgabe 6) --------
p = 43                  # Primzahl des Feldes
a = 22                  # Kurvenparameter a
b = 17                  # Kurvenparameter b (eig. nicht direkt benötigt)
P = (37, 20)            # Basispunkt
n = 53                  # Ordnung von P
A = (12, 26)            # Zielpunkt A = x*P
# ---------------------------------------------------------------

INF = None  # Punkt im Unendlichen (neutrales Element)


def inv_mod(x, p):
    """Modulare Inverse von x modulo p (p prim)."""
    return pow(x % p, -1, p)


def point_add(P, Q, a, p):
    """Punktaddition P + Q auf der elliptischen Kurve."""
    if P is INF:
        return Q
    if Q is INF:
        return P

    x1, y1 = P
    x2, y2 = Q

    # P + (-P) = INF
    if x1 == x2 and (y1 + y2) % p == 0:
        return INF

    if P != Q:
        # lambda = (y2 - y1) / (x2 - x1)
        num = (y2 - y1) % p
        den = (x2 - x1) % p
        lam = (num * inv_mod(den, p)) % p
    else:
        # Punktverdopplung
        num = (3 * x1 * x1 + a) % p
        den = (2 * y1) % p
        lam = (num * inv_mod(den, p)) % p

    x3 = (lam * lam - x1 - x2) % p
    y3 = (lam * (x1 - x3) - y1) % p
    return (x3, y3)


def scalar_mul(k, P, a, p):
    """Skalarmultiplikation k*P (Double-and-Add)."""
    result = INF
    addend = P
    k_bin = k

    while k_bin > 0:
        if k_bin & 1:
            result = point_add(result, addend, a, p)
        addend = point_add(addend, addend, a, p)
        k_bin >>= 1
    return result


# ----------------- Baby Steps -----------------

def baby_steps(P, m, a, p):
    """
    Baby-Step-Tabelle: r -> r*P für r = 0..m-1
    Gibt die Tabelle aus und liefert auch ein Dict {Punkt: r}.
    """
    print("=== Baby Steps ===")
    table = {}
    R = INF  # 0*P
    for r in range(m):
        if R is INF:
            print(f"r = {r:2d}:  O (neutrales Element)")
        else:
            print(f"r = {r:2d}:  {R}")
        table[R] = r
        R = point_add(R, P, a, p)  # nächstes r*P
    print()
    return table


# ----------------- Giant Steps -----------------

def negate_point(P, p):
    """Negation eines Punkts P = (x,y) -> (x,-y)."""
    if P is INF:
        return INF
    x, y = P
    return (x, (-y) % p)


def giant_steps(A, P, n, a, p, baby_table):
    """
    Führt Giant-Steps aus:
        r*P = A + q*(-mP)
    und gibt Zwischenschritte aus.
    Liefert (q, r, x) wenn Lösung gefunden, sonst None.
    """
    m = math.isqrt(n)
    if m * m < n:
        m += 1
    print(f"Ordnung n = {n},  m = ceil(sqrt(n)) = {m}\n")

    # mP und -mP berechnen
    mP = scalar_mul(m, P, a, p)
    minus_mP = negate_point(mP, p)
    print(f"m*P     = {mP}")
    print(f"-m*P    = {minus_mP}\n")

    print("=== Giant Steps ===")
    Q = A
    for q in range(m):
        print(f"q = {q:2d}:  A + {q} * (-mP) = {Q}")
        # Prüfen, ob Q in Baby-Tabelle vorkommt
        if Q in baby_table:
            r = baby_table[Q]
            x = q * m + r
            print("\n>>> Treffer gefunden!")
            print(f"r*P = {Q} mit r = {r}")
            print(f"A + q*(-mP) = {Q} mit q = {q}")
            print(f"x = q*m + r = {q}*{m} + {r} = {x}")
            return q, r, x
        # nächster Giant Step: Q = Q + (-mP)
        Q = point_add(Q, minus_mP, a, p)

    print("\nKeine Lösung in diesem Bereich gefunden.")
    return None


# ================== Hauptteil ==================

if __name__ == "__main__":
    # m aus n berechnen
    m = math.isqrt(n)
    if m * m < n:
        m += 1

    print(f"Kurve: y^2 = x^3 + {a}x + {b} (mod {p})")
    print(f"P = {P},  Ordnung n = {n}")
    print(f"A = {A}")
    print(f"m = ceil(sqrt(n)) = {m}\n")

    # Baby Steps
    baby_table = baby_steps(P, m, a, p)

    # Giant Steps
    giant_steps(A, P, n, a, p, baby_table)
