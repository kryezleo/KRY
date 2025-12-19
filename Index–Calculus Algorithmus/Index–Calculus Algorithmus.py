"""
Index–Calculus Algorithmus
--------------------------
Dieses Skript löst diskrete Logarithmen der Form

    g^x ≡ a (mod p)

mithilfe des Index–Calculus–Verfahrens.

⚙️ Voraussetzungen:
    - p ist eine Primzahl (z. B. p = 2027)
    - g ist eine Primitivwurzel mod p
    - a ist das Element, dessen Logarithmus gesucht wird
    - B ist die Schranke der Faktorbasis

💡 Vorgehen (vereinfacht):
    1️⃣ Faktorbasis F(B) = {Primzahlen ≤ B}
    2️⃣ Suche viele "B-glatte" Werte g^z mod p (nur Faktoren aus F(B))
    3️⃣ Bilde daraus ein lineares Gleichungssystem mod (p-1)
    4️⃣ Löse es → ergibt log_g(q) für alle q ∈ F(B)
    5️⃣ Berechne log_g(a) mithilfe dieser Werte

📘 Dieses Skript ist für Lernzwecke gedacht — nicht für große p!
"""

import math
from sympy import factorint, Matrix, mod_inverse, primerange

# ------------------------------------------------------------
# 🧮 Hilfsfunktionen
# ------------------------------------------------------------

def is_B_smooth(n, B):
    """Prüft, ob n vollständig aus Primfaktoren ≤ B besteht."""
    factors = factorint(n)
    return all(p <= B for p in factors.keys())

def modexp(base, exp, mod):
    """Berechnet (base^exp mod mod)."""
    return pow(base, exp, mod)


# ------------------------------------------------------------
# ⚙️ Hauptfunktion: Index–Calculus Algorithmus
# ------------------------------------------------------------
def index_calculus(p, g, a, B, num_relations=20):
    """
    Berechnet x mit g^x ≡ a (mod p) mithilfe des Index–Calculus Algorithmus.
    """
    print(f"\n=== Index–Calculus Algorithmus ===")
    print(f"Modulus p = {p}, Basis g = {g}, Zielwert a = {a}, Faktorbasisgrenze B = {B}")

    # 1️⃣ Faktorbasis aufbauen
    factor_base = list(primerange(2, B + 1))
    print(f"\nFaktorbasis F(B): {factor_base}")

    # 2️⃣ Relationen sammeln
    relations = []
    rhs = []  # rechte Seite (Exponenten z)
    z = 1
    while len(relations) < len(factor_base) and z < num_relations:
        val = modexp(g, z, p)
        if is_B_smooth(val, B):
            facs = factorint(val)
            row = [facs.get(q, 0) for q in factor_base]
            relations.append(row)
            rhs.append(z)
            print(f"Relation gefunden: g^{z} ≡ {val} = {facs}")
        z += 1

    if len(relations) < len(factor_base):
        print("\n❌ Nicht genug B-glatte Zahlen gefunden. Erhöhe num_relations oder B.")
        return None

    # 3️⃣ Gleichungssystem lösen (mod p-1)
    print("\nLöse lineares Gleichungssystem für log_g(q)...")
    M = Matrix(relations)
    rhs_vec = Matrix(rhs)
    mod = p - 1
    try:
        sol = list(M.inv_mod(mod) * rhs_vec % mod)
    except Exception as e:
        print("❌ Fehler beim Lösen des Systems:", e)
        return None

    log_q = dict(zip(factor_base, sol))
    print("\nBerechnete Logarithmen der Faktorbasis:")
    for q, xq in log_q.items():
        print(f"log_g({q}) = {xq}")

    # 4️⃣ Individuellen Logarithmus berechnen
    print("\nSuche y, sodass a*g^y B-glatt ist...")
    for y in range(1, p):
        val = (a * modexp(g, y, p)) % p
        if is_B_smooth(val, B):
            facs = factorint(val)
            exps = sum(log_q[q] * e for q, e in facs.items() if q in log_q)
            x = (exps - y) % (p - 1)
            print(f"\n✅ Gefunden: a*g^{y} ≡ {val} = {facs}")
            print(f"→ Diskreter Logarithmus x = {x}")
            return x

    print("\n❌ Kein y gefunden, für das a*g^y B-glatt ist.")
    return None


# ------------------------------------------------------------
# ✏️ EINGABEPARAMETER —> HIER ANPASSEN FÜR ANDERE AUFGABEN
# ------------------------------------------------------------
p = 2027      # Primzahl (Modulus)
g = 2         # Basis (Primitivwurzel mod p)
a = 13        # Zielwert: g^x ≡ a (mod p)
B = 11        # Schranke für Faktorbasis (Primzahlen ≤ B)
num_relations = 100  # max. Anzahl getesteter Relationen

# ------------------------------------------------------------
# 🖥️ AUSFÜHRUNG
# ------------------------------------------------------------
index_calculus(p, g, a, B, num_relations)
