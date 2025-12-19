#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Elliptic Curve Helper (universell für Aufgaben im Stil: y² = x³ + a·x + b)

💡 HINWEIS:
---------------------------------------
Bei neuen Aufgaben musst du **nur** die Stellen ändern,
die mit >>> MARKIERT <<< sind!
---------------------------------------
"""

from dataclasses import dataclass
from typing import List, Optional, Tuple
import math

# Optional für Nullstellen/Plots
try:
    import numpy as np
except ImportError:
    np = None
try:
    import matplotlib.pyplot as plt
except ImportError:
    plt = None


# ======================================================
# KLASSE für die Kurve y² = x³ + a·x + b
# ======================================================
@dataclass
class EllipticCurve:
    a: float
    b: float

    # Diskriminante Δ = -16(4a³ + 27b²)
    def discriminant(self) -> float:
        return -16.0 * (4.0 * self.a ** 3 + 27.0 * self.b ** 2)

    def is_nonsingular(self) -> bool:
        return self.discriminant() != 0

    def j_invariant(self) -> Optional[float]:
        denom = 4.0 * self.a ** 3 + 27.0 * self.b ** 2
        if denom == 0:
            return None
        return 1728.0 * (4.0 * self.a ** 3) / denom

    # x³ + a·x + b
    def cubic(self, x: float) -> float:
        return x ** 3 + self.a * x + self.b

    # Reelle Nullstellen (nur wenn numpy vorhanden)
    def real_roots(self) -> List[float]:
        if np is None:
            return []
        coeffs = [1.0, 0.0, self.a, self.b]
        roots = np.roots(coeffs)
        return sorted([float(r.real) for r in roots if abs(r.imag) < 1e-10])

    # Intervalle, in denen y² ≥ 0 gilt
    def intervals_y2_ge_0(self) -> List[Tuple[Optional[float], Optional[float]]]:
        roots = self.real_roots()
        intervals = []
        cuts = [-math.inf] + roots + [math.inf]
        for L, R in zip(cuts[:-1], cuts[1:]):
            x_test = (0.0 if math.isinf(L) and math.isinf(R)
                      else (((-1e3 if math.isinf(L) else L) + (1e3 if math.isinf(R) else R)) / 2.0))
            val = self.cubic(x_test)
            if val >= 0:
                intervals.append((None if math.isinf(L) else L, None if math.isinf(R) else R))
        return intervals

    # Beispielpunkte auf E(R)
    def sample_real_points(self, n_per_interval: int = 50) -> List[Tuple[float, float]]:
        pts = []
        intervals = self.intervals_y2_ge_0()
        if np is None:
            return pts
        for L, R in intervals:
            if L is None: L = -5.0  # <<< HIER ggf. Bereich anpassen, wenn Kurve sehr groß/klein
            if R is None: R =  5.0  # <<< dito
            xs = np.linspace(L, R, n_per_interval)
            for x in xs:
                rhs = self.cubic(x)
                if rhs >= -1e-12:
                    y = math.sqrt(max(0.0, rhs))
                    pts.append((x,  y))
                    pts.append((x, -y))
        return pts

    # Plot
    def plot_real(self, x_min: float = -4.0, x_max: float = 4.0, n: int = 200):
        if plt is None or np is None:
            print("Plot nicht möglich (matplotlib/numpy nicht installiert).")
            return
        xs = np.linspace(x_min, x_max, n)
        ys_pos, ys_neg = [], []
        for x in xs:
            val = self.cubic(x)
            if val >= 0:
                y = math.sqrt(val)
                ys_pos.append(y)
                ys_neg.append(-y)
            else:
                ys_pos.append(np.nan)
                ys_neg.append(np.nan)

        plt.figure()
        plt.plot(xs, ys_pos, label="y = +√(x³ + a·x + b)")
        plt.plot(xs, ys_neg, label="y = -√(x³ + a·x + b)")
        plt.title(f"Elliptische Kurve y² = x³ + {self.a}x + {self.b}")
        plt.xlabel("x")
        plt.ylabel("y")
        plt.legend()
        plt.grid(True)
        plt.show()


# ======================================================
# GF(p)-Funktionen (für Aufgaben über endlichen Körper)
# ======================================================
def points_over_fp(a: int, b: int, p: int) -> List[Tuple[int, int]]:
    pts = []
    for x in range(p):
        rhs = (x**3 + a*x + b) % p
        for y in range(p):
            if (y*y) % p == rhs:
                pts.append((x, y))
    pts.append((None, None))
    return pts

def is_nonsingular_mod_p(a: int, b: int, p: int) -> bool:
    delta = (-16 * (4 * (a % p)**3 + 27 * (b % p)**2)) % p
    return delta != 0


# ======================================================
# HAUPTBEREICH (HIER MUSST DU ANPASSEN!)
# ======================================================
if __name__ == "__main__":

    # === 🔹 REALER FALL =================================
    # >>> HIER DEINE KOEFFIZIENTEN EINGEBEN <<<
    # Beispiel: y² = x³ - 2x  -> a = -2, b = 0
    a = -2      # <<< HIER a einsetzen
    b = 0       # <<< HIER b einsetzen

    E = EllipticCurve(a=a, b=b)
    print("=== Reeller Fall ===")
    print(f"Kurve: y² = x³ + {a}x + {b}")
    print(f"Δ = {E.discriminant()}  → Nicht-singulär? {E.is_nonsingular()}")
    print(f"j-Invariante j = {E.j_invariant()}")
    print(f"Reelle Nullstellen: {E.real_roots()}")
    print(f"Intervalle mit y² ≥ 0: {E.intervals_y2_ge_0()}")

    # >>> Optional: Plot anzeigen <<<
    # E.plot_real(x_min=-4, x_max=4, n=400)

    pts = E.sample_real_points(n_per_interval=20)
    print(f"Beispielpunkte auf E(R): {len(pts)} (erste 10) → {pts[:10]}")


    # === 🔹 ENDLICHER KÖRPER GF(p) ======================
    # >>> HIER DEINE PRIMZAHL p ANPASSEN <<<
    # Beispiel: p = 101
    p = 101     # <<< HIER p ändern (muss Primzahl sein)

    print("\n=== Endlicher Körper GF(p) ===")
    print(f"p = {p} → Nicht-singulär mod p? {is_nonsingular_mod_p(a, b, p)}")

    pts_fp = points_over_fp(a, b, p)
    print(f"|E(GF({p}))| (inkl. ∞) = {len(pts_fp)}")
    # print(pts_fp)   # <<< Optional: alle Punkte anzeigen
