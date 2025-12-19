# elliptic_elgamal.py
# Kleines Hilfsskript für EC-ElGamal-Aufgaben über GF(p)

from typing import Optional, Tuple

Point = Optional[tuple[int, int]]  # (x, y) oder None für Punkt im Unendlichen


class EllipticCurve:
    def __init__(self, p: int, a: int, b: int):
        """
        Kurve: y^2 = x^3 + a*x + b   (mod p)
        """
        self.p = p
        self.a = a
        self.b = b
        self.O: Point = None  # Punkt im Unendlichen

    # ---------- Grundfunktionen ----------

    def inv_mod(self, k: int) -> int:
        """Multiplikatives Inverses von k modulo p."""
        return pow(k, -1, self.p)

    def is_on_curve(self, P: Point) -> bool:
        """Prüfen, ob Punkt auf der Kurve liegt."""
        if P is None:
            return True
        x, y = P
        return (y * y - (x ** 3 + self.a * x + self.b)) % self.p == 0

    def add(self, P: Point, Q: Point, verbose: bool = False) -> Point:
        """P + Q auf der elliptischen Kurve."""
        p = self.p
        if P is None:
            if verbose:
                print("P = O, also P + Q = Q =", Q)
            return Q
        if Q is None:
            if verbose:
                print("Q = O, also P + Q = P =", P)
            return P

        x1, y1 = P
        x2, y2 = Q

        # P und Q sind Gegenpunkte
        if x1 == x2 and (y1 + y2) % p == 0:
            if verbose:
                print("P und Q sind Gegenpunkte, also P + Q = O")
            return None

        # Steigung λ
        if P != Q:
            num = (y2 - y1) % p
            den = (x2 - x1) % p
            lamb = (num * self.inv_mod(den)) % p
            if verbose:
                print(f"λ = (y2 - y1)/(x2 - x1) = ({y2}-{y1})/({x2}-{x1}) mod {p} = {lamb}")
        else:  # Tangente (P = Q)
            num = (3 * x1 * x1 + self.a) % p
            den = (2 * y1) % p
            lamb = (num * self.inv_mod(den)) % p
            if verbose:
                print(f"λ = (3x1^2 + a)/(2y1) = (3*{x1}^2 + {self.a})/(2*{y1}) mod {p} = {lamb}")

        x3 = (lamb * lamb - x1 - x2) % p
        y3 = (lamb * (x1 - x3) - y1) % p

        if verbose:
            print(f"x3 = λ^2 - x1 - x2 = {x3} (mod {p})")
            print(f"y3 = λ(x1 - x3) - y1 = {y3} (mod {p})")
            print(f"Ergebnis P + Q = ({x3}, {y3})\n")

        return (x3, y3)

    def neg(self, P: Point) -> Point:
        """Additiv inverser Punkt -P."""
        if P is None:
            return None
        x, y = P
        return (x, (-y) % self.p)

    def sub(self, P: Point, Q: Point, verbose: bool = False) -> Point:
        """P - Q = P + (-Q)."""
        return self.add(P, self.neg(Q), verbose=verbose)

    def scalar_mult(self, k: int, P: Point, verbose: bool = False) -> Point:
        """k * P mit Double-and-Add."""
        assert self.is_on_curve(P), "P liegt nicht auf der Kurve!"
        result: Point = None  # startet bei O
        addend: Point = P
        bit_index = 0

        if verbose:
            print(f"Berechne {k} * {P} mit Double-and-Add:")

        while k > 0:
            if k & 1:
                if verbose:
                    print(f"  Bit {bit_index} ist 1 -> result = result + addend")
                    print(f"    result vorher: {result}")
                result = self.add(result, addend, verbose=verbose)
                if verbose:
                    print(f"    result nachher: {result}\n")

            # nächstes Bit
            if k > 1:  # letzter Durchgang braucht die Verdopplung nicht unbedingt im Detail
                if verbose:
                    print(f"  Verdoppele addend: addend = addend + addend")
                addend = self.add(addend, addend, verbose=verbose)
            else:
                addend = self.add(addend, addend)
            k >>= 1
            bit_index += 1

        if verbose:
            print(f"Ergebnis: {result}\n")
        return result

    def order(self, P: Point) -> int:
        """Ordnung von P bestimmen (nur für kleine Kurven sinnvoll)."""
        assert self.is_on_curve(P), "P liegt nicht auf der Kurve!"
        Q: Point = None
        n = 0
        while True:
            n += 1
            Q = self.add(Q, P)
            if Q is None:
                return n


