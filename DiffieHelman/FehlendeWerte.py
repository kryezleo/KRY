# Diffie-Hellman „Allround“-Skript (mit vollständigen Zwischenschritten)

VERBOSE = True   # <--- Zwischenschritte anzeigen (True/False)

def log(msg):
    if VERBOSE:
        print(msg)

def read_int_or_none(prompt):
    s = input(prompt).strip()
    if s == "":
        return None
    return int(s)


def discrete_log_bruteforce(g, value, p, max_exp=None):
    """
    Löse g^x ≡ value (mod p) per Bruteforce.
    Gibt Zwischenschritte aus.
    """
    if max_exp is None:
        max_exp = p - 1

    log(f"\n[Diskreter Logarithmus] Löse: {g}^x ≡ {value} (mod {p})")
    x_val = 1
    for k in range(0, max_exp + 1):
        if VERBOSE and k < 20:   # nur erste 20 Iterationen anzeigen
            log(f"  Teste k={k}: {g}^{k} mod {p} = {x_val}")
        if x_val == value:
            log(f"  ✔ Gefunden bei k={k}")
            return k
        x_val = (x_val * g) % p

    log("  ❌ Kein x gefunden (Bereich erschöpft)")
    return None


def egcd(a, b):
    """Erweiterter euklidischer Algorithmus (mit optionalen Zwischenschritten)."""
    if b == 0:
        return a, 1, 0
    g, x1, y1 = egcd(b, a % b)
    x = y1
    y = x1 - (a // b) * y1
    return g, x, y


def modinv(a, m):
    """Multiplikatives Inverses von a modulo m (zeigt Zwischenschritte)."""
    log(f"\n[ModInv] Berechne Inverses von {a} mod {m}")
    a_mod = a % m
    g, x, _ = egcd(a_mod, m)
    log(f"  gcd({a_mod}, {m}) = {g}")
    if g != 1:
        log("  ❌ Kein Inverses, da gcd != 1")
        return None
    inv = x % m
    log(f"  ✔ Inverses gefunden: {inv}, da {a_mod} * {inv} ≡ 1 (mod {m})")
    return inv


def main():
    print("=== Diffie-Hellman Rechner (mit Spezialfall K = g + Zwischenschritten) ===")
    print("Einfach Enter drücken, wenn ein Wert unbekannt ist.\n")

    p = read_int_or_none("p (Primzahl): ")
    g = read_int_or_none("g (Generator): ")

    a = read_int_or_none("a (geheimer Schlüssel von Alice): ")
    A = read_int_or_none("A = g^a mod p (öffentlicher Schlüssel von Alice): ")

    b = read_int_or_none("b (geheimer Schlüssel von Bob): ")
    B = read_int_or_none("B = g^b mod p (öffentlicher Schlüssel von Bob): ")

    K = read_int_or_none("K (gemeinsamer Schlüssel): ")

    want_K_eq_g = input("Soll der gemeinsame Schlüssel K gleich g sein? (j/n): ").strip().lower()
    K_eq_g = (want_K_eq_g == "j" or want_K_eq_g == "y")

    if p is None or g is None:
        print("\n❌ Du musst mindestens p und g eingeben.")
        return

    ord_g = p - 1

    changed = True
    while changed:
        changed = False

        # --- Spezialfall: K = g ---
        if K_eq_g:

            if a is not None and b is None:
                b = modinv(a, ord_g)
                if b is not None:
                    log(f"[Spezialfall] b = {b}")
                    changed = True

            if b is not None and a is None:
                a = modinv(b, ord_g)
                if a is not None:
                    log(f"[Spezialfall] a = {a}")
                    changed = True

            if a is not None and b is not None and K is None:
                K = g % p
                log(f"[Spezialfall] Setze K = g = {K}")
                changed = True

        # --- Normale DH-Berechnungen ---
        if a is not None and A is None:
            log(f"\n[Berechnung] A = g^a mod p")
            log(f"  = {g}^{a} mod {p}")
            A = pow(g, a, p)
            log(f"  = {A}")
            changed = True

        if A is not None and a is None:
            a = discrete_log_bruteforce(g, A, p)
            if a is not None:
                log(f"[Berechnung] a = {a}")
                changed = True

        if b is not None and B is None:
            log(f"\n[Berechnung] B = g^b mod p")
            log(f"  = {g}^{b} mod {p}")
            B = pow(g, b, p)
            log(f"  = {B}")
            changed = True

        if B is not None and b is None:
            b = discrete_log_bruteforce(g, B, p)
            if b is not None:
                log(f"[Berechnung] b = {b}")
                changed = True

        if K is None and a is not None and B is not None:
            log(f"\n[Berechnung] K = B^a mod p = {B}^{a} mod {p}")
            K = pow(B, a, p)
            log(f"  = {K}")
            changed = True

        if K is None and b is not None and A is not None:
            log(f"\n[Berechnung] K = A^b mod p = {A}^{b} mod {p}")
            K = pow(A, b, p)
            log(f"  = {K}")
            changed = True

    # --- Ergebnis ---
    print("\n============== Endergebnis ==============")
    print(f"p = {p}")
    print(f"g = {g}")
    print(f"a = {a}")
    print(f"A = {A}")
    print(f"b = {b}")
    print(f"B = {B}")
    print(f"K (gemeinsamer Schlüssel) = {K}")
    print("=========================================")


if __name__ == "__main__":
    main()
