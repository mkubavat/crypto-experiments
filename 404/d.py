from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import binascii
from datetime import datetime, timedelta
import random

def generate_key(seed):
    random.seed(seed)
    return ''.join(f'{random.randint(0, 255):02X}' for _ in range(16))

def try_decrypt(key_hex, iv_hex, ciphertext):
    key = binascii.unhexlify(key_hex)
    iv = binascii.unhexlify(iv_hex)
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    return decryptor.update(ciphertext) + decryptor.finalize()

# Read the entire plaintext file to extract the corresponding bytes for XORing
with open('default.pdf', 'rb') as plaintext_file:
    plaintext = plaintext_file.read()

# Read the first block (16 bytes) of the ciphertext file to extract the IV
with open('cf0c62520ed8.pdf.enc', 'rb') as encrypted_file:
    iv = encrypted_file.read(16)

# Decrypt the first block of ciphertext to recover the IV for each key
recovered_ivs = {}
for i in range(7200):
    key_hex = generate_key(1582201800 + i)  # Start timestamp is adjusted according to your requirements
    decrypted_block = try_decrypt(key_hex, "00000000000000000000000000000000", iv)
    recovered_iv = bytes(a ^ b for a, b in zip(decrypted_block, plaintext[:16])).hex()
    recovered_ivs[key_hex] = recovered_iv

# Continue with the original script to read the entire encrypted file and decrypt with the recovered IVs
with open("cf0c62520ed8.pdf.enc", "rb") as encrypted_file:
    ciphertext = encrypted_file.read()

decryption_successful = False

for key_hex, recovered_iv in recovered_ivs.items():
    try:
        plaintext = try_decrypt(key_hex, recovered_iv, ciphertext)
        if plaintext[:5].decode("ascii").startswith('%PDF-'):
            output_filename = "decrypted_output.pdf"
            with open(output_filename, "wb") as decrypted_file:
                decrypted_file.write(plaintext)
            print(f"Decryption successful with key: {key_hex}, IV: {recovered_iv}")
            print("First line of the decrypted file:")
            print(plaintext.splitlines()[0].decode("ascii"))
            decryption_successful = True
            break
    except Exception as e:
        pass


if not decryption_successful:
    print("Failed to decrypt with any key. There might be another issue.")
