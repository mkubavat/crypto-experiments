# Given ciphertext (hex encoded)
ciphertext_hex = "CE540300AE059D498295B59D00A7EEE6CB7475F9899AEDFB3E29F0A5647E311B4194D82BB58FF0407CCEC0A9A48D15CDB451806FEF7798C8A47A450D519ADE"

# Convert it to bytes
ciphertext = bytes.fromhex(ciphertext_hex)

# The original and desired parts of the plaintext
original_plaintext_part1 = b"$125"
target_plaintext_part1 = b"$500"

original_plaintext_part2 = b"Ann's"
target_plaintext_part2 = b"mine"

# XOR function
def xor_bytes(b1, b2):
    return bytes(a ^ b for a, b in zip(b1, b2))

# Apply the XOR operation at the correct indices
# The positions need to be multiplied by 2 for hex representation (1 byte = 2 hex characters)
# "Transfer " is 9 bytes long so $125 starts at the 9th byte position. 
# Adding 16 bytes for the IV, we start at the 25th byte position in the ciphertext.
part1_start = 9 * 2 + 32  # 9 bytes for "Transfer ", times 2 for hex, plus 32 hex chars for the IV
part2_start = 36 * 2 + 32  # 36 bytes for up to "into ", times 2 for hex, plus 32 hex chars for the IV

# Calculate the XOR values for both parts
part1_xor = xor_bytes(original_plaintext_part1, target_plaintext_part1)
part2_xor = xor_bytes(original_plaintext_part2, target_plaintext_part2)

# Modify the ciphertext
ciphertext = (
    ciphertext[:part1_start] +
    xor_bytes(ciphertext[part1_start:part1_start+len(part1_xor)], part1_xor) +
    ciphertext[part1_start+len(part1_xor):part2_start] +
    xor_bytes(ciphertext[part2_start:part2_start+len(part2_xor)], part2_xor) +
    ciphertext[part2_start+len(part2_xor):]
)

# Convert the modified ciphertext back to hex
new_ciphertext_hex = ciphertext.hex()

# Output the result
print("First 32 HEXs from the forged ciphertext: " + new_ciphertext_hex[:32])
print("Next 32 HEXs from the forged ciphertext: " + new_ciphertext_hex[32:64])
print("Further 32 HEXs from the forged ciphertext: " + new_ciphertext_hex[64:96])
print("Final HEXs from the forged ciphertext: " + new_ciphertext_hex[96:])