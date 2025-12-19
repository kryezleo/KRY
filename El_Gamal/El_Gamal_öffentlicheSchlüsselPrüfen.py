# ============================================
# Aufgabe (a): ElGamal Public-Key Check
# mit vollständiger Schritt-für-Schritt-Ausgabe
# ============================================

# --- HIER ANPASSEN ---
p = 137
g = 42
A = 107
# ---------------------

def factorize(n):
    factors = {}
    d = 2
    while d * d <= n:
        while n % d == 0:
            factors[d] = factors.get(d, 0) + 1
            n //= d
        d += 1
    if n > 1:
        factors[n] = factors.get(n, 0) + 1
    return factors


print("Gegeben:")
print(f"p = {p}")
print(f"g = {g}")
print(f"A = {A}")
print()

# 1️⃣ p prim?
print("1) Prüfe, ob p prim ist:")
if all(p % i != 0 for i in range(2, int(p**0.5) + 1)):
    print(f"   p = {p} ist prim ✅")
else:
    print(f"   p = {p} ist NICHT prim ❌")
    raise SystemExit

# 2️⃣ Gruppenordnung
print("\n2) Bestimme die Gruppenordnung:")
order = p - 1
print(f"   |Z_p*| = p - 1 = {p} - 1 = {order}")

fac = factorize(order)
fac_str = " · ".join(f"{k}^{v}" if v > 1 else str(k) for k, v in fac.items())
print(f"   {order} = {fac_str}")

# 3️⃣ Generator-Test
print("\n3) Prüfe, ob g erzeugend ist:")
is_generator = True

for q in fac:
    exp = order // q
    val = pow(g, exp, p)
    print(f"   g^({order}/{q}) mod p = {g}^{exp} mod {p} = {val}", end="")
    if val == 1:
        print("  ⇒ 1 ❌")
        is_generator = False
    else:
        print("  ⇒ ≠ 1 ✅")

if is_generator:
    print("\n⇒ g = 42 ist erzeugend!")
else:
    print("\n⇒ g ist NICHT erzeugend!")

# 4️⃣ Prüfe A
print("\n4) Prüfe A:")
if A % p != 0:
    print(f"   A = {A} ≠ 0 (mod {p}) ✅")
else:
    print(f"   A = {A} ≡ 0 (mod {p}) ❌")

# 5️⃣ Fazit
print("\nFazit:")
if is_generator and A % p != 0:
    print(f"(p, g, A) = ({p}, {g}, {A}) ist geeignet als öffentlicher ElGamal-Schlüssel ✅")
else:
    print(f"(p, g, A) = ({p}, {g}, {A}) ist NICHT geeignet ❌")
