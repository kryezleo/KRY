def modinv(a, m):
    """ Berechnet das multiplikative Inverse von a modulo m. """
    a %= m
    for x in range(m):
        if (a * x) % m == 1:
            return x
    return None


def solve_equation(a, b, c, x, y, z, m, result):
    """
    Löst (a*x + b*y + c*z) mod m = result

    Genau EINE Variable (a,b,c,x,y,z) muss None sein.
    """

    # Prüfen, dass genau ein Wert None ist
    params = [a, b, c, x, y, z]
    if params.count(None) != 1:
        raise ValueError("❌ Es muss GENAU EIN Wert None sein!")

    # ------- a berechnen -------
    if a is None:
        rhs = (result - (b * y + c * z)) % m
        inv = modinv(x, m)
        if inv is None:
            raise ValueError("❌ x hat kein Inverses mod m!")
        return (rhs * inv) % m

    # ------- b berechnen -------
    if b is None:
        rhs = (result - (a * x + c * z)) % m
        inv = modinv(y, m)
        if inv is None:
            raise ValueError("❌ y hat kein Inverses mod m!")
        return (rhs * inv) % m

    # ------- c berechnen -------
    if c is None:
        rhs = (result - (a * x + b * y)) % m
        inv = modinv(z, m)
        if inv is None:
            raise ValueError("❌ z hat kein Inverses mod m!")
        return (rhs * inv) % m

    # ------- x berechnen -------
    if x is None:
        rhs = (result - (b * y + c * z)) % m
        inv = modinv(a, m)
        if inv is None:
            raise ValueError("❌ a hat kein Inverses mod m!")
        return (rhs * inv) % m

    # ------- y berechnen -------
    if y is None:
        rhs = (result - (a * x + c * z)) % m
        inv = modinv(b, m)
        if inv is None:
            raise ValueError("❌ b hat kein Inverses mod m!")
        return (rhs * inv) % m

    # ------- z berechnen -------
    if z is None:
        rhs = (result - (a * x + b * y)) % m
        inv = modinv(c, m)
        if inv is None:
            raise ValueError("❌ c hat kein Inverses mod m!")
        return (rhs * inv) % m

    # -------- Falls nichts fehlt: einfach ausrechnen -------
    return (a * x + b * y + c * z) % m


# ============================
#   HIER GIBST DU DEINE WERTE EIN
# ============================

a = None # <--- DIESE Variable wird ausgerechnet!
b = 20
c = 30

x = 1
y = 3
z = 20  # <--- DIESE Variable wird ausgerechnet!

m = 29
result = 5

# ============================
#       AUTOMATISCH STARTEN
# ============================

solution = solve_equation(a, b, c, x, y, z, m, result)
print("\n✔ Der fehlende Wert ist:", solution)
