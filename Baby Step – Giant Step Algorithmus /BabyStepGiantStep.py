"""
Baby-Step Giant-Step Algorithmus (BSGS)
---------------------------------------
Dieses Skript löst diskrete Logarithmus-Aufgaben der Form:

    g^x ≡ a (mod p)

Dabei gilt:
    - p: Primzahl (Modulus)
    - g: Basis (Erzeuger der Gruppe)
    - a: Zielwert
    - x: Gesuchte Zahl (diskreter Logarithmus)

Verwendung:
    1️⃣ Setze unten im Abschnitt "EINGABEPARAMETER" deine eigenen Werte ein.
    2️⃣ Führe das Skript aus.
    3️⃣ Das Ergebnis x wird ausgegeben.

Beispiel:
    g = 3, a = 57, p = 113  →  3^x ≡ 57 (mod 113)
"""

from math import ceil, sqrt

# ------------------------------------------------------------
# 🧮 Hilfsfunktion: Modularer Inverser (für Division in mod p)
# ------------------------------------------------------------
def modinv(a, m):
    """
    Berechnet das Inverse von a modulo m (Erweiterter euklidischer Algorithmus).
    Liefert ein u mit (a * u) % m == 1.
    """
    t, new_t = 0, 1
    r, new_r = m, a % m
    while new_r != 0:
        q = r // new_r
        t, new_t = new_t, t - q * new_t
        r, new_r = new_r, r - q * new_r
    if r != 1:
        raise ValueError(f"Kein Inverses für {a} mod {m} (ggT ≠ 1)")
    return t % m


# ------------------------------------------------------------
# ⚙️ Hauptfunktion: Baby-Step Giant-Step Algorithmus
# ------------------------------------------------------------
def bsgs(g, a, p):
    """
    Berechnet x mit g^x ≡ a (mod p).
    Gibt None zurück, falls keine Lösung existiert.
    """
    n = p - 1                # Ordnung der multiplikativen Gruppe mod p
    m = ceil(sqrt(n))        # Schrittgröße (√n)

    # -------------------
    # 👶 BABY-STEPS
    # -------------------
    # Berechne alle g^j für j = 0, 1, 2, ..., m-1
    table = {}
    val = 1
    for j in range(m):
        table.setdefault(val, j)   # speichere nur erstes Auftreten
        val = (val * g) % p

    # -------------------
    # 🧍 GIANT-STEPS
    # -------------------
    # Berechne (a * g^(-m*i)) und prüfe, ob es in Baby-Tabelle vorkommt
    gm = pow(g, m, p)
    inv_gm = modinv(gm, p)
    gamma = a % p

    for i in range(m):
        if gamma in table:
            j = table[gamma]
            return i * m + j       # x = i*m + j gefunden
        gamma = (gamma * inv_gm) % p

    # Keine Lösung gefunden
    return None


# ------------------------------------------------------------
# ✏️ EINGABEPARAMETER –> HIER ANPASSEN FÜR ANDERE AUFGABEN
# ------------------------------------------------------------
# Beispiel: Berechne x mit 3^x ≡ 57 (mod 113)
p = 113       # Modulus (muss prim sein)
g = 3         # Basis (Generator)
a = 57        # Zielwert (rechte Seite)

# ------------------------------------------------------------
# 🖥️ AUSFÜHRUNG UND AUSGABE
# ------------------------------------------------------------
x = bsgs(g, a, p)

if x is not None:
    print(f"Lösung gefunden: x = {x}")
    # Überprüfung
    check = pow(g, x, p)
    print(f"Überprüfung: {g}^{x} mod {p} = {check}")
else:
    print("❌ Keine Lösung gefunden.")
