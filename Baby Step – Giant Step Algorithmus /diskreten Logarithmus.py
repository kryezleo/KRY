# Universal Baby-Step Giant-Step implementation for discrete logarithm in Z_p^*
# Usage: set the variables `g`, `h`, `p` to your instance and call discrete_log_bsgs(g,h,p).
# If p is prime, order = p-1 by default. For a subgroup or non-prime modulus, pass `order` explicitly.
#
# What to adapt for another problem:
# - g : generator/base (int)
# - h : target element (int), we want x such that g^x ≡ h (mod p)
# - p : modulus (int) — typically a prime for Z_p^*
# - order (optional): the order of g in the multiplicative group. If p is prime and g is a primitive root, use p-1.
#
# The function returns an integer x in [0, order-1] such that g^x ≡ h (mod p), or None if no solution found.

from math import ceil, sqrt

def egcd(a, b):
    """Extended gcd. Returns (g, x, y) with g = gcd(a,b) and ax + by = g."""
    if b == 0:
        return (a, 1, 0)
    else:
        g, x1, y1 = egcd(b, a % b)
        return (g, y1, x1 - (a // b) * y1)

def modinv(a, m):
    """Modular inverse of a mod m (works for general m if inverse exists)."""
    g, x, _ = egcd(a, m)
    if g != 1:
        return None  # inverse does not exist
    return x % m

def discrete_log_bsgs(g, h, p, order=None):
    """
    Baby-step Giant-step algorithm to solve discrete log g^x = h (mod p).
    - g, h, p: integers
    - order: optional, the order of g; if p is prime and g is primitive, use p-1.
    Returns x (0 <= x < order) or None if no solution found.
    """
    # Normalize inputs
    g %= p
    h %= p
    if order is None:
        # default to p-1 (valid when p is prime and g in multiplicative group)
        order = p - 1

    m = ceil(sqrt(order))  # baby-step size

    # Baby steps: store g^j -> j for j = 0..m-1
    baby = {}
    cur = 1
    for j in range(m):
        if cur not in baby:   # only store first occurrence (smallest j)
            baby[cur] = j
        cur = (cur * g) % p

    # Compute factor = g^{-m} mod p
    g_m = pow(g, m, p)
    try:
        factor = pow(g_m, -1, p)  # modular inverse of g^m mod p (Python 3.8+)
    except ValueError:
        # fallback: use modinv (works for general modulus if inverse exists)
        inv = modinv(g_m, p)
        if inv is None:
            # no inverse, algorithm fails for this modulus
            return None
        factor = inv

    # Giant steps: look for collision h * (g^{-m})^i in baby
    giant = h
    for i in range(m):
        if giant in baby:
            # solution found: x = i*m + baby[giant]
            x = i * m + baby[giant]
            # reduce modulo order (smallest non-negative solution)
            x %= order
            # verify (safety)
            if pow(g, x, p) == h:
                return x
            # otherwise continue searching (rare)
        giant = (giant * factor) % p

    # No solution found
    return None

# -------------------------
# Example: the exercise you had
# Solve for x: 17^x ≡ 42 (mod 61)
# To adapt for a different instance, change g, h, p below.
# -------------------------
if __name__ == "__main__":
    g = 17   # base (change me)
    h = 42   # target (change me)
    p = 61   # modulus (change me)
    # If p is prime and g is a generator, you can omit order or set order=p-1.
    x = discrete_log_bsgs(g, h, p)
    if x is None:
        print(f"No solution found for g={g}, h={h}, p={p}")
    else:
        print(f"Solution: x = {x}  (check: {g}^{x} ≡ {pow(g,x,p)} mod {p})")
