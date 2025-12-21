def egcd(a, b):
    if b == 0:
        return a, 1, 0
    g, x1, y1 = egcd(b, a % b)
    return g, y1, x1 - (a // b) * y1

def modinv(a, m):
    a %= m
    g, x, _ = egcd(a, m)
    if g != 1:
        return None
    return x % m

def solve_equation_verbose(a, b, c, x, y, z, m, result):
    print("Ausgangsgleichung:")
    print(f"  ({a}·{x} + {b}·{y} + {c}·z) mod {m} = {result}\n")

    ax = a * x
    by = b * y
    print("1) Bekannte Teile ausrechnen:")
    print(f"  {a}·{x} = {ax}")
    print(f"  {b}·{y} = {by}")
    print(f"  Summe = {ax} + {by} = {ax+by}\n")

    print("2) Nach z umstellen:")
    print("  Formel: z ≡ (result - (a·x + b·y)) · c^{-1}  (mod m)")
    rhs = (result - (ax + by)) % m
    print(f"  rhs = ({result} - ({ax+by})) mod {m}")
    print(f"      = ({result - (ax+by)}) mod {m} = {rhs}\n")

    c_mod = c % m
    print("3) c modulo m vereinfachen:")
    print(f"  {c} mod {m} = {c_mod}\n")

    inv = modinv(c, m)
    if inv is None:
        raise ValueError("Kein Inverses von c modulo m!")
    print("4) Inverses bestimmen:")
    print(f"  c^{-1} mod m = ({c_mod})^{-1} mod {m} = {inv}")
    print(f"  Kontrolle: {c_mod}·{inv} mod {m} = {(c_mod*inv)%m}\n")

    z_val = (rhs * inv) % m
    print("5) z berechnen:")
    print(f"  z = ({rhs}·{inv}) mod {m} = {z_val}\n")

    print("Kontrolle:")
    check = (a*x + b*y + c*z_val) % m
    print(f"  ({a}·{x} + {b}·{y} + {c}·{z_val}) mod {m} = {check}")
    print(f"  Soll = {result}\n")

    return z_val

# Beispiel
a, b, c = 12, 20, 30
x, y = 1, 3
m = 29
result = 5

z = solve_equation_verbose(a, b, c, x, y, None, m, result)
print("✔ Der fehlende Wert ist:", z)
