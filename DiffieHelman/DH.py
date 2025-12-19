"""
Diffie-Hellman Schlüsselaustausch - Universelles Skript
Berechnet den gemeinsamen Schlüssel basierend auf der elliptischen Kurve
oder modularer Arithmetik
"""


def gcd(a, b):
    """Berechnet den größten gemeinsamen Teiler"""
    while b:
        a, b = b, a % b
    return a


def mod_inverse(a, m):
    """Berechnet das modulare Inverse von a mod m"""
    if gcd(a, m) != 1:
        return None
    u1, u2, u3 = 1, 0, a
    v1, v2, v3 = 0, 1, m
    while v3 != 0:
        q = u3 // v3
        v1, v2, v3, u1, u2, u3 = (u1 - q * v1), (u2 - q * v2), (u3 - q * v3), v1, v2, v3
    return u1 % m


def point_add(P, Q, a, p):
    """Addiert zwei Punkte auf einer elliptischen Kurve E: y² = x³ + ax + b mod p"""
    if P is None:
        return Q
    if Q is None:
        return P

    x1, y1 = P
    x2, y2 = Q

    # Gleicher Punkt
    if x1 == x2:
        if y1 == y2:
            # Punktverdopplung
            s = ((3 * x1 ** 2 + a) * mod_inverse(2 * y1, p)) % p
        else:
            # P + (-P) = O (Punkt im Unendlichen)
            return None
    else:
        # Verschiedene Punkte
        s = ((y2 - y1) * mod_inverse((x2 - x1) % p, p)) % p

    x3 = (s ** 2 - x1 - x2) % p
    y3 = (s * (x1 - x3) - y1) % p

    return (x3, y3)


def point_multiply(k, P, a, p):
    """Multipliziert einen Punkt P mit einem Skalar k (k*P)"""
    if k == 0:
        return None

    result = None
    addend = P

    while k:
        if k & 1:
            result = point_add(result, addend, a, p)
        addend = point_add(addend, addend, a, p)
        k >>= 1

    return result


def verify_point_on_curve(P, a, b, p):
    """Überprüft, ob ein Punkt auf der Kurve liegt"""
    if P is None:
        return True
    x, y = P
    return (y ** 2) % p == (x ** 3 + a * x + b) % p


def find_discrete_log(target, P, a, p, max_k=None):
    """
    Findet k so dass k*P = target (Diskreter Logarithmus)
    Verwendet Brute-Force für kleine Werte

    Parameter:
    - target: Zielpunkt
    - P: Basispunkt
    - a: Kurvenparameter
    - p: Primzahl
    - max_k: Maximaler Wert für k (Standard: p)
    """
    if max_k is None:
        max_k = p

    current = None
    for k in range(max_k + 1):
        current = point_multiply(k, P, a, p)
        if current == target:
            return k
    return None


