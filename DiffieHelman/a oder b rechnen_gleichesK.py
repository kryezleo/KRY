# Eingaben
p = 467                 # sichere Primzahl
g = 464                 # Beispiel-Erzeuger (optional, für K irrelevant)
unknown = "b"           # "a" oder "b": welches möchtest du berechnen?
known_value = 99        # der bekannte Wert (a oder b)

# Erweiterter euklidischer Algorithmus MIT Zwischenschritten
def extended_euclid(a, b):
    print(f"Starte erweiterten euklidischen Algorithmus für a={a}, b={b}\n")

    old_r, r = a, b
    old_s, s = 1, 0
    old_t, t = 0, 1

    step = 0
    while r != 0:
        q = old_r // r

        print(f"Schritt {step}:")
        print(f"  Quotient q = {q}")
        print(f"  Vorher:")
        print(f"    old_r={old_r}, r={r}")
        print(f"    old_s={old_s}, s={s}")
        print(f"    old_t={old_t}, t={t}")

        # Update-Regeln (damit man sieht, wie gerechnet wird)
        print(f"  Update:")
        print(f"    new_r  = old_r - q*r  = {old_r} - {q}*{r} = {old_r - q*r}")
        print(f"    new_s  = old_s - q*s  = {old_s} - {q}*{s} = {old_s - q*s}")
        print(f"    new_t  = old_t - q*t  = {old_t} - {q}*{t} = {old_t - q*t}\n")

        old_r, r = r, old_r - q * r
        old_s, s = s, old_s - q * s
        old_t, t = t, old_t - q * t

        step += 1

    print("Algorithmus beendet.\n")
    print(f"ggT = {old_r}")
    print(f"Koeffizienten: s = {old_s}, t = {old_t}\n")

    return old_r, old_s, old_t


# Ordnung der Gruppe Z*_p ist p-1
modulus = p - 1
print(f"Modulus (p-1) = {modulus}\n")

# Berechne modulare Inverse mit Zwischenschritten
gcd, s, t = extended_euclid(known_value, modulus)

# Zusätzliche Erklärung, wie man auf s,t und b kommt
print("Nachweis (Bézout-Gleichung):")
print(f"  {known_value}*({s}) + {modulus}*({t}) = {known_value*s + modulus*t}")
print(f"  => ggT({known_value}, {modulus}) = {gcd}\n")

print("In Pari GP: lift(Mod(99, 466)^(-1)): 466 = p-1 / 99 = a oder b\n")

if gcd != 1:
    raise ValueError("Keine Inverse vorhanden (ggT != 1)!")

# s ist die Inverse modulo modulus (aber evtl. negativ -> mod nehmen)
inverse = s % modulus

print("Modulo-Schritt:")
print(f"  {known_value}*{s} ≡ 1 (mod {modulus})")
print(f"  Inverse = s mod {modulus} = {s} mod {modulus} = {inverse}\n")

# Optionaler Check
check = (known_value * inverse) % modulus
print("Check:")
print(f"  ({known_value} * {inverse}) mod {modulus} = {check}\n")

if unknown == "b":
    print(f"Ergebnis: b = {inverse}")
else:
    print(f"Ergebnis: a = {inverse}")
