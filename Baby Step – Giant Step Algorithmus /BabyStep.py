# ================================================
# Elliptische Kurve: Baby-Step-Tabelle generieren
# ================================================

# Kurvenparameter: y^2 = x^3 + a*x + b (mod p)
p = 43          # Primzahl (z.B. 43)
a = 22          # Parameter a (z.B. 22)
b = 17          # Parameter b (z.B. 17)

# Basispunkt P
P = (37, 20)    # z.B. aus Aufgabe: P = (37,20)

# Anzahl Schritte für Tabelle (Baby Steps)
m = 8           # z.B. m = ceil(sqrt(n)) = 8 bei n = 53, wurzel von n aufgerundet


# ---------- Hilfsfunktionen ----------

INF = None  # Punkt im Unendlichen (neutrales Element)


def inv_mod(x, p):
    """Modulare Inverse von x modulo p (p prim)."""
    return pow(x % p, -1, p)


def point_add(P, Q, a, p):
    """
    Punktaddition P + Q auf der elliptischen Kurve y^2 = x^3 + a*x + b (mod p).
    P und Q sind Tupel (x, y) oder INF.
    """
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
        # λ = (y2 - y1) / (x2 - x1)
        num = (y2 - y1) % p
        den = (x2 - x1) % p
        lam = (num * inv_mod(den, p)) % p
    else:
        # Punktverdopplung: λ = (3*x1^2 + a) / (2*y1)
        num = (3 * x1 * x1 + a) % p
        den = (2 * y1) % p
        lam = (num * inv_mod(den, p)) % p

    x3 = (lam * lam - x1 - x2) % p
    y3 = (lam * (x1 - x3) - y1) % p
    return (x3, y3)


def scalar_mul(k, P, a, p):
    """Skalarmultiplikation k*P mit Double-and-Add."""
    result = INF
    addend = P
    k_bin = k

    while k_bin > 0:
        if k_bin & 1:
            result = point_add(result, addend, a, p)
        addend = point_add(addend, addend, a, p)
        k_bin >>= 1

    return result


# ---------- Baby-Step-Tabelle ----------

def baby_step_table(P, m, a, p):
    """
    Erzeugt eine Liste [(r, r*P), ...] für r = 0..m-1
    und gibt sie auch schön aus.
    """
    table = []
    R = INF  # 0*P = INF
    for r in range(m):
        table.append((r, R))
        # nächster Schritt: (r+1)*P = r*P + P
        R = point_add(R, P, a, p)
    return table


if __name__ == "__main__":
    table = baby_step_table(P, m, a, p)

    print("r   r·P")
    print("--------------")
    for r, R in table:
        if R is INF:
            print(f"{r:<2}  O (neutrales Element)")
        else:
            x, y = R
            print(f"{r:<2}  ({x:2d}, {y:2d})")
