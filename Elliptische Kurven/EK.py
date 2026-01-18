#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Universelles Elliptische-Kurven-Skript über GF(p) (p prim)
inkl. Zwischenschritte, Formeln und schöner Ausgabe.

Aufgaben-Typ:
E: y^2 = x^3 + a x + b  über GF(p)

Kann:
(a) Tabelle s_x = x^3 + a x + b (mod p)
(b) Quadratische Reste + Wurzeln finden, Punkte der Kurve ausgeben
(c) Punkt-Subtraktion P - Q mit Zwischenschritten
(d) Punkt-Verdopplung 2P mit Zwischenschritten
"""

from dataclasses import dataclass
from typing import Optional, List, Tuple, Dict

# ----------------------------
# Mathe-Basics mod p
# ----------------------------

def mod(x: int, p: int) -> int:
    return x % p

def egcd(a: int, b: int):
    if b == 0:
        return (a, 1, 0)
    g, x, y = egcd(b, a % b)
    return (g, y, x - (a // b) * y)

def inv_mod(a: int, p: int) -> int:
    a %= p
    if a == 0:
        raise ZeroDivisionError("Keine Inverse für 0 mod p")
    g, x, _ = egcd(a, p)
    if g != 1:
        raise ZeroDivisionError(f"Keine Inverse: gcd({a},{p})={g}")
    return x % p

def sqrt_mod_bruteforce(n: int, p: int) -> List[int]:
    """Bruteforce-Wurzeln: finde alle y mit y^2 ≡ n (mod p). (Für kleine p perfekt.)"""
    n %= p
    roots = []
    for y in range(p):
        if (y * y) % p == n:
            roots.append(y)
    return roots

def quadratic_residues_map(p: int) -> Dict[int, List[int]]:
    """Map: r -> [y], so dass y^2 ≡ r (mod p)."""
    mp: Dict[int, List[int]] = {}
    for y in range(p):
        r = (y * y) % p
        mp.setdefault(r, []).append(y)
    return mp

# ----------------------------
# Elliptische Kurve & Punkte
# ----------------------------

@dataclass(frozen=True)
class ECPoint:
    x: Optional[int] = None
    y: Optional[int] = None

    @property
    def is_infinity(self) -> bool:
        return self.x is None and self.y is None

    def __str__(self) -> str:
        return "O" if self.is_infinity else f"({self.x},{self.y})"

O = ECPoint()

class EllipticCurveFp:
    def __init__(self, p: int, a: int, b: int):
        self.p = p
        self.a = a % p
        self.b = b % p

    def rhs(self, x: int) -> int:
        """x^3: + a x + b mod p"""
        p = self.p
        return (x*x*x + self.a*x + self.b) % p

    def is_on_curve(self, P: ECPoint) -> bool:
        if P.is_infinity:
            return True
        p = self.p
        return (P.y * P.y - self.rhs(P.x)) % p == 0

    def negate(self, P: ECPoint) -> ECPoint:
        """-P = (x, -y mod p)"""
        if P.is_infinity:
            return O
        return ECPoint(P.x, (-P.y) % self.p)

    # ----------------------------
    # Punktaddition mit Ausgabe
    # ----------------------------

    def add(self, P: ECPoint, Q: ECPoint, show_steps: bool = True) -> ECPoint:
        p = self.p

        if show_steps:
            print("\n=== Punktaddition ===")
            print(f"Kurve: y^2 = x^3 + {self.a}x + {self.b}  über GF({p})")
            print(f"P = {P}, Q = {Q}")

        # Sonderfälle
        if P.is_infinity:
            if show_steps:
                print("Sonderfall: P = O  =>  P + Q = Q")
            return Q
        if Q.is_infinity:
            if show_steps:
                print("Sonderfall: Q = O  =>  P + Q = P")
            return P

        # P + (-P) = O
        if P.x == Q.x and (P.y + Q.y) % p == 0:
            if show_steps:
                print("Sonderfall: Q = -P (gleicher x, y1 + y2 ≡ 0)  =>  P + Q = O")
            return O

        # Steigung λ
        if P.x != Q.x:
            # λ = (y2 - y1) / (x2 - x1) mod p
            num = (Q.y - P.y) % p
            den = (Q.x - P.x) % p
            den_inv = inv_mod(den, p)
            lam = (num * den_inv) % p
            if show_steps:
                print("\nFall: P != Q (x1 != x2)")
                print("Formel: λ = (y2 - y1) / (x2 - x1)  (mod p)")
                print(f"λ = ({Q.y} - {P.y}) / ({Q.x} - {P.x}) mod {p}")
                print(f"  = {num} / {den} mod {p}")
                print(f"  inv({den}) mod {p} = {den_inv}")
                print(f"  => λ = {num} * {den_inv} mod {p} = {lam}")
        else:
            # Punktverdopplung: λ = (3x1^2 + a) / (2y1) mod p
            num = (3 * P.x * P.x + self.a) % p
            den = (2 * P.y) % p
            den_inv = inv_mod(den, p)
            lam = (num * den_inv) % p
            if show_steps:
                print("\nFall: P = Q (Verdopplung)")
                print("Formel: λ = (3x1^2 + a) / (2y1)  (mod p)")
                print(f"λ = (3*{P.x}^2 + {self.a}) / (2*{P.y}) mod {p}")
                print(f"  = {num} / {den} mod {p}")
                print(f"  inv({den}) mod {p} = {den_inv}")
                print(f"  => λ = {num} * {den_inv} mod {p} = {lam}")

        # x3 = λ^2 - x1 - x2
        x3 = (lam * lam - P.x - Q.x) % p
        # y3 = λ(x1 - x3) - y1
        y3 = (lam * (P.x - x3) - P.y) % p

        if show_steps:
            print("\nFormeln:")
            print("x3 = λ^2 - x1 - x2 (mod p)")
            print("y3 = λ(x1 - x3) - y1 (mod p)")
            print(f"x3 = {lam}^2 - {P.x} - {Q.x} mod {p} = {x3}")
            print(f"y3 = {lam}*({P.x} - {x3}) - {P.y} mod {p} = {y3}")
            print(f"Ergebnis: R = P + Q = ({x3},{y3})")

        return ECPoint(x3, y3)

    def sub(self, P: ECPoint, Q: ECPoint, show_steps: bool = True) -> ECPoint:
        if show_steps:
            print("\n=== Subtraktion ===")
            print("Definition: P - Q = P + (-Q)")
        negQ = self.negate(Q)
        if show_steps:
            print(f"-Q = {negQ} (weil -y mod p)")
        return self.add(P, negQ, show_steps=show_steps)

    # ----------------------------
    # Tabellen & Punkte
    # ----------------------------

    def table_sx(self, show_steps: bool = True) -> List[Tuple[int, int]]:
        p = self.p
        out = []
        if show_steps:
            print("\n=== (a) Tabelle s_x = x^3 + ax + b (mod p) ===")
            print(f"Formel: s_x = x^3 + {self.a}x + {self.b} (mod {p})\n")
            print(" x | s_x")
            print("---+-----")
        for x in range(p):
            sx = self.rhs(x)
            out.append((x, sx))
            if show_steps:
                print(f"{x:>2} | {sx:>3}")
        return out

    def list_points(self, show_steps: bool = True) -> List[ECPoint]:
        p = self.p
        qr = quadratic_residues_map(p)

        if show_steps:
            print("\n=== (b) Quadratische Reste & Punkte der Kurve ===")
            print("Wir prüfen für jedes x:")
            print("  s_x = x^3 + ax + b (mod p)")
            print("Falls s_x quadratischer Rest ist: löse y^2 ≡ s_x (mod p)")
            print("\nQuadratische Reste (r -> y mit y^2=r):")
            # kompakt ausgeben
            for r in sorted(qr):
                ys = qr[r]
                print(f"  {r:>2}: {ys}")

        points: List[ECPoint] = [O]  # Punkt im Unendlichen
        if show_steps:
            print("\nPunkte auf E:")
            print("O (Punkt im Unendlichen)")

        for x in range(p):
            sx = self.rhs(x)
            ys = qr.get(sx, [])
            if show_steps:
                if ys:
                    print(f"x={x:>2}: s_x={sx:>2} ist QR -> Lösungen y = {ys}")
                else:
                    print(f"x={x:>2}: s_x={sx:>2} ist KEIN QR -> keine Punkte")

            for y in ys:
                points.append(ECPoint(x, y))

        if show_steps:
            print(f"\nAnzahl Punkte |E(GF({p}))| = {len(points)}")
        return points


# ----------------------------
# PARI/GP-Hinweis (optional)
# ----------------------------

def pari_gp_hint(p: int):
    print("\n=== PARI/GP Hinweis (optional) ===")
    print("Für Wurzeln mod p kannst du in PARI/GP z.B. benutzen:")
    print(f"  for(x=0,{p-1}, sx=Mod(x, {p})^3 + 4*Mod(x,{p}) + 1; print(x, \" \", sqrt(sx)))")
    print("Oder allgemein: sqrt(Mod(sx,p)) liefert ggf. Wurzeln / 0 wenn keine existieren.")


# ----------------------------
# Interaktive Konsole
# ----------------------------

def read_point(name: str, p: int) -> ECPoint:
    raw = input(f"{name} eingeben als x,y (oder 'O'): ").strip()
    if raw.upper() == "O":
        return O
    try:
        xs, ys = raw.split(",")
        x = int(xs.strip()) % p
        y = int(ys.strip()) % p
        return ECPoint(x, y)
    except Exception:
        raise ValueError("Punktformat muss 'x,y' oder 'O' sein.")

def main():
    print("Elliptische Kurven über GF(p) – Übungsmodus mit Zwischenschritten")
    print("----------------------------------------------------------------")

    try:
        p = int(input("Primzahl p (z.B. 11): ").strip())
        a = int(input("Parameter a (z.B. 4): ").strip())
        b = int(input("Parameter b (z.B. 1): ").strip())
    except ValueError:
        print("❌ Bitte ganze Zahlen eingeben.")
        return

    E = EllipticCurveFp(p, a, b)

    print(f"\nKurve: E: y^2 = x^3 + {E.a}x + {E.b}  über GF({p})")

    # (a)
    E.table_sx(show_steps=True)

    # (b)
    E.list_points(show_steps=True)

    # optionaler PARI/GP Hinweis
    pari_gp_hint(p)

    # (c) und (d)
    print("\n=== (c) und (d) Punktrechnungen ===")
    print("Du kannst jetzt Punkte eingeben und das Skript zeigt alle Zwischenschritte.")
    print("Beispiel aus deinem Blatt: P=5,5 und Q=7,3 bei p=11, a=4, b=1")

    while True:
        print("\nWähle:")
        print("  1) P - Q berechnen")
        print("  2) 2P berechnen")
        print("  3) Programm beenden")
        choice = input("> ").strip()

        if choice == "1":
            try:
                P = read_point("P", p)
                Q = read_point("Q", p)
            except ValueError as e:
                print(f"❌ {e}")
                continue

            if not E.is_on_curve(P) or not E.is_on_curve(Q):
                print("❌ Achtung: Mindestens ein Punkt liegt nicht auf der Kurve!")
                print(f"   P on curve? {E.is_on_curve(P)} | Q on curve? {E.is_on_curve(Q)}")
                continue

            R = E.sub(P, Q, show_steps=True)
            print(f"\n✅ Ergebnis: P - Q = {R}")

        elif choice == "2":
            try:
                P = read_point("P", p)
            except ValueError as e:
                print(f"❌ {e}")
                continue

            if not E.is_on_curve(P):
                print("❌ Achtung: Punkt liegt nicht auf der Kurve!")
                continue

            R = E.add(P, P, show_steps=True)
            print(f"\n✅ Ergebnis: 2P = {R}")

        elif choice == "3":
            print("Bye 👋")
            break
        else:
            print("❌ Ungültige Auswahl.")


if __name__ == "__main__":
    main()
