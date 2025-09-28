
import secrets
import math
import sys

#probable_prime
def is_probable_prime(n: int, k: int = 16) -> bool:
    if n < 2:
        return False
    small_primes = (2,3,5,7,11,13,17,19,23,29)
    for p in small_primes:
        if n % p == 0:
            return n == p
    d = n - 1
    r = 0
    while d % 2 == 0:
        d //= 2
        r += 1
    for _ in range(k):
        a = secrets.randbelow(n - 3) + 2
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True

def generate_prime(bits: int) -> int:
    if bits < 2:
        raise ValueError("bits must be >= 2")
    while True:
        cand = secrets.randbits(bits) | (1 << (bits - 1)) | 1
        if is_probable_prime(cand):
            return cand


def egcd(a: int, b: int):
    if b == 0:
        return (a, 1, 0)
    else:
        g, x1, y1 = egcd(b, a % b)
        return (g, y1, x1 - (a // b) * y1)

def modinv(a: int, m: int) -> int:
    g, x, _ = egcd(a, m)
    if g != 1:
        raise ValueError("modular inverse does not exist")
    return x % m


def generate_keypair(prime_bits: int = 256):
    p = generate_prime(prime_bits)
    q = generate_prime(prime_bits)
    while q == p:
        q = generate_prime(prime_bits)
    n = p * q
    phi = (p - 1) * (q - 1)
    e = 65537
    if math.gcd(e, phi) != 1:
        # choose another e if clash
        while True:
            e = secrets.randbelow(phi - 3) + 2
            if e % 2 == 0:
                e += 1
            if math.gcd(e, phi) == 1:
                break
    d = modinv(e, phi)
    pub = (n, e)
    priv = (n, d, p, q)
    return pub, priv

def text_to_int(s: str) -> int:
    return int.from_bytes(s.encode('utf-8'), 'big')

def int_to_text(i: int) -> str:
    b = i.to_bytes((i.bit_length() + 7) // 8 or 1, 'big')
    return b.decode('utf-8', errors='strict')

def encrypt_text_plainstore(message: str, pubkey):
    n, e = pubkey
    m = text_to_int(message)
    if m >= n:
        raise ValueError("Message too long for current modulus.")
    c = pow(m, e, n)
    return c  # store ciphertext integer

def decrypt_cipher_to_text(cipher_int: int, privkey):
    n, d, p, q = privkey
    m = pow(cipher_int, d, n)
    # decode
    return int_to_text(m)

def sign_text(message: str, privkey):
    n, d, p, q = privkey
    m = text_to_int(message)
    if m >= n:
        raise ValueError("Message too long for current modulus.")
    s = pow(m, d, n)
    return s

def verify_text(message: str, signature_int: int, pubkey):
    n, e = pubkey
    if not (0 <= signature_int < n):
        return False
    m = text_to_int(message)
    v = pow(signature_int, e, n)
    return v == m

# Phases of the app

# Generating keys
PUBLIC_KEY, PRIVATE_KEY = generate_keypair(256)  # primes of 256 bits -> n ~ 512 bits
print("RSA keys have been generated.")

#array to store the message and signatures
MESSAGES = []        
SIGNATURES = []      # list of tuples 

# main app

def main_menu():
    while True:
        print("Please select your user type:")
        print("1. A public user")
        print("2. The owner of the keys")
        print("3. Exit program")
        choice = input("Enter your choice: ").strip()
        if choice == "1":
            public_user_menu()
        elif choice == "2":
            owner_menu()
        elif choice == "3":
            print("Bye for now!")
            sys.exit(0)
        else:
            print("Invalid choice. Try again.")

#user  app
def public_user_menu():
    while True:
        print("As a public user, what would you like to do?")
        print("1. Send an encrypted message")
        print("2. Authenticate a digital signature")
        print("3. Exit")
        choice = input("Enter your choice: ").strip()
        if choice == "1":
            # send encrypted message to owner
            msg = input("Enter a message: ")
            try:
                c = encrypt_text_plainstore(msg, PUBLIC_KEY)
                MESSAGES.append(c)
                print("Message encrypted and sent.")
            except Exception as e:
                print("Error encrypting message:", e)
        elif choice == "2":
            if not SIGNATURES:
                print("There are no signature to authenticate.")
                continue
            # list available signatures
            print("The following messages are available:")
            for idx, (mtext, _) in enumerate(SIGNATURES, start=1):
                print(f"{idx}. {mtext}")
            sel = input("Enter your choice: ").strip()
            if not sel.isdigit() or not (1 <= int(sel) <= len(SIGNATURES)):
                print("Invalid choice.")
                continue
            idx = int(sel) - 1
            mtext, sigint = SIGNATURES[idx]
            valid = verify_text(mtext, sigint, PUBLIC_KEY)
            if valid:
                print("Signature is valid.")
            else:
                print("Signature is NOT valid.")
        elif choice == "3":
            return
        else:
            print("Invalid choice. Try again.")


def owner_menu():
    global PUBLIC_KEY, PRIVATE_KEY, MESSAGES, SIGNATURES
    while True:
        print("As the owner of the keys, what would you like to do?")
        print("1. Decrypt a received message")
        print("2. Digitally sign a message")
        print("3. Show the keys ")
        print("4. Generating a new set of the keys")
        print("5. Exit")
        choice = input("Enter your choice: ").strip()
        if choice == "1":
            if not MESSAGES:
                print("There are no messages to decrypt.")
                continue
            print("The following messages are available:")
            for i, c in enumerate(MESSAGES, start=1):
                
                try:
                    decrypted = decrypt_cipher_to_text(c, PRIVATE_KEY)
                    length = len(decrypted)
                except Exception:
                    
                    try:
                        m_int = pow(c, PRIVATE_KEY[1], PRIVATE_KEY[0])
                        b = m_int.to_bytes((m_int.bit_length() + 7)//8 or 1, 'big')
                        length = len(b)
                    except Exception:
                        length = 0
                print(f"{i}. (length = {length})")
            sel = input("Enter your choice: ").strip()
            if not sel.isdigit() or not (1 <= int(sel) <= len(MESSAGES)):
                print("Invalid choice.")
                continue
            idx = int(sel) - 1
            c = MESSAGES[idx]
            try:
                decrypted_text = decrypt_cipher_to_text(c, PRIVATE_KEY)
                # show uppercase as in sample I/O
                print("Decrypted message:", decrypted_text.upper())
            except Exception as e:
                print("Error decrypting message:", e)
        elif choice == "2":
            m = input("Enter a message: ")
            try:
                sig = sign_text(m, PRIVATE_KEY)
                SIGNATURES.append((m, sig))
                print("Message signed and sent.")
            except Exception as e:
                print("Error signing message:", e)
        elif choice == "3":
            n, e = PUBLIC_KEY
            n_hex = hex(n)
            e_hex = hex(e)
            print("Public key (n, e):")
            print("n (hex):", n_hex)
            print("e (hex):", e_hex)
            # show private too for owner
            n2, d, p, q = PRIVATE_KEY
            print("Private key (showing d in hex):")
            print("d (hex):", hex(d))
        elif choice == "4":
            PUBLIC_KEY, PRIVATE_KEY = generate_keypair(256)
            # Keep stored messages/signatures as per design (or clear if desired). We'll keep them.
            print("New RSA keys have been generated.")
        elif choice == "5":
            return
        else:
            print("Invalid choice. Try again.")

#Starting point
def main():
    try:
        main_menu()
    except KeyboardInterrupt:
        print("\nInterrupted. Exiting.")
        sys.exit(0)

if __name__ == "__main__":
    main()