# ---------- El-Gamal auf elliptischen Kurven ----------

def elgamal_encrypt(curve: EllipticCurve,
                    P: Point,
                    M: Point,
                    kA: int,
                    kB: int,
                    verbose: bool = True):
    """
    Verschlüsselung aus Aufgaben-Typ:
    - P: Generator
    - kB: geheimer Schlüssel von Bob
    - kA: "Ephemeralschlüssel" von Alice (in den Aufgaben meist gegeben)
    - M: Klartext-Punkt

    Es wird angenommen:
      Q_B = kB * P
      C1  = kA * P
      S   = kA * Q_B
      C2  = M + S
    """
    if verbose:
        print("=== Schlüsselerzeugung von Bob ===")
    QB = curve.scalar_mult(kB, P, verbose=verbose)
    if verbose:
        print(f"Bob's öffentlicher Schlüssel: Q_B = {QB}\n")

    if verbose:
        print("=== Verschlüsselung durch Alice ===")
        print(f"Ich verwende k_A = {kA} als Ephemeralschlüssel.\n")

        print("1) C1 = k_A * P:")
    C1 = curve.scalar_mult(kA, P, verbose=verbose)

    if verbose:
        print("2) S = k_A * Q_B (geteiltes Geheimnis):")
    S = curve.scalar_mult(kA, QB, verbose=verbose)

    if verbose:
        print(f"3) C2 = M + S = {M} + {S}:")
    C2 = curve.add(M, S, verbose=verbose)

    if verbose:
        print(f"--> Chiffrat: (C1, C2) = ({C1}, {C2})\n")

    return QB, C1, C2


def elgamal_decrypt(curve: EllipticCurve,
                    C1: Point,
                    C2: Point,
                    kB: int,
                    verbose: bool = True) -> Point:
    """
    Entschlüsselung:
      S = kB * C1
      M = C2 - S
    """
    if verbose:
        print("=== Entschlüsselung durch Bob ===")
        print(f"1) S = k_B * C1 mit k_B = {kB}, C1 = {C1}:")
    S = curve.scalar_mult(kB, C1, verbose=verbose)

    if verbose:
        print(f"2) Klartext M = C2 - S = {C2} - {S}:")
    M = curve.sub(C2, S, verbose=verbose)

    if verbose:
        print(f"--> Entschlüsselter Punkt M = {M}\n")
    return M


# ---------- Beispiel: Aufgabe 3 aus deinem Screenshot ----------

if __name__ == "__main__":
    # Kurve: y^2 = x^3 + 2x(a) + 5(b) über GF(13)(p)
    curve = EllipticCurve(p=11, a=3, b=9)

    # Generator-Punkt
    P: Point = (2, 1)

    # Geheimschlüssel / Nachricht aus der Aufgabe
    kA = 7  # Alice
    kB = 3  # Bob
    M: Point = (10, 4)

    print("=== Check: Punkt und Ordnung ===")
    print("Liegt P auf der Kurve?", curve.is_on_curve(P))
    print("Ordnung von P:", curve.order(P), "\n")

    # Verschlüsselung
    QB, C1, C2 = elgamal_encrypt(curve, P, M, kA, kB, verbose=True)

    # Entschlüsselung
    M_rec = elgamal_decrypt(curve, C1, C2, kB, verbose=True)

    print("Zusammenfassung:")
    print("  Q_B =", QB)
    print("  C1  =", C1)
    print("  C2  =", C2)
    print("  entschlüsseltes M =", M_rec)
