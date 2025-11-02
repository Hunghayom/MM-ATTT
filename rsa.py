import sympy
import random

def text_to_int(text):
    return int.from_bytes(text.encode(), byteorder='big')

def int_to_text(num):
    return num.to_bytes((num.bit_length() + 7) // 8, byteorder='big').decode()

def generate_large_prime(n_digits=50):
    lower = 10**(n_digits-1)
    upper = (10**n_digits) - 1
    return sympy.randprime(lower, upper)

def generate_rsa_keys(n_digits=50):
    p = generate_large_prime(n_digits)
    q = generate_large_prime(n_digits)
    n = p * q
    phi = (p - 1) * (q - 1)
    e = 65537
    d = sympy.mod_inverse(e, phi)
    return (e, n), (d, n)

def encrypt(message, public_key):
    e, n = public_key
    m = text_to_int(message)
    c = pow(m, e, n)
    return c

def decrypt(ciphertext, private_key):
    d, n = private_key
    m = pow(ciphertext, d, n)
    return int_to_text(m)

if __name__ == "__main__":
    message = input("Nhập thông điệp cần mã hóa (RSA): ")

    public_key, private_key = generate_rsa_keys()
    ciphertext = encrypt(message, public_key)
    plaintext = decrypt(ciphertext, private_key)

    print("\n--- RSA ---")
    print("Ciphertext:", ciphertext)
    print("Giải mã:", plaintext)
