import random
import math

def factorize(n: int):
    """Zerlegt n in Primfaktoren."""
    factors = []

    while n % 2 == 0:
        factors.append(2)
        n //= 2

    f = 3
    while f * f <= n:
        while n % f == 0:
            factors.append(f)
            n //= f
        f += 2

    if n > 1:
        factors.append(n)

    return factors


def my_is_probable_prime(n: int, t: int = 10) -> bool:
    """Verbesserter Fermat-Primzahltest mit ggT-Kriterium."""

    if n < 2:
        return False
    if n in (2, 3):
        return True
    if n % 2 == 0:
        return False

    for _ in range(t):
        a = random.randrange(2, n - 1)
        if math.gcd(a, n) != 1:
            return False
        if pow(a, n - 1, n) != 1:
            return False

    return True


# -------------------------
# Hauptprogramm (Konsole)
# -------------------------
if __name__ == "__main__":
    try:
        n = int(input("Gib eine ganze Zahl ein: "))
    except ValueError:
        print("❌ Ungültige Eingabe – bitte eine ganze Zahl eingeben.")
        exit(1)

    if my_is_probable_prime(n):
        print(f"✅ Ergebnis: {n} IST eine Primzahl.")
    else:
        print(f"❌ Ergebnis: {n} IST KEINE Primzahl.")
        factors = factorize(n)
        print(f"👉 Zerlegung: {n} = {' · '.join(map(str, factors))}")
