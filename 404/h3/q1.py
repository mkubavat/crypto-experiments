import hashlib
import binascii

def compute_sha256_with_key_and_padding(file_path, hex_key):
    # Convert the hexadecimal key to bytes
    key_bytes = binascii.unhexlify(hex_key)

    # Read the file content
    with open(file_path, "rb") as file:
        file_data = file.read()

    # Concatenate key and file data
    key_plus_file = key_bytes + file_data

    # Compute SHA-256 hash
    sha256_hash = hashlib.sha256(key_plus_file)

    # Padding calculation for SHA-256
    message_length = len(key_plus_file) * 8
    padding = b'\x80'
    padding_length = (64 - (len(key_plus_file) + 1 + 8) % 64) % 64
    padding += b'\x00' * padding_length
    padding += message_length.to_bytes(8, byteorder='big')

    return sha256_hash.hexdigest(), padding

file_path = '5372bc129ee7.binary'  # Replace with your file path
hex_key = '0A6A24F5EAFCA5D0'  # Key in hexadecimal format
hash_value, padding = compute_sha256_with_key_and_padding(file_path, hex_key)
print(f"SHA-256 Hash of Key || File: {hash_value}")
print(f"Padding: {padding.hex()}")
