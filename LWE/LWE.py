# ===== Universelles Skript für vereinfachte LWE-Aufgaben wie in deiner Lösung =====

def add_rows(matrix_rows):
    """Addiert mehrere Zeilen komponentenweise."""
    return [sum(col) for col in zip(*matrix_rows)]

def encode_bit(sum_row, rhs_sum, q, bit):
    """Codiert ein Bit: bei 0 nichts, bei 1 +q/2."""
    if bit == 1:
        rhs_sum = (rhs_sum + q // 2) % q
    return sum_row, rhs_sum

def plug_in_secret(sum_row, rhs, known_secret, unknown_index):
    """
    Setzt bekannte Geheimnisse ein und gibt eine Gleichung der Form:
        coeff * z ≈ rhs_mod
    zurück.
    """
    total_known = 0
    for i, s in known_secret.items():
        total_known += sum_row[i] * s
    total_known %= q

    coeff = sum_row[unknown_index] % q
    rhs_mod = (rhs - total_known) % q

    return coeff, rhs_mod

def all_z_that_decode_1(coeff, rhs_mod, q):
    """
    Liefert alle z in {0,...,q-1}, für die die Differenz näher bei q/2 als bei 0 liegt.
    Das ist GENAU dein handschriftliches Verfahren.
    """
    half = q // 2
    valid = []
    for z in range(q):
        val = (coeff * z) % q
        diff = (rhs_mod - val) % q
        # Bedingung: näher bei half als bei 0
        if abs(diff - half) < abs(diff - 0):
            valid.append(z)
    return valid


# ======= Beispiel: Aufgabe 5 ==========
if __name__ == "__main__":
    q = 29

    # Die 7 Zeilen aus der Aufgabe
    A = [
        [2, 1, 7],
        [5, 9, 6],
        [4, 4, 8],
        [1, 6, 9],
        [4, 3, 2],
        [7, 5, 8],
        [2, 4, 9],
    ]
    b = [5, 28, 20, 25, 22, 26, 22]

    # ===== (a) Bob kodiert 0-Bit mit den letzten 4 Zeilen =====
    last4 = A[3:]
    last4_rhs = b[3:]

    sum_row_a = add_rows(last4)
    rhs_sum_a = sum(last4_rhs) % q

    encoded_0 = encode_bit(sum_row_a, rhs_sum_a, q, bit=0)
    print("(a) Kodiertes 0-Bit:", encoded_0)

    # ===== (b) Buzz kodiert 1-Bit mit den ersten 4 Zeilen =====
    first4 = A[:4]
    first4_rhs = b[:4]

    sum_row_b = add_rows(first4)
    rhs_sum_b = sum(first4_rhs) % q

    encoded_1 = encode_bit(sum_row_b, rhs_sum_b, q, bit=1)
    print("(b) Kodiertes 1-Bit:", encoded_1)

    # ===== (c) x=1, y=3, z unbekannt =====
    known_secret = {0: 1, 1: 3}
    unknown_index = 2

    sum_row, rhs_val = encoded_1
    coeff, rhs_mod = plug_in_secret(sum_row, rhs_val, known_secret, unknown_index)

    print("\n(c) Gleichung ist:")
    print(f"{coeff} * z ≈ {rhs_mod}  (mod {q})")

    valid_z = all_z_that_decode_1(coeff, rhs_mod, q)
    print("\nAlle z, die näher bei 14 sind als bei 0:")
    print(valid_z)
