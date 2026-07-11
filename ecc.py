p = 17
a = 2
b = 2

G = (5, 1)
n = 19


def is_on_curve(P):
    if P is None:
        return True

    x, y = P
    return (y * y - (x * x * x + a * x + b)) % p == 0


def inverse_mod(k, p):
    return pow(k, -1, p)


def point_add(P, Q):
    if P is None:
        return Q
    if Q is None:
        return P

    x1, y1 = P
    x2, y2 = Q

    if x1 == x2 and (y1 + y2) % p == 0:
        return None

    if P == Q:
        m = ((3 * x1 * x1 + a) * inverse_mod(2 * y1, p)) % p
    else:
        m = ((y2 - y1) * inverse_mod(x2 - x1, p)) % p

    x3 = (m * m - x1 - x2) % p
    y3 = (m * (x1 - x3) - y1) % p

    return (x3, y3)


def scalar_mult(k, P):
    result = None
    current = P
    while k > 0:
        if k % 2 == 1:
            result = point_add(result, current)

        current = point_add(current, current)
        k //= 2

    return result


def generate_keys(private_key):
    public_key = scalar_mult(private_key, G)
    return private_key, public_key


def display_keys(private_key, public_key):
    print("\nECC Key Generation")
    print("Private Key =", private_key)
    print("Public Key  =", public_key)

print("G =", G)
print("2G =", point_add(G, G))
print("3G =", scalar_mult(3, G))
print("7G =", scalar_mult(7, G))

private_key = 7
private_key, public_key = generate_keys(private_key)
display_keys(private_key, public_key)
def encrypt(message, public_key, k):
    C1 = scalar_mult(k, G)
    shared = scalar_mult(k, public_key)
    C2 = point_add(message, shared)
    return C1, C2


def negate(P):
    if P is None:
        return None

    x, y = P
    return (x, (-y) % p)


def decrypt(C1, C2, private_key):
    shared = scalar_mult(private_key, C1)
    message = point_add(C2, negate(shared))
    return message
message = (10, 6)
k = 3

C1, C2 = encrypt(message, public_key, k)

print("\nECC Encryption")
print("Message =", message)
print("Random k =", k)
print("C1 =", C1)
print("C2 =", C2)

decrypted = decrypt(C1, C2, private_key)

print("\nECC Decryption")
print("Recovered Message =", decrypted)