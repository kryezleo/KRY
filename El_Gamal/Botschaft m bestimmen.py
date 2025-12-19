# ============================================================
# Aufgabe 4(c)
#
# (1 Punkt)
# Bestimmen Sie für das ElGamal-Kryptosystem mit öffentlichem
# Schlüssel (p, g, A) = (73, 20, 33) und privatem Schlüssel
# a = 29 die zum Chiffrat (B, c) = (65, 38) passende Botschaft m.
#
# ElGamal in Z_p^*:
#   B = g^k mod p
#   c = m · A^k mod p
# Entschlüsselung:
#   m = c · (B^a)^(-1) mod p
# ============================================================


# --- HIER ANPASSEN ---
p = 73
g = 20
A = 33
a = 29        # privater Schlüssel
B = 65        # Cipher-Komponente B = g^k
c = 38        # Cipher-Komponente c = m · A^k
# ---------------------


def elgamal_decrypt_verbose(p, g, A, a, B, c):
    print("Aufgabe 4(c) – ElGamal Entschlüsselung\n")

    print("Gegeben:")
    print(f"p = {p}, g = {g}, A = {A}")
    print(f"privater Schlüssel a = {a}")
    print(f"Chiffrat (B, c) = ({B}, {c})\n")

    print("🔹 Schritt 1: Shared Secret berechnen")
    print("s = B^a mod p")
    print(f"  = {B}^{a} mod {p}")
    s = pow(B, a, p)
    print(f"  = {s}\n")

    print("🔹 Schritt 2: Inverses von s")
    print("s^(-1) mod p")
    print(f"  = {s}^(-1) mod {p}")
    s_inv = pow(s, p - 2, p)
    print(f"  = {s_inv}\n")

    print("🔹 Schritt 3: Nachricht berechnen")
    print("m = c · s^(-1) mod p")
    print(f"  = {c} · {s_inv} mod {p}")
    m = (c * s_inv) % p
    print(f"  = {m}\n")

    print(f"✅ Entschlüsselte Nachricht: m = {m}")
    return m


if __name__ == "__main__":
    elgamal_decrypt_verbose(p, g, A, a, B, c)
