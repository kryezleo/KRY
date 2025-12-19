# Pollard's ρ (Floyd) – universelles Skript
# -------------------------------------------------------------
# HIER ANPASSEN:
n = 1501  # <- Zu faktorierende Zahl (ändern)
x0 = 1  # <- Startwert x0 (ändern)
a = 13  # <- f(x) = x^2 + a (ändern) modulo n ist integriert
max_iters = 10000  # <- Sicherheitslimit Iterationen (ändern)
verbose = True  # <- True = Zwischenschritte mitdrucken


# -------------------------------------------------------------
# Optional: eigene Iterationsfunktion f(x) definieren
# Standard ist f(x) = x^2 + a (mod n). Du kannst sie ersetzen.
def f(x, n=n, a=a):
    return (x * x + a) % n


# -------------------------------------------------------------
# GCD (kann auch math.gcd sein, hier explizit implementiert)
def gcd(a, b):
    while b:
        a, b = b, a % b
    return abs(a)


# -------------------------------------------------------------
# Pollard ρ mit Floyds Zyklus-Findung
def pollards_rho(n, x0=2, a=1, max_iters=10000, verbose=False):
    if n % 2 == 0:
        return 2

    x = x0
    y = x0
    d = 1
    it = 0

    while d == 1 and it < max_iters:
        x = f(x, n, a)  # Schrittweite 1
        y = f(f(y, n, a), n, a)  # Schrittweite 2 (Floyd: "Hase")
        d = gcd(abs(x - y), n)
        it += 1

        if verbose:
            print(f"{it:4d}: f(x)={x:6d}, f(f(y))={y:6d}, gcd(|x-y|,n) ={d}")

    if d == n or d == 1:
        return None  # kein Faktor gefunden (Parameter ändern/neu starten)
    return d


# -------------------------------------------------------------
# Läuft als Skript:
if __name__ == "__main__":
    factor = pollards_rho(n=n, x0=x0, a=a, max_iters=max_iters, verbose=verbose)
    if factor is None:
        print("\nKein Faktor gefunden. Versuche andere Parameter (x0, a) oder mehr Iterationen.")
    else:
        other = n // factor
        print(f"\nGefundener Faktor: {factor}")
        print(f"Anderer Faktor   : {other}")
        print(f"Prüfung          : {factor} * {other} = {factor * other}")
