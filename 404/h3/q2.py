# Convert the hex-encoded ciphertext to bytes
original_ciphertext = bytes.fromhex('373AEE2B9862A0C683E4E05380E368ECFED5A47D7E48F1A695804517C4385E08')

# Convert the original and target messages to bytes
original_message = b"Pay Ann $25"
target_message = b"Pay me $900"

# Ensure both messages are the same length
assert len(original_message) == len(target_message), "Messages must be of equal length."

# Calculate the new IV by XORing the old IV with the XOR of the original and target messages
new_iv = bytes(a ^ b ^ c for a, b, c in zip(original_ciphertext[:len(original_message)], original_message, target_message))

# Construct the new ciphertext with the new IV and the original second block
new_ciphertext = new_iv + original_ciphertext[len(original_message):]

# Print the new hex-encoded ciphertext
print(new_ciphertext.hex())
