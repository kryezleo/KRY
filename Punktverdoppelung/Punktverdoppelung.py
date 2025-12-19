# ============================================================
# Universelles Skript für Rechnen auf elliptischen Kurven
# (Punktaddition, Punktverdopplung, k * P)
#
# Alles läuft über einem Primkörper F_p : 0,1,...,p-1
# ============================================================

# --------- 1. KURVENPARAMETER ANPASSEN ----------------------
# Hier stellst du deine Kurve ein:
#   E: y^2 = x^3 + a*x + b  (mod p)
#
# ==> Diese Werte änderst du für andere Aufgaben.
p = 49037          # Primzahl des Körpers
a = 11784            # "a" aus der Kurvengleichung
b = 29274          # "b" aus der Kurvengleichung

# Basispunkt P (Generator)
# ==> Diesen Punkt änderst du, wenn in der Aufgabe ein anderer Punkt gegeben ist.
Gx, Gy =11181, 14848  # P = (Gx, Gy)
G = (Gx, Gy)

# (optional) Ordnung des Punkts, falls bekannt
# z.B. n = 167 in deiner Aufgabe
n = 49363


# --------- 2. HILFSFUNKTIONEN -------------------------------

def inv_mod(x, p):
    """
    Modularer Inverser von x modulo p.
    Findet y mit x * y ≡ 1 (mod p).
    Voraussetzung: p ist prim, x != 0 (mod p).
    """
    return pow(x % p, p - 2, p)   # Fermat's little theorem


def ec_add(P, Q):
    """
    Addiert zwei Punkte P und Q auf der elliptischen Kurve.
    P, Q sind Tupel (x, y) oder None (für den Punkt im Unendlichen).
    Gibt R = P + Q zurück.
    """
    if P is None:
        return Q
    if Q is None:
        return P

    x1, y1 = P
    x2, y2 = Q

    # Fall: P == -Q  -> Ergebnis ist Punkt im Unendlichen
    if x1 == x2 and (y1 + y2) % p == 0:
        return None

    # Steigung lambda berechnen
    if P == Q:
        # Punktverdopplung: lambda = (3*x1^2 + a) / (2*y1)
        num = (3 * x1 * x1 + a) % p
        den = (2 * y1) % p
    else:
        # Punktaddition: lambda = (y2 - y1) / (x2 - x1)
        num = (y2 - y1) % p
        den = (x2 - x1) % p

    lam = (num * inv_mod(den, p)) % p

    # x3 = lambda^2 - x1 - x2
    x3 = (lam * lam - x1 - x2) % p
    # y3 = lambda * (x1 - x3) - y1
    y3 = (lam * (x1 - x3) - y1) % p

    return (x3, y3)


def scalar_mult(k, P):
    """
    Berechnet k * P mit der Double-and-Add Methode.
    k: ganzzahliger Skalar (z.B. geheimer Schlüssel)
    P: Punkt auf der Kurve (x, y) oder None
    """
    result = None      # Punkt im Unendlichen = neutrales Element
    addend = P

    # Solange noch Bits in k vorhanden sind
    while k > 0:
        # Wenn das niedrigste Bit 1 ist -> addiere aktuellen addend
        if k & 1:
            result = ec_add(result, addend)

        # Verdopple den Punkt für das nächste Bit
        addend = ec_add(addend, addend)

        # Schiebe k um ein Bit nach rechts
        k >>= 1

    return result


# --------- 3. BEISPIELE: TABELLE UND SCHLÜSSEL --------------

if __name__ == "__main__":
    print("Elliptische Kurve: y^2 = x^3 + {}x + {} (mod {})".format(a, b, p))
    print("Basispunkt P =", G)
    print()

    # Beispiel: Vielfache von P für k = 1,2,4,8,16,32
    print("Tabelle der Vielfachen von P (Double-and-Add):")
    for k in [1, 2, 4, 8, 16, 32]:
        kP = scalar_mult(k, G)
        print(f"{k:2d} * P = {kP}")
    print()

    # Beispiel: öffentlicher Schlüssel Q = d * P
    # ==> Hier d anpassen, wenn du einen anderen geheimen Schlüssel testen willst.
    d = 8249   # geheimer Schlüssel aus deiner Aufgabe
    Q = scalar_mult(d, G)
    print(f"Mit d = {d} ist der öffentliche Schlüssel Q = d*P = {Q}")

    # Beispiel: noch ein anderes k, z.B. k = 94 (Nonce für ECDSA)
    k = 17413
    kP = scalar_mult(k, G)
    print(f"{k} * P = {kP}")
