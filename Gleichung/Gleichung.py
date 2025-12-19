from math import gcd

# ======================================================
# ✅ HIER ANPASSEN!
# Trage hier deine Werte ein:
a = 78   # der Koeffizient vor x  → von Aufgabe: 78x = 246 (mod 264)
b = 246  # rechter Wert
m = 264  # Modulus
# ======================================================


# --- Funktion: löst lineare Kongruenz a·x ≡ b (mod m) ---
def solve_congruence(a, b, m):
    d = gcd(a, m)

    # Prüfen ob eine Lösung existiert
    if b % d != 0:
        print("❌ Keine Lösung, da gcd(a, m) b nicht teilt.")
        return []

    # Gleichung kürzen
    a_reduced = a // d
    b_reduced = b // d
    m_reduced = m // d

    # modular inverses: a_reduced * x ≡ b_reduced (mod m_reduced)
    # pow(a_reduced, -1, m_reduced) berechnet das multiplikative Inverse
    x0 = (b_reduced * pow(a_reduced, -1, m_reduced)) % m_reduced

    # Alle Lösungen erzeugen
    solutions = [(x0 + k * m_reduced) % m for k in range(d)]
    return sorted(solutions)


# --- Ausgabe ---
solutions = solve_congruence(a, b, m)
print(f"Lösungen von {a}x ≡ {b} (mod {m}): {solutions}")
