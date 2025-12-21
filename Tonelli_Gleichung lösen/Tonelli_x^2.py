# x^2 ≡ n (mod p)  with p an odd prime
p = 97
n = 27

print(f"Gesucht: x^2 ≡ {n} (mod {p})\n")

# 1) Legendre symbol test
ls = pow(n, (p - 1) // 2, p)
print("1) Legendre-Symbol:")
print(f"   {n}^({(p-1)//2}) mod {p} = {ls}")
if ls != 1:
    raise ValueError("n ist kein quadratischer Rest mod p (keine Lösung).")
print("   ⇒ quadratischer Rest\n")

# Special case p % 4 == 3
if p % 4 == 3:
    x = pow(n, (p + 1) // 4, p)
    print("p ≡ 3 (mod 4) ⇒ einfache Formel")
    print("Lösungen:", x, p - x)
    exit()

# 2) Factor p-1 = q * 2^s with q odd
q = p - 1
s = 0
while q % 2 == 0:
    q //= 2
    s += 1

print("2) Zerlegung:")
print(f"   p-1 = {p-1} = {q} * 2^{s}\n")

# 3) Find a quadratic non-residue z
z = 2
while pow(z, (p - 1) // 2, p) != p - 1:
    z += 1
print("3) Nichtquadratischer Rest:")
print(f"   z = {z}\n")

# 4) Tonelli–Shanks init
c = pow(z, q, p)
x = pow(n, (q + 1) // 2, p)
t = pow(n, q, p)
m = s

print("4) Initialisierung:")
print(f"   c = {c}, x = {x}, t = {t}, m = {m}\n")

# 5) Loop
while t != 1:
    # find smallest i (0 < i < m) s.t. t^(2^i) = 1
    i = 1
    t2i = (t * t) % p
    while i < m and t2i != 1:
        t2i = (t2i * t2i) % p
        i += 1

    # b = c^(2^(m-i-1))
    b = pow(c, 1 << (m - i - 1), p)
    x = (x * b) % p
    t = (t * b * b) % p
    c = (b * b) % p
    m = i

print("Ergebnis:")
print(f"   Lösungen: x ≡ {x} und x ≡ {p-x} (mod {p})")
print(f"   Kontrolle: {x}^2 mod {p} = {(x*x)%p}, {(p-x)}^2 mod {p} = {((p-x)*(p-x))%p}")
