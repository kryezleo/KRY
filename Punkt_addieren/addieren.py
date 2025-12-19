# ============================================================
# Elliptische Kurve + ECDSA-Helferskript
# Für Kurven der Form: y^2 = x^3 + a*x + b (mod p)
# ============================================================

# --------- 1. PARAMETER ANPASSEN -----------------------------
# >>> HIER deine Kurve und ECDSA-Parameter einstellen <<<

p = 179          # Primzahl des Körpers F_p
a = 8            # Parameter a der Kurve
b = 102          # Parameter b der Kurve

# Basispunkt P (Generator)
G = (73, 60)     # P = (x, y)

# Ordnung des Basispunkts
n = 167          # z.B. aus Aufgabe

# Geheimer Schlüssel und "Nonce" k, Hash h(m)
d = 37           # geheimer Schlüssel
k = 94           # Zufallszahl für ECDSA-Signatur
h = 121          # Hash-Wert der Nachricht


# --------- 2. HILFSFUNKTIONEN -------------------------------

def inv_mod(x, m):
    """Modulare Inverse: finde y mit x*y ≡ 1 (mod m)."""
    return pow(x % m, m - 2, m)  # nur korrekt, wenn m prim

def ec_add(P, Q):
    """Punktaddition auf der elliptischen Kurve.
       P, Q: Tupel (x,y) oder None (Punkt im Unendlichen)."""
    if P is None:
        return Q
    if Q is None:
        return P

    x1, y1 = P
    x2, y2 = Q

    # P == -Q -> Punkt im Unendlichen
    if x1 == x2 and (y1 + y2) % p == 0:
        return None

    if P == Q:
        # Punktverdopplung
        num = (3 * x1 * x1 + a) % p
        den = (2 * y1) % p
    else:
        # Punktaddition
        num = (y2 - y1) % p
        den = (x2 - x1) % p

    lam = (num * inv_mod(den, p)) % p

    x3 = (lam * lam - x1 - x2) % p
    y3 = (lam * (x1 - x3) - y1) % p
    return (x3, y3)

def scalar_mult(k, P):
    """k * P mit Double-and-Add."""
    result = None   # Punkt im Unendlichen
    addend = P

    while k > 0:
        if k & 1:
            result = ec_add(result, addend)
        addend = ec_add(addend, addend)
        k >>= 1

    return result


# --------- 3. ECDSA: SIGNIEREN UND VERIFIZIEREN --------------

def ecdsa_sign(h, d, k):
    """ECDSA-Signatur (r,s) für Hash h mit privatem Schlüssel d und Nonce k."""
    # Schritt 1: kP
    kP = scalar_mult(k, G)
    xk, yk = kP
    r = xk % n
    if r == 0:
        raise ValueError("r = 0, wähle ein anderes k")

    # Schritt 2: k^{-1} mod n
    k_inv = inv_mod(k, n)

    # Schritt 3: s = k^{-1}(h + d*r) mod n
    s = (k_inv * (h + d * r)) % n
    if s == 0:
        raise ValueError("s = 0, wähle ein anderes k")

    return (r, s), kP  # kP geben wir zurück, falls du es sehen willst

def ecdsa_verify(h, Q, r, s):
    """ECDSA-Verifikation. Liefert (bool, X, u1, u2)."""
    if not (1 <= r < n and 1 <= s < n):
        return False, None, None, None

    w = inv_mod(s, n)              # s^{-1} mod n
    u1 = (h * w) % n
    u2 = (r * w) % n

    # Variante 1 (direkt): X = u1*G + u2*Q
    # X1 = ec_add(scalar_mult(u1, G), scalar_mult(u2, Q))

    # Variante 2 (schnell, wenn Q = dG): X = (u1 + u2*d) * G
    # Nur korrekt, wenn du d kennst; bei echter Verifikation nimmt man Variante 1.
    X = ec_add(scalar_mult(u1, G), scalar_mult(u2, Q))

    if X is None:
        return False, X, u1, u2

    xX, yX = X
    return (r == xX % n), X, u1, u2


# --------- 4. BEISPIELLAUF MIT DEINEN ZAHLEN -----------------

if __name__ == "__main__":
    print("Kurve: y^2 = x^3 + {}x + {} (mod {})".format(a, b, p))
    print("Basispunkt P =", G)
    print("Ordnung n   =", n)
    print()

    # Öffentlicher Schlüssel Q = d*P
    Q = scalar_mult(d, G)
    print(f"Privater Schlüssel d = {d}")
    print(f"Öffentlicher Schlüssel Q = d*P = {Q}")
    print()

    # Signatur berechnen
    (r, s), kP = ecdsa_sign(h, d, k)
    print(f"Nonce k = {k}")
    print(f"kP      = {kP}")
    print(f"Hash h  = {h}")
    print(f"Signatur: r = {r}, s = {s}")
    print()

    # Verifikation
    ok, X, u1, u2 = ecdsa_verify(h, Q, r, s)
    print("Verifikation:")
    print(f"u1 = {u1}, u2 = {u2}")
    print(f"X  = u1*P + u2*Q = {X}")
    print(f"gilt r == x_X mod n ? -> {ok}")
