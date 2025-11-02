import sympy
import random

def text_to_int(text):
    return int.from_bytes(text.encode(), byteorder='big')

def int_to_text(num):
    return num.to_bytes((num.bit_length() + 7) // 8, byteorder='big').decode()

class ECC:
    def __init__(self, a, b, p, G):
        self.a = a
        self.b = b
        self.p = p
        self.G = G

    def add(self, P, Q):
        if P is None: return Q
        if Q is None: return P

        if P == Q:
            m = (3 * P[0]**2 + self.a) * sympy.mod_inverse(2 * P[1], self.p)
        else:
            m = (Q[1] - P[1]) * sympy.mod_inverse(Q[0] - P[0], self.p)

        m %= self.p
        x = (m*m - P[0] - Q[0]) % self.p
        y = (m*(P[0] - x) - P[1]) % self.p
        return (x, y)

    def multiply(self, P, n):
        R = None
        while n:
            if n & 1:
                R = self.add(R, P)
            P = self.add(P, P)
            n >>= 1
        return R

def generate_prime(n_digits=50):
    lower = 10**(n_digits-1)
    upper = (10**n_digits) - 1
    return sympy.randprime(lower, upper)

p = generate_prime()
a, b = 2, 3
G = (5, 1)
E = ECC(a, b, p, G)

private_key = random.randint(2, p-1)
public_key = E.multiply(G, private_key)

def encrypt(message):
    m = text_to_int(message)
    M = (m % p, (m*m) % p)  # simple encoding to point

    k = random.randint(2, p-1)
    C1 = E.multiply(G, k)
    S = E.multiply(public_key, k)
    C2 = ( (M[0] + S[0]) % p, (M[1] + S[1]) % p )
    return C1, C2

def decrypt(C1, C2):
    S = E.multiply(C1, private_key)
    Mx = (C2[0] - S[0]) % p
    return int_to_text(Mx)

if __name__ == "__main__":
    message = input("Nhập thông điệp cần mã hóa (ECC): ")

    C1, C2 = encrypt(message)
    plaintext = decrypt(C1, C2)

    print("\n--- ECC ---")
    print("Ciphertext:", C1, C2)
    print("Giải mã:", plaintext)
