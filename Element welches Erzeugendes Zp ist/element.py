# Script: Erzeugende modulo p mit Zwischenschritten

def ord_mod(a, p, verbose=False, label=""):
    """
    Berechnet die Ordnung von a modulo p.
    Wenn verbose=True, werden alle Zwischenschritte ausgegeben:
    a^k mod p für k = 1, 2, ...
    """
    x = 1
    k = 0

    if verbose:
        print(f"\nZwischenschritte für g = {a} (mod {p}) {label}")
        print("-" * 50)

    while True:
        k += 1
        x = (x * a) % p

        if verbose:
            print(f"  Schritt {k:3d}: {a}^{k} mod {p} = {x}")

        if x == 1:
            # Ordnung gefunden
            if verbose:
                print(f"--> Ordnung von {a} modulo {p} ist {k}\n")
            return k

        # Sicherheitsbremse (sollte bei Primzahl p nie greifen,
        # weil die Ordnung höchstens p-1 ist)
        if k > p:
            return None


def find_generators(p):
    """
    Findet alle Erzeugenden modulo p (p prim).
    Gibt eine Liste aller g mit Ordnung p-1 zurück.
    """
    phi = p - 1
    generators = []

    for g in range(1, p):
        if ord_mod(g, p) == phi:
            generators.append(g)

    return generators


def main():
    p = 467 # Prüfende Primzahl eingeben
    print(f"Modul p = {p}")
    print(f"phi(p) = p - 1 = {p - 1}\n")

    # 1) Alle Erzeugenden finden
    generators = find_generators(p)

    print(f"Anzahl Erzeugende modulo {p}: {len(generators)}")
    print(f"Erzeugende (nur zur Kontrolle):")
    print(generators)
    print()

    # 2) Kleinstes und größtes Erzeugendes bestimmen
    smallest = generators[0]
    largest = generators[-1]

    print(f"Kleinstes Erzeugendes  g_min = {smallest}")
    print(f"Groesstes Erzeugendes  g_max = {largest}\n")

    # 3) Zwischenschritte für beide anzeigen
    #    (alle Potenzen, bis wieder 1 erreicht ist)
    ord_mod(smallest, p, verbose=True, label="(kleinstes Erzeugendes)")
    ord_mod(largest, p, verbose=True, label="(groesstes Erzeugendes)")


if __name__ == "__main__":
    main()
