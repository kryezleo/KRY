# ============================================
# Aufgabe 4(b): Baby-Step-Giant-Step
# mit vollständiger Schritt-für-Schritt-Ausgabe
# ============================================

# --- HIER ANPASSEN ---
p = 73
g = 20
A = 52
# ---------------------

import math

def bsgs_verbose(p, g, A):
    print("Aufgabe 4(b) – Baby-Step-Giant-Step\n")

    print(f"Gegeben: p = {p}, g = {g}, A = {A}")
    print("Gesucht: a mit g^a ≡ A (mod p)\n")

    N = p - 1
    print(f"|Z_p^*| = p - 1 = {N}")

    m = math.isqrt(N) + 1
    print(f"m = ⌈√{N}⌉ = {m}\n")

    # Baby steps
    print("🔹 Baby-Steps: g^j mod p")
    baby = {}
    cur = 1
    for j in range(m):
        baby[cur] = j
        print(f"  j={j:2d}: g^{j} ≡ {cur} (mod {p})")
        cur = (cur * g) % p

    # Giant steps
    print("\n🔹 Giant-Steps:")
    g_inv = pow(g, p - 2, p)
    factor = pow(g_inv, m, p)
    print(f"g^(-1) ≡ {g_inv} (mod {p})")
    print(f"g^(-m) ≡ {factor} (mod {p})\n")

    gamma = A
    for i in range(m + 1):
        print(f"  i={i:2d}: A·(g^(-m))^{i} ≡ {gamma} (mod {p})")
        if gamma in baby:
            j = baby[gamma]
            a = i * m + j
            print(f"\n✅ Treffer!")
            print(f"{gamma} = g^{j}")
            print(f"a = i·m + j = {i}·{m} + {j} = {a}")
            print(f"Check: g^a mod p = {pow(g, a, p)}")
            return a
        gamma = (gamma * factor) % p

    print("❌ Kein a gefunden")
    return None

if __name__ == "__main__":
    bsgs_verbose(p, g, A)
