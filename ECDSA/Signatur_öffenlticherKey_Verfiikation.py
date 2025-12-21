# ============================================================
# UNIVERSAL ECDSA (Signatur + Verifikation + Nachweis)
# Kurve: y^2 = x^3 + a*x + b (mod p)
# ============================================================

# -------------------- HIER ANPASSEN -------------------------
p = 49037
a = 11784
b = 29274

P = (11181, 14848)   # Generator
n = 49363            # Ordnung von P (falls vorgegeben) ODER None

d  = 8249            # privater Schlüssel (aus Aufgabe)
k  = 17413           # Nonce (aus Aufgabe)
hm = 12345           # h(m) als Integer (aus Aufgabe)
# ------------------------------------------------------------

verbose = True


# -------------------- MATHE HILFEN --------------------------
def egcd(A, B):
    if B == 0:
        return A, 1, 0
    g, x1, y1 = egcd(B, A % B)
    return g, y1, x1 - (A // B) * y1

def inv_mod(x, m):
    """Modulares Inverses von x mod m (Extended Euclid)."""
    x %= m
    g, u, _ = egcd(x, m)
    if g != 1:
        raise ValueError(f"Kein Inverses: gcd({x}, {m}) = {g} != 1")
    return u % m

def inv_mod_p(x):
    """Inverses mod p (p prim)."""
    x %= p
    if x == 0:
        raise ZeroDivisionError("Kein Inverses für 0 mod p.")
    return pow(x, p - 2, p)


# -------------------- EC-FUNKTIONEN --------------------------
def is_on_curve(Pt):
    if Pt is None:
        return True
    x, y = Pt
    return (y*y - (x*x*x + a*x + b)) % p == 0

def ec_add(P1, P2):
    """P1 + P2 auf der Kurve; None = Punkt im Unendlichen."""
    if P1 is None:
        return P2
    if P2 is None:
        return P1

    x1, y1 = P1
    x2, y2 = P2

    # P + (-P) = O
    if x1 == x2 and (y1 + y2) % p == 0:
        return None

    if P1 == P2:
        # Verdopplung
        if y1 % p == 0:
            return None
        num = (3 * x1 * x1 + a) % p
        den = (2 * y1) % p
    else:
        # Addition
        num = (y2 - y1) % p
        den = (x2 - x1) % p

    lam = (num * inv_mod_p(den)) % p
    x3 = (lam * lam - x1 - x2) % p
    y3 = (lam * (x1 - x3) - y1) % p
    return (x3, y3)

def scalar_mult(k, Pt):
    """k * Pt (Double-and-Add)."""
    k = int(k)
    R = None
    A = Pt
    while k > 0:
        if k & 1:
            R = ec_add(R, A)
        A = ec_add(A, A)
        k >>= 1
    return R


# -------------------- ORDNUNG (nur falls n=None) -------------
def point_order(Pt):
    """
    Bestimmt Ordnung ord(Pt) mit Hasse-Obergrenze:
      #E(F_p) <= p + 1 + 2*sqrt(p)
    Die Punktordnung teilt #E(F_p), liegt also <= dieser Grenze.
    """
    from math import isqrt
    max_steps = p + 1 + 2 * isqrt(p) + 5  # kleine Reserve

    R = None
    for i in range(1, max_steps + 1):
        R = ec_add(R, Pt)
        if R is None:
            return i
    raise RuntimeError("Ordnung nicht gefunden (Hasse-Grenze erreicht).")


# -------------------- ECDSA: SIGNIEREN -----------------------
def ecdsa_sign(hm, d, k, P, n, verbose=True):
    hm %= n

    if verbose:
        print("============================================================")
        print("ECDSA SIGNATUR")
        print("============================================================")
        print("Formeln:")
        print("  R = k·P")
        print("  r = x_R mod n")
        print("  s = k^{-1}(h(m) + r·d) mod n\n")

    # 1) R = kP
    R = scalar_mult(k, P)
    if R is None:
        raise ValueError("R = O (Punkt im Unendlichen). Wähle anderes k.")

    # 2) r = x_R mod n
    r = R[0] % n
    if r == 0:
        raise ValueError("r = 0. Wähle anderes k.")

    # 3) s = k^{-1}(h(m)+r d) mod n
    k_inv = inv_mod(k, n)
    s = (k_inv * ((hm + r * d) % n)) % n
    if s == 0:
        raise ValueError("s = 0. Wähle anderes k.")

    if verbose:
        print("Eingesetzt:")
        print(f"  R = {k}·P = {R}")
        print(f"  r = {R[0]} mod {n} = {r}")
        print(f"  k^{-1} mod n = {k}^(-1) mod {n} = {k_inv}")
        print(f"  h(m)+r·d = {hm} + {r}·{d} = {hm + r*d}")
        print(f"  (h(m)+r·d) mod n = {(hm + r*d) % n}")
        print(f"  s = {k_inv} · {((hm + r*d) % n)} mod {n} = {s}")
        print("============================================================\n")

    return r, s, R


# -------------------- ECDSA: VERIFIKATION --------------------
def ecdsa_verify(hm, r, s, P, Q, n, verbose=True):
    hm %= n
    r %= n
    s %= n

    if verbose:
        print("============================================================")
        print("ECDSA VERIFIKATION")
        print("============================================================")
        print("Schritte:")
        print("  1) u = h(m)·s^{-1} (mod n)")
        print("  2) v = r·s^{-1} (mod n)")
        print("  3) X = u·P + v·Q")
        print("  4) gültig falls r ≡ x_X (mod n)\n")

    if not (1 <= r <= n - 1 and 1 <= s <= n - 1):
        if verbose:
            print("Ungültig: r oder s nicht in [1, n-1].")
        return False, None, None, None

    s_inv = inv_mod(s, n)
    u = (hm * s_inv) % n
    v = (r * s_inv) % n

    uP = scalar_mult(u, P)
    vQ = scalar_mult(v, Q)
    X = ec_add(uP, vQ)

    if X is None:
        if verbose:
            print("X = O ⇒ ungültig.")
        return False, u, v, X

    xX = X[0] % n
    ok = (xX == r)

    if verbose:
        print("Eingesetzt:")
        print(f"  s^{-1} mod n = {s}^(-1) mod {n} = {s_inv}")
        print(f"  u = {hm}·{s_inv} mod {n} = {u}")
        print(f"  v = {r}·{s_inv} mod {n} = {v}")
        print(f"  uP = {uP}")
        print(f"  vQ = {vQ}")
        print(f"  X = uP + vQ = {X}")
        print(f"  x_X mod n = {X[0]} mod {n} = {xX}")
        print(f"  r mod n   = {r}")
        print("  ⇒", "GÜLTIG ✅" if ok else "UNGÜLTIG ❌")
        print("============================================================\n")

    return ok, u, v, X


# -------------------- NACHWEIS -------------------------------
def proof(hm, r, s, d, n, P, X, verbose=True):
    if not verbose or X is None:
        return

    hm %= n
    r %= n
    s %= n

    s_inv = inv_mod(s, n)
    k_from_sig = (((hm + r*d) % n) * s_inv) % n
    kP = scalar_mult(k_from_sig, P)

    print("============================================================")
    print("NACHWEIS DER FUNKTIONSWEISE")
    print("============================================================")
    print("uP + vQ")
    print("= (h(m)s^{-1})P + (rs^{-1})Q")
    print("= (h(m)s^{-1})P + (rs^{-1})·(dP)")
    print("= (h(m)s^{-1} + rs^{-1}d)P")
    print("= ((h(m)+rd)s^{-1})P  (mod n)\n")

    print("Zahlen einsetzen:")
    print(f"  (h(m)+r·d) mod n = ({hm} + {r}·{d}) mod {n} = {(hm + r*d) % n}")
    print(f"  s^{-1} mod n = {s}^(-1) mod {n} = {s_inv}")
    print(f"  k = (h(m)+r·d)·s^{-1} mod n = {k_from_sig}\n")

    print("Damit:")
    print("  uP+vQ = kP")
    print(f"  X   = {X}")
    print(f"  kP  = {kP}")
    print("  Vergleich kP==X ⇒", "JA ✅" if kP == X else "NEIN ❌")
    if kP is not None:
        print(f"  x(kP) mod n = {kP[0]} mod {n} = {kP[0] % n} (soll r sein)")
    print("============================================================\n")


# ======================= MAIN ===============================
if __name__ == "__main__":
    print("============================================================")
    print("UNIVERSAL ECDSA – Komplettrechnung")
    print("============================================================\n")

    if not is_on_curve(P):
        raise ValueError("P liegt NICHT auf der Kurve! Bitte P prüfen.")

    # n nur berechnen, wenn nicht vorgegeben
    if n is None:
        print("n ist nicht vorgegeben -> berechne ord(P) mit Hasse-Grenze ...")
        n = point_order(P)
        print(f"Gefunden: n = ord(P) = {n}\n")
    else:
        print(f"n ist vorgegeben: n = {n}\n")

    # Öffentlicher Schlüssel
    Q = scalar_mult(d, P)
    print("Öffentlicher Schlüssel:")
    print(f"  Q = d·P = {d}·P = {Q}\n")

    # Signatur
    r, s, R = ecdsa_sign(hm, d, k, P, n, verbose=verbose)
    print(f"Signatur: (r,s)=({r},{s})\n")

    # Verifikation
    ok, u, v, X = ecdsa_verify(hm, r, s, P, Q, n, verbose=verbose)

    # Nachweis
    proof(hm, r, s, d, n, P, X, verbose=verbose)

    print("FERTIG.")
