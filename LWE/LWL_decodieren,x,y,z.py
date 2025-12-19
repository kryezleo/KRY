def modinv(a, m):
    # modular inverse of a mod m
    a = a % m
    for x in range(m):
        if (a * x) % m == 1:
            return x
    return None

def solve_equation(a, b, c, x, y, z, m, result):
    """
    Löst (a*x + b*y + c*z) mod m = result
    Ein Wert von x, y oder z darf None sein (unbekannt).
    """

    # Falls z unbekannt ist
    if z is None:
        # z = (result - (a*x + b*y)) * inverse(c)  mod m
        rhs = (result - (a*x + b*y)) % m
        inv = modinv(c, m)
        if inv is None:
            raise ValueError("Kein Inverses von c modulo m!")
        z = (rhs * inv) % m
        return z

    # Falls x unbekannt ist
    if x is None:
        rhs = (result - (b*y + c*z)) % m
        inv = modinv(a, m)
        if inv is None:
            raise ValueError("Kein Inverses von a modulo m!")
        x = (rhs * inv) % m
        return x

    # Falls y unbekannt ist
    if y is None:
        rhs = (result - (a*x + c*z)) % m
        inv = modinv(b, m)
        if inv is None:
            raise ValueError("Kein Inverses von b modulo m!")
        y = (rhs * inv) % m
        return y

    # Falls alles bekannt ist → einfach ausrechnen
    return (a*x + b*y + c*z) % m


# ============================
# Beispiel: Leona will z ausrechnen
# ============================

# Beispielgleichung:
# (12*1 + 20*3 + 30*z) mod 29 = 5

a, b, c = 12, 20, 30
x, y = 1, 3
z = None     # Das soll berechnet werden
m = 29
result = 5
# ============================
solution = solve_equation(a, b, c, x, y, z, m, result)
print("\n✔ Der fehlende Wert ist:", solution)