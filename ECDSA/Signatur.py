# ============================================
# Nur ECDSA-r berechnen:
# R = k*G, r = R.x mod n
# E: y^2 = x^3 + a*x + b (mod p)
# ============================================

# --- HIER ANPASSEN ---
p = 49037
a = 11784
b = 29274

P = (11181, 14848)   # Basispunkt / Generator
n = 49363            # Ordnung von G (oder vorgegeben)

k = 17413            # Nonce
# ---------------------

def inv_mod(x, p):
    x %= p
    if x == 0:
        raise ZeroDivisionError("Kein Inverses für 0 mod p.")
    return pow(x, p - 2, p)

def ec_add(P, Q):
    """P + Q auf der Kurve. None = Punkt im Unendlichen."""
    if P is None:
        return Q
    if Q is None:
        return P

    x1, y1 = P
    x2, y2 = Q

    # P == -Q
    if x1 == x2 and (y1 + y2) % p == 0:
        return None

    if P == Q:
        # Verdopplung
        if y1 % p == 0:
            return None
        num = (3 * x1 * x1 + a) % p
        den = (2 * y1) % p
    else:
        # Addition
        num = (y2 - y1) % p
        den = (x2 - x1) % p

    lam = (num * inv_mod(den, p)) % p
    x3 = (lam * lam - x1 - x2) % p
    y3 = (lam * (x1 - x3) - y1) % p
    return (x3, y3)

def scalar_mult(k, P):
    """k*P via Double-and-Add."""
    result = None
    addend = P
    while k > 0:
        if k & 1:
            result = ec_add(result, addend)
        addend = ec_add(addend, addend)
        k >>= 1
    return result

def ecdsa_r(k, G, n):
    R = scalar_mult(k, G)
    if R is None:
        raise ValueError("R ist Punkt im Unendlichen -> anderes k wählen.")
    r = R[0] % n
    return r, R

if __name__ == "__main__":
    r, R = ecdsa_r(k, P, n)
    print("Kurve: y^2 = x^3 + {}x + {} (mod {})".format(a, b, p))
    print("G =", P)
    print("k =", k)
    print("R = k*G =", R)
    print("r = R.x mod n =", r)
