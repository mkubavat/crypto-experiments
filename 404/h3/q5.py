import struct

def left_circular_shift(n, d, w=32):
    # Ensure the shift amount is positive
    d = d % w
    return ((n << d) | (n >> (w - d))) & ((1 << w) - 1)

def right_circular_shift(n, d, w=32):
    # Ensure the shift amount is positive
    d = d % w
    return ((n >> d) | (n << (w - d))) & ((1 << w) - 1)

def hash_function_final(data: bytes, key_hex: str) -> str:
    """Hash function as described in the pseudocode using the key as a hex string."""
    key = int(key_hex, 16)
    
    # Padding the data
    L = len(data) * 8  # Length of data in bits
    padded_data = data + b'\x80' + b'\x00' * ((-len(data) - 9) % 64) + struct.pack('!Q', L)
    
    # Initializing hash parameters directly from hex values
    a = left_circular_shift(int('6148a3b6', 16), key, 32)
    b = right_circular_shift(int('a5472a5d', 16), key, 32)
    c = left_circular_shift(int('516ed6e1', 16), key, 32)
    d = right_circular_shift(int('02246c86', 16), key, 32)
    
    # Process each 128-bit block
    p = [5, 11, 17, 23, 31]
    for i in range(0, len(padded_data), 16):
        block = padded_data[i:i+16]
        b0, b1, b2, b3 = struct.unpack('!LLLL', block)
        for _ in range(32):
            at = left_circular_shift(d ^ b2, p[b % 5], 32)
            bt = right_circular_shift(a ^ b3, p[c % 5], 32)
            ct = left_circular_shift(b ^ b0, p[d % 5], 32)
            dt = right_circular_shift(c ^ b1, p[a % 5], 32)
            
            a = at + dt
            b = bt + at
            c = ct + bt
            d = dt + ct

    # Concatenate the hash values to form the final 128-bit number
    number_bytes = a.to_bytes(4, 'big') + b.to_bytes(4, 'big') + c.to_bytes(4, 'big') + d.to_bytes(4, 'big')
    number = int.from_bytes(number_bytes, 'big')

    # Perform the final bit rotation on the number
    digest = left_circular_shift(number, (number * key) % 128, 128)
    
    return format(digest, '032x')

# Example usage
data_example = "Hello CryptoLab".encode()
key_example = "b9827426"

# Compute the digest
digest_hex = hash_function_final(data_example, key_example)
digest_hex
