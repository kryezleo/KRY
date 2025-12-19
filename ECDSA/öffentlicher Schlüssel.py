# ============================================
# Öffentlichen Schlüssel auf elliptischer Kurve
# Q = d * G
# ============================================

# --------- HIER ANPASSEN ---------------------
# Kurve: y^2 = x^3 + a*x + b (mod p)
p = 49037
a = 11784
b = 29274

# Basispunkt (Generator)
P = (11181, 14848)

# Geheimer Schlüssel
d = 8249
# --------------------------------------------


def inv_mod(x, p):
    """Modularer Inverser von x modulo p."""
    x %= p
    if x == 0:
        raise ZeroDivisionError("Kein Inverses für 0 mod p.")
    return pow(x, p - 2, p)


def ec_add(P, Q):
    """Punktaddition auf der elliptischen Kurve."""
    if P is None:
        return Q
    if Q is None:
        return P

    x1, y1 = P
    x2, y2 = Q

    # P + (-P) = O
    if x1 == x2 and (y1 + y2) % p == 0:
        return None

    if P == Q:
        # Punktverdopplung
        if y1 % p == 0:
            return None
        num = (3 * x1 * x1 + a) % p
        den = (2 * y1) % p
    else:
        # Normale Addition
        num = (y2 - y1) % p
        den = (x2 - x1) % p

    lam = (num * inv_mod(den, p)) % p
    x3 = (lam * lam - x1 - x2) % p
    y3 = (lam * (x1 - x3) - y1) % p

    return (x3, y3)


def scalar_mult(d, P):
    """Berechnet d * P (Double-and-Add)."""
    result = None
    addend = P

    while d > 0:
        if d & 1:
            result = ec_add(result, addend)
        addend = ec_add(addend, addend)
        d >>= 1

    return result


# --------- AUSFÜHRUNG ------------------------
if __name__ == "__main__":
    Q = scalar_mult(d, P)

    print("Elliptische Kurve: y^2 = x^3 + {}x + {} (mod {})".format(a, b, p))
    print("Basispunkt P =", P)
    print("Geheimer Schlüssel d =", d)
    print("Öffentlicher Schlüssel Q = d * P =", Q)
