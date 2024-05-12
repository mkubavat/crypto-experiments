import hashlib

# Function to calculate the SHA-256 padding
def sha256_padding(message_length):
    # The length of the message in bits
    message_bit_length = message_length * 8
    # Padding starts with a '1' bit plus enough '0' bits to make the length
    # 64 bits less than a multiple of 512
    padding = b'\x80' + b'\x00' * ((448 - message_bit_length - 1) % 512 // 8)
    # Append the length of the message in the last 64 bits
    padding += message_bit_length.to_bytes(8, byteorder='big')
    return padding

# Given message M (hex encoded)
message_hex = '553CCD44546F01C2C82A30679E49D05E941799E1046C99ABAC93A48DC3333250D12072EB15DDD56DD2630D5B1D9ADBD6680E3492C32A4E00DCC4D690009CCC49469D3A21981D08323DAC6E8B0E05059201DC58D7630D47957AE403'

# Convert message M from hex to bytes and calculate its length
message = bytes.fromhex(message_hex)
message_length = len(message)

# Assume the key K is 20 bytes long
key_length = 20  # in bytes

# Total length is key + message
total_length = key_length + message_length

# Calculate the padding
padding = sha256_padding(total_length)

# The given additional message block M2 (hex encoded)
m2_hex = 'B15B28E0BE701025107073CD506D3020CD80459C635B2DE351B5DE6C6D790DACBC965490C8847007261CDB905ECC6E6C7A81B909B0730E208B1D73AD6D50A2BA728640E2A450DE5B6220443D44DC030372928140509D9EEB'
m2 = bytes.fromhex(m2_hex)

# Create a dummy key of 20 bytes length since the actual key is unknown
key = b'\x00' * key_length

# Calculate the SHA256 hash of K || M || P || M2
hash_input = key + message + padding + m2
computed_hash = hashlib.sha256(hash_input).hexdigest()

# The results
padding_hex = padding.hex()
computed_hash_hex = computed_hash

print(padding_hex)
print(computed_hash_hex)
