from Crypto.Cipher import DES
import itertools

# The known part of the key in hexadecimal
known_key_part_hex = 'F7E675BC38'
known_key_part = bytes.fromhex(known_key_part_hex)
unknown_key_part_length = 3  # 24 bits = 3 bytes

# Function to try decrypting with a specific key
def try_decrypt(key, encrypted_data):
    cipher = DES.new(key, DES.MODE_ECB)
    decrypted_data = cipher.decrypt(encrypted_data)
    return decrypted_data

# Read the encrypted file
encrypted_file_path = '5a214bcae507.txt.enc'  # Update this path
with open(encrypted_file_path, 'rb') as file:
    encrypted_data = file.read()

# Iterate over all possible combinations for the unknown part of the key
for unknown_part in itertools.product(range(256), repeat=unknown_key_part_length):
    # Construct the full key by combining the known and unknown parts
    key = known_key_part + bytes(unknown_part)
    
    # Attempt to decrypt the data
    decrypted_data = try_decrypt(key, encrypted_data)
    
    try:
        # Try to decode as UTF-8 and print
        decoded_text = decrypted_data.decode('utf-8')
        print(f"Success with key: {key.hex()}\nDecrypted content (UTF-8): {decoded_text}\n")
        break  # Stop the loop after successful UTF-8 decoding
    except UnicodeDecodeError:
        # If decoding fails, continue with the next key without printing
        continue

print("Attempt completed. If no success message, no valid UTF-8 decryption was found.")
