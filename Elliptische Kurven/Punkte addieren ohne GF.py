# ec_real.py
# Elliptische Kurve über den reellen Zahlen (mit rationalen Brüchen)

from fractions import Fraction
from typing import Optional, Tuple

Point = Optional[tuple[Fraction, Fraction]]  # None = Punkt im Unendlichen


class EllipticCurveReal:
    def __init__(self, a: int | float, b: int | float):
        """
        Kurve: y^2 = x^3 + a*x + b  über K = R
        a und b gibst du aus der Aufgabe an.
        """
        self.a = Fraction(a)
        self.b = Fraction(b)
        self.O: Point = None

    # ---------- Hilfsfunktionen ----------

    def to_fraction_point(self, P: tuple[float, float]) -> Point:
        """(x,y) mit Zahlen -> (Fraction, Fraction)."""
        if P is None:
            return None
        x, y = P
        return (Fraction(x), Fraction(y))

    def is_on_curve(self, P: Point) -> bool:
        """Prüfen, ob P auf der Kurve liegt."""
        if P is None:
            return True
        x, y = P
        return y * y == x**3 + self.a * x + self.b

    # ---------- Punktoperationen ----------

    def add(self, P: Point, Q: Point, verbose: bool = False) -> Point:
        """P + Q (mit Rechenschritten, wenn verbose=True)."""
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

        # Gegenpunkte -> O
        if x1 == x2 and y1 == -y2:
            if verbose:
                print("P und Q sind Gegenpunkte -> P + Q = O")
            return None

        # Steigung λ
        if P != Q:
            # Sekante
            num = y2 - y1
            den = x2 - x1
            lam = num / den
            if verbose:
                print("P != Q (Sekante):")
                print(f"  λ = (y2 - y1)/(x2 - x1) = ({y2} - {y1})/({x2} - {x1}) = {lam}")
        else:
            # Tangente
            num = 3 * x1 * x1 + self.a
            den = 2 * y1
            lam = num / den
            if verbose:
                print("P = Q (Tangente):")
                print(f"  λ = (3x1^2 + a)/(2y1) = (3*{x1}^2 + {self.a})/(2*{y1}) = {lam}")

        x3 = lam * lam - x1 - x2
        y3 = lam * (x1 - x3) - y1

        if verbose:
            print(f"  x3 = λ^2 - x1 - x2 = {lam}^2 - {x1} - {x2} = {x3}")
            print(f"  y3 = λ(x1 - x3) - y1 = {lam}*({x1} - {x3}) - {y1} = {y3}")
            print(f"--> P + Q = ({x3}, {y3})\n")

        return (x3, y3)

    def neg(self, P: Point) -> Point:
        """-P (Spiegelung an der x-Achse)."""
        if P is None:
            return None
        x, y = P
        return (x, -y)

    def scalar_mult(self, k: int, P: Point, verbose: bool = False) -> Point:
        """k*P mit dem üblichen Gruppen-Algorithmus (Double-and-Add)."""
        assert self.is_on_curve(P), "P liegt nicht auf der Kurve!"
        result: Point = None
        addend: Point = P

        if verbose:
            print(f"Berechne {k}*P für P = {P}:")

        bit_index = 0
        n = k
        while n > 0:
            if n & 1:
                if verbose:
                    print(f"  Bit {bit_index} von {k} ist 1 -> result = result + addend")
                    print(f"    result vorher: {result}")
                result = self.add(result, addend, verbose=verbose)
                if verbose:
                    print(f"    result nachher: {result}\n")

            n >>= 1
            bit_index += 1
            if n > 0:       # letztes Mal muss man die Verdopplung nicht ausgeben
                if verbose:
                    print("  Verdopple addend: addend = addend + addend")
                addend = self.add(addend, addend, verbose=verbose)

        if verbose:
            print(f"--> Ergebnis {k}*P = {result}\n")
        return result


# ---------- Beispiel: deine Aufgabe 1 (T) ----------

if __name__ == "__main__":
    # Kurve: y^2 = x^3 + 2x(a) + 9(b)  über R
    curve = EllipticCurveReal(a=2, b=9)

    # Punkte P(4, -9) und Q(0, -3)
    P = curve.to_fraction_point((4, -9))
    Q = curve.to_fraction_point((0, -3))

    print("Liegt P auf der Kurve?", curve.is_on_curve(P))
    print("Liegt Q auf der Kurve?", curve.is_on_curve(Q), "\n")

    # (b) P + Q und 2P exakt
    print("===== P + Q =====")
    PQ = curve.add(P, Q, verbose=True)

    print("===== 2P =====")
    twoP = curve.scalar_mult(2, P, verbose=True)

    # schöne Zusammenfassung mit Dezimalwerten
    def show_point(name: str, R: Point):
        if R is None:
            print(f"{name} = O (Punkt im Unendlichen)")
        else:
            x, y = R
            print(f"{name} = ({x}, {y}) ≈ ({float(x):.4f}, {float(y):.4f})")

    print("\nZusammenfassung:")
    show_point("P + Q", PQ)
    show_point("2P", twoP)