def reverse_diffie_hellman(P, a, b, p, known_k, shared_key, find_which='B'):
    """
    Berechnet den unbekannten privaten Schlüssel wenn der gemeinsame Schlüssel bekannt ist

    Parameter:
    - P: Basispunkt
    - a, b: Kurvenparameter
    - p: Primzahl
    - known_k: Bekannter privater Schlüssel (kA oder kB)
    - shared_key: Gemeinsamer Schlüssel
    - find_which: 'A' oder 'B' - welcher Schlüssel gesucht wird
    """
    print("=" * 60)
    print("REVERSE DIFFIE-HELLMAN (Privaten Schlüssel finden)")
    print("=" * 60)
    print(f"\nElliptische Kurve E: y² = x³ + {a}x + {b}")
    print(f"Primzahl p = {p}")
    print(f"Basispunkt P = {P}")
    print(f"Gemeinsamer Schlüssel = {shared_key}")

    if find_which == 'B':
        print(f"\nBekannt: kA = {known_k}")
        print("Gesucht: kB")

        # Berechne QA = kA * P
        QA = point_multiply(known_k, P, a, p)
        print(f"\nSchritt 1: Berechne QA = {known_k} * P = {QA}")

        # Gemeinsamer Schlüssel = kB * QA
        # Wir suchen kB so dass kB * QA = shared_key
        print(f"\nSchritt 2: Finde kB so dass kB * QA = {shared_key}")
        print("Teste verschiedene Werte für kB...")

        kB = find_discrete_log(shared_key, QA, a, p, max_k=p)

        if kB is not None:
            print(f"\n✓ Gefunden: kB = {kB}")
            # Verifizierung
            QB = point_multiply(kB, P, a, p)
            verify = point_multiply(known_k, QB, a, p)
            print(f"\nVerifizierung:")
            print(f"  QB = {kB} * P = {QB}")
            print(f"  kA * QB = {known_k} * {QB} = {verify}")
            if verify == shared_key:
                print(f"  ✓ Korrekt! Gemeinsamer Schlüssel stimmt überein.")
            return kB
        else:
            print(f"\n✗ Konnte kB nicht finden (möglicherweise > {p})")
            return None

    else:  # find_which == 'A'
        print(f"\nBekannt: kB = {known_k}")
        print("Gesucht: kA")

        # Berechne QB = kB * P
        QB = point_multiply(known_k, P, a, p)
        print(f"\nSchritt 1: Berechne QB = {known_k} * P = {QB}")

        # Gemeinsamer Schlüssel = kA * QB
        print(f"\nSchritt 2: Finde kA so dass kA * QB = {shared_key}")
        print("Teste verschiedene Werte für kA...")

        kA = find_discrete_log(shared_key, QB, a, p, max_k=p)

        if kA is not None:
            print(f"\n✓ Gefunden: kA = {kA}")
            # Verifizierung
            QA = point_multiply(kA, P, a, p)
            verify = point_multiply(known_k, QA, a, p)
            print(f"\nVerifizierung:")
            print(f"  QA = {kA} * P = {QA}")
            print(f"  kB * QA = {known_k} * {QA} = {verify}")
            if verify == shared_key:
                print(f"  ✓ Korrekt! Gemeinsamer Schlüssel stimmt überein.")
            return kA
        else:
            print(f"\n✗ Konnte kA nicht finden (möglicherweise > {p})")
            return None


def diffie_hellman_ec(P, a, b, p, kA, kB):
    """
    Berechnet den gemeinsamen Schlüssel für Diffie-Hellman auf elliptischen Kurven

    Parameter:
    - P: Basispunkt (Generator)
    - a, b: Kurvenparameter für E: y² = x³ + ax + b
    - p: Primzahl (Modulus)
    - kA: Privater Schlüssel von Alice
    - kB: Privater Schlüssel von Bob
    """
    print("=" * 60)
    print("DIFFIE-HELLMAN SCHLÜSSELAUSTAUSCH")
    print("=" * 60)
    print(f"\nElliptische Kurve E: y² = x³ + {a}x + {b}")
    print(f"Primzahl p = {p}")
    print(f"Basispunkt P = {P}")

    # Überprüfe ob P auf der Kurve liegt
    if not verify_point_on_curve(P, a, b, p):
        print("\nFEHLER: Punkt P liegt nicht auf der Kurve!")
        return None

    # Berechne die Ordnung des Punktes P
    print(f"\nÜberprüfe Ordnung von P...")
    order = 1
    current = P
    max_order = p + 1  # Sicherheitsgrenze
    while order < max_order:
        current = point_add(current, P, a, p)
        order += 1
        if current is None:
            break
        if current == P:
            break
    print(f"Ordnung von P: {order}")

    print("\n" + "-" * 60)
    print("ALICE's BERECHNUNGEN:")
    print("-" * 60)
    print(f"Privater Schlüssel: kA = {kA}")

    # Alice berechnet ihren öffentlichen Schlüssel
    QA = point_multiply(kA, P, a, p)
    print(f"Öffentlicher Schlüssel: QA = {kA}*P = {QA}")

    print("\n" + "-" * 60)
    print("BOB's BERECHNUNGEN:")
    print("-" * 60)
    print(f"Privater Schlüssel: kB = {kB}")

    # Bob berechnet seinen öffentlichen Schlüssel
    QB = point_multiply(kB, P, a, p)
    print(f"Öffentlicher Schlüssel: QB = {kB}*P = {QB}")

    print("\n" + "-" * 60)
    print("GEMEINSAMER SCHLÜSSEL:")
    print("-" * 60)

    # Alice berechnet den gemeinsamen Schlüssel
    shared_A = point_multiply(kA, QB, a, p)
    print(f"Alice berechnet: kA * QB = {kA} * {QB} = {shared_A}")

    # Bob berechnet den gemeinsamen Schlüssel
    shared_B = point_multiply(kB, QA, a, p)
    print(f"Bob berechnet:   kB * QA = {kB} * {QA} = {shared_B}")

    if shared_A == shared_B:
        print(f"\n✓ Gemeinsamer Schlüssel: {shared_A}")
        print("=" * 60)
        return shared_A
    else:
        print("\n✗ FEHLER: Schlüssel stimmen nicht überein!")
        return None


