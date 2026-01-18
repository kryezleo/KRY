#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Universelles Skript (für ungerade Primzahl p):
Löst x^2 ≡ a (mod p) mit Tonelli–Shanks und gibt ALLE Zwischenschritte aus.

Beispiel aus Aufgabe (a):
x^2 ≡ 57 (mod 61)
"""

from dataclasses import dataclass

def egcd(a: int, b: int):
    """Extended GCD: returns (g, x, y) with ax + by = g."""
    if b == 0:
        return (a, 1, 0)
    g, x1, y1 = egcd(b, a % b)
    return (g, y1, x1 - (a // b) * y1)

def inv_mod(a: int, p: int) -> int:
    """Modular inverse a^{-1} mod p (p may be prime)."""
    a %= p
    g, x, _ = egcd(a, p)
    if g != 1:
        raise ValueError(f"Kein Inverses: gcd({a},{p})={g}")
    return x % p

def legendre_symbol(a: int, p: int) -> int:
    """
    Legendre-Symbol (a|p) für ungerade Primzahl p.
    Gibt 0, 1 oder -1 zurück.
    """
    a %= p
    if a == 0:
        return 0
    ls = pow(a, (p - 1) // 2, p)
    return -1 if ls == p - 1 else ls  # p-1 entspricht -1 mod p

@dataclass
class TSState:
    q: int
    s: int
    z: int
    c: int
    t: int
    r: int
    m: int

def tonelli_shanks(a: int, p: int, verbose: bool = True):
    """
    Löst x^2 ≡ a (mod p) für ungerade Primzahl p.
    Rückgabe: (x, p-x) als zwei Lösungen, oder None falls keine Lösung existiert.
    """
    if p % 2 == 0:
        raise ValueError("Dieses Skript ist für ungerade p gedacht.")
    a %= p

    def vprint(*args):
        if verbose:
            print(*args)

    vprint("========================================")
    vprint(f"Gesucht: x^2 ≡ {a} (mod {p})")
    vprint("========================================\n")

    # Sonderfälle
    if a == 0:
        vprint("Sonderfall: a = 0 ⇒ x ≡ 0 (mod p)\n")
        return (0, 0)

    # 1) Quadratischer Rest?
    vprint("1) Prüfe, ob a ein quadratischer Rest mod p ist (Euler-Kriterium):")
    exp = (p - 1) // 2
    apow = pow(a, exp, p)
    vprint(f"   a^((p-1)/2) = {a}^({exp}) mod {p} = {apow}")
    if apow == p - 1:
        vprint("   Ergebnis = -1 (mod p) ⇒ KEINE Lösung.\n")
        return None
    elif apow == 1:
        vprint("   Ergebnis =  1 (mod p) ⇒ a ∈ QR_p (Quadratischer Rest). ✓\n")
    else:
        # Bei Prim p sollte das nur 0/1/-1 sein, aber wir lassen es robust.
        vprint(f"   Unerwartetes Ergebnis {apow} (p sollte prim sein).\n")
        return None

    # 2) p ≡ 3 (mod 4) Spezialfall
    if p % 4 == 3:
        vprint("2) Spezialfall: p ≡ 3 (mod 4)")
        x = pow(a, (p + 1) // 4, p)
        vprint(f"   x = a^((p+1)/4) = {a}^({(p+1)//4}) mod {p} = {x}")
        vprint(f"   Kontrolle: x^2 mod p = {pow(x,2,p)}")
        vprint(f"   Lösungen: x ≡ {x} und x ≡ {(-x) % p} (mod {p})\n")
        return (x, (-x) % p)

    # 3) Schreibe p-1 = q * 2^s mit q ungerade
    vprint("2) Zerlegung von p-1 in q * 2^s (q ungerade):")
    pm1 = p - 1
    q = pm1
    s = 0
    while q % 2 == 0:
        q //= 2
        s += 1
    vprint(f"   p-1 = {pm1} = {q} * 2^{s}")
    vprint(f"   q = {q} (ungerade), s = {s}\n")

    # 4) Finde quadratischen Nichtrest z
    vprint("3) Suche z (quadratischer Nichtrest), d.h. z^((p-1)/2) ≡ -1 (mod p):")
    z = 2
    while True:
        lz = legendre_symbol(z, p)
        vprint(f"   teste z = {z}: (z|p) = {lz}  "
               f"⇒ z^({exp}) mod {p} = {pow(z, exp, p)}")
        if lz == -1:
            vprint(f"   Gefunden: z = {z} ist ein Nichtrest. ✓\n")
            break
        z += 1

    # 5) Tonelli–Shanks Initialisierung
    vprint("4) Tonelli–Shanks Initialisierung:")
    c = pow(z, q, p)
    t = pow(a, q, p)
    r = pow(a, (q + 1) // 2, p)
    m = s
    vprint(f"   c = z^q mod p = {z}^{q} mod {p} = {c}")
    vprint(f"   t = a^q mod p = {a}^{q} mod {p} = {t}")
    vprint(f"   r = a^((q+1)/2) mod p = {a}^{(q+1)//2} mod {p} = {r}")
    vprint(f"   m = s = {m}\n")

    state = TSState(q=q, s=s, z=z, c=c, t=t, r=r, m=m)

    # 6) Iteration
    step = 1
    while state.t != 1:
        vprint(f"5) Iteration {step}: t != 1 ⇒ finde kleinste i (0 < i < m) mit t^(2^i) ≡ 1 (mod p)")
        # finde i
        t2i = state.t
        i = 0
        for i in range(1, state.m):
            t2i = pow(t2i, 2, p)  # t^(2^i)
            vprint(f"   i = {i}: t^(2^{i}) mod p = {t2i}")
            if t2i == 1:
                break
        else:
            raise RuntimeError("Tonelli–Shanks: Kein i gefunden (unerwartet bei Primzahl p).")

        # b = c^(2^(m-i-1))
        e = 1 << (state.m - i - 1)
        b = pow(state.c, e, p)

        vprint("   Update:")
        vprint(f"   b = c^(2^(m-i-1)) mod p = {state.c}^(2^{state.m - i - 1}) mod {p} = {b}")
        vprint(f"   r = r*b mod p = {state.r}*{b} mod {p} = {(state.r*b) % p}")
        vprint(f"   t = t*b^2 mod p = {state.t}*{pow(b,2,p)} mod {p} = {(state.t*pow(b,2,p)) % p}")
        vprint(f"   c = b^2 mod p = {pow(b,2,p)}")
        vprint(f"   m = i = {i}\n")

        state.r = (state.r * b) % p
        state.t = (state.t * pow(b, 2, p)) % p
        state.c = pow(b, 2, p)
        state.m = i
        step += 1

    x = state.r
    vprint("6) Fertig: t = 1 erreicht.")
    vprint(f"   ⇒ Eine Wurzel ist x ≡ r ≡ {x} (mod {p})")
    vprint(f"   ⇒ Zweite Wurzel: -x ≡ {(-x) % p} (mod {p})\n")

    vprint("7) Kontrolle:")
    vprint(f"   {x}^2 mod {p} = {pow(x,2,p)}")
    vprint(f"   {((-x)%p)}^2 mod {p} = {pow((-x)%p,2,p)}")
    vprint("========================================\n")

    return (x, (-x) % p)


def main():
    # Aufgabe (a)
    a = 57
    p = 61
    roots = tonelli_shanks(a, p, verbose=True)
    if roots is None:
        print("Keine Lösung.")
    else:
        x1, x2 = roots
        print(f"Lösungsmenge: {{ {x1}, {x2} }} (mod {p})")


if __name__ == "__main__":
    main()
