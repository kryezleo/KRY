def ist_primzahl(n):
    """Prüft ob n eine Primzahl ist"""
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    for i in range(3, int(n ** 0.5) + 1, 2):
        if n % i == 0:
            return False
    return True


def primfaktoren(n):
    """Gibt die Liste der eindeutigen Primfaktoren zurück"""
    faktoren = []
    d = 2
    temp_n = n
    while d * d <= temp_n:
        if temp_n % d == 0:
            faktoren.append(d)
            while temp_n % d == 0:
                temp_n //= d
        d += 1
    if temp_n > 1:
        faktoren.append(temp_n)
    return faktoren


def ist_quadratfrei(n, faktoren):
    """Prüft ob n quadratfrei ist (kein Primfaktor kommt mehrfach vor)"""
    for p in faktoren:
        if n % (p * p) == 0:
            return False
    return True


def ist_carmichael_zahl_mit_begruendung(n):
    """Prüft ob n eine Carmichael-Zahl ist und gibt Begründung zurück"""
    # Carmichael-Zahlen müssen zusammengesetzt sein
    if n < 2:
        return False, f"{n} ist kleiner als 2"

    if ist_primzahl(n):
        return False, f"{n} ist eine Primzahl (muss zusammengesetzt sein)"

    # Primfaktoren bestimmen
    faktoren = primfaktoren(n)

    # Mindestens 3 verschiedene Primfaktoren
    if len(faktoren) < 3:
        return False, f"{n} hat nur {len(faktoren)} Primfaktor(en): {faktoren} (benötigt mindestens 3)"

    # Muss quadratfrei sein
    if not ist_quadratfrei(n, faktoren):
        return False, f"{n} ist nicht quadratfrei (ein Primfaktor kommt mehrfach vor)"

    # Für jeden Primfaktor p muss gelten: (p-1) teilt (n-1)
    for p in faktoren:
        if (n - 1) % (p - 1) != 0:
            return False, f"Für Primfaktor {p} gilt nicht: ({p}-1) teilt ({n}-1)"

    return True, f"{n} erfüllt alle Kriterien: Primfaktoren {faktoren}, quadratfrei, (p-1) teilt (n-1) für alle p"


# Beispiel-Verwendung
if __name__ == "__main__":
    # Teste einige bekannte Carmichael-Zahlen
    test_zahlen = [561, 1105, 1729, 2465, 2821, 6601, 8911, 560, 1000]

    for n in test_zahlen:
        ist_carmichael, begruendung = ist_carmichael_zahl_mit_begruendung(n)
        if ist_carmichael:
            print(f"✓ {n} ist eine Carmichael-Zahl")
            print(f"  → {begruendung}")
        else:
            print(f"✗ {n} ist keine Carmichael-Zahl")
            print(f"  → {begruendung}")
        print()

    # Eigene Zahl testen
    print("--- Eigene Zahl testen ---")
    zahl = int(input("Gib eine Zahl ein: "))
    ist_carmichael, begruendung = ist_carmichael_zahl_mit_begruendung(zahl)
    if ist_carmichael:
        print(f"\n✓ {zahl} ist eine Carmichael-Zahl")
    else:
        print(f"\n✗ {zahl} ist keine Carmichael-Zahl")
    print(f"Begründung: {begruendung}")
