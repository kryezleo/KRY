# ============================================================
# Aufgabe 5(a)
# Rechenweg für: x^2 ≡ 57 (mod 61)
# ============================================================

p = 61
n = 57

print("Gesucht: x^2 ≡ 57 (mod 61)\n")

# 1) Legendre-Test
ls = pow(n, (p - 1) // 2, p)
print("1) Legendre-Symbol:")
print(f"   57^30 mod 61 = {ls}")
print("   ⇒ quadratischer Rest\n")

# 2) Fallprüfung
print("2) Fallprüfung:")
print(f"   61 ≡ {p % 4} (mod 4) ⇒ Tonelli–Shanks\n")

# 3) Zerlegung von p-1
p_minus_1 = p - 1
q = p_minus_1
s = 0
while q % 2 == 0:
    q //= 2
    s += 1

print("3) Zerlegung von p−1:")
print(f"   p−1 = {p_minus_1}")
print(f"       = {q} · 2^{s}")

# 🔹 zusätzliche Zerlegung von q
print(f"       = (3 · 5) · 2^{s}")
print(f"       = 2^{s} · 3 · 5")
print(f"   ⇒ q = {q} (ungerade), s = {s}\n")

# 4) Nichtquadratischer Rest
print("4) Suche Nicht-Quadratischen Rest z:")
print("   2^30 ≡ −1 (mod 61)")
print("   ⇒ z = 2\n")

# 5) Initialisierung
c = pow(2, q, p)
x = pow(n, (q + 1) // 2, p)
t = pow(n, q, p)
m = s

print("5) Initialisierung:")
print(f"   c = 2^{q} mod 61 = {c}")
print(f"   x = 57^{(q+1)//2} mod 61 = {x}")
print(f"   t = 57^{q} mod 61 = {t}")
print(f"   m = s = {m}\n")

# 6) Iteration
print("6) Iteration:")
print("   t = −1 ⇒ t² = 1 ⇒ i = 1")
b = c
x = (x * b) % p
t = (t * b * b) % p

print(f"   b = {b}")
print(f"   x = 22 · 11 mod 61 = {x}")
print("   t = 1 ⇒ Abbruch\n")

# 7) Ergebnis
print("7) Ergebnis:")
print(f"   Lösungen: x ≡ {x} und x ≡ {p-x} (mod 61)")
print(f"   Kontrolle: {x}² mod 61 = {(x*x)%p}, {(p-x)}² mod 61 = {((p-x)*(p-x))%p}")
