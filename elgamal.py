import sympy
import random

def text_to_int(text):
    return int.from_bytes(text.encode(), byteorder='big')

def int_to_text(num):
    return num.to_bytes((num.bit_length() + 7) // 8, byteorder='big').decode()

def generate_prime(n_digits=50):
    lower = 10**(n_digits-1)
    upper = (10**n_digits) - 1
    return sympy.randprime(lower, upper)

def generate_elgamal_keys(n_digits=50):
    p = generate_prime(n_digits)
    g = random.randint(2, p-2)
    x = random.randint(2, p-2)
    h = pow(g, x, p)
    return (p, g, h), x

def encrypt(message, public_key):
    p, g, h = public_key
    m = text_to_int(message)
    y = random.randint(2, p-2)
    c1 = pow(g, y, p)
    s = pow(h, y, p)
    c2 = (m * s) % p
    return c1, c2

def decrypt(ciphertext, private_key, p):
    c1, c2 = ciphertext
    x = private_key
    s = pow(c1, x, p)
    m = (c2 * sympy.mod_inverse(s, p)) % p
    return int_to_text(m)

if __name__ == "__main__":
    message = input("Nhập thông điệp cần mã hóa (ElGamal): ")

    public_key, private_key = generate_elgamal_keys()
    ciphertext = encrypt(message, public_key)
    plaintext = decrypt(ciphertext, private_key, public_key[0])

    print("\n--- ElGamal ---")
    print("Ciphertext:", ciphertext)
    print("Giải mã:", plaintext)