# Hauptprogramm
if __name__ == "__main__":
    # Gegebene Werte aus der Aufgabe
    a = 3
    b = 2
    p = 23  # GF(23)
    P = (0, 5)

    # ========================================
    # ÄNDERE HIER DEN MODUS:
    # MODE = 1  für normalen Diffie-Hellman
    # MODE = 2  für Reverse (privaten Schlüssel finden)
    # ========================================
    MODE = 2
    # ========================================

    if MODE == 1:
        print("\n" + "=" * 60)
        print("MODUS 1: NORMALER DIFFIE-HELLMAN")
        print("=" * 60)

        # Private Schlüssel
        kA = 3
        kB = 9

        # Berechne den gemeinsamen Schlüssel
        shared_key = diffie_hellman_ec(P, a, b, p, kA, kB)

        print("\n" + "=" * 60)
        print("ZUSAMMENFASSUNG:")
        print("=" * 60)
        print(f"Elliptische Kurve: y² = x³ + {a}x + {b} mod {p}")
        print(f"Basispunkt P: {P}")
        print(f"Private Schlüssel: kA = {kA}, kB = {kB}")
        print(f"Gemeinsamer Schlüssel: {shared_key}")
        print("=" * 60)

    elif MODE == 2:
        print("\n" + "=" * 60)
        print("MODUS 2: REVERSE - FINDE PRIVATEN SCHLÜSSEL")
        print("=" * 60)

        # ========================================
        # ÄNDERE HIER DEINE BEKANNTEN WERTE:
        # ========================================
        known_kA = 3  # Bekannter privater Schlüssel von Alice
        shared_key = (0, 18)  # Gegebener gemeinsamer Schlüssel (ersetze mit deinem Wert!)
        find_which = 'B'  # 'B' um kB zu finden, 'A' um kA zu finden
        # ========================================

        if find_which == 'B':
            unknown_k = reverse_diffie_hellman(P, a, b, p, known_kA, shared_key, find_which='B')
            if unknown_k:
                print("\n" + "=" * 60)
                print("ZUSAMMENFASSUNG:")
                print("=" * 60)
                print(f"Bekannt war: kA = {known_kA}")
                print(f"Gefundener privater Schlüssel: kB = {unknown_k}")
                print("=" * 60)
        else:
            known_kB = 9  # Bekannter privater Schlüssel von Bob
            unknown_k = reverse_diffie_hellman(P, a, b, p, known_kB, shared_key, find_which='A')
            if unknown_k:
                print("\n" + "=" * 60)
                print("ZUSAMMENFASSUNG:")
                print("=" * 60)
                print(f"Bekannt war: kB = {known_kB}")
                print(f"Gefundener privater Schlüssel: kA = {unknown_k}")
                print("=" * 60)

    else:
        print("FEHLER: Ungültiger Modus! Wähle MODE = 1 oder MODE = 2")