def custom_hash(input_bytes: bytes) -> bytes:
    if not isinstance(input_bytes, bytes):
        raise TypeError("Input must be bytes")

    h = [
        0x6a09e667, 0xbb67ae85, 0x3c6ef372, 0xa54ff53a,
        0x510e527f, 0x9b05688c, 0x1f83d9ab, 0x5be0cd19
    ]
    
    k = [
        0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5, 0x3956c25b, 0x59f111f1, 0x923f82a4, 0xab1c5ed5,
        0xd807aa98, 0x12835b01, 0x243185be, 0x550c7dc3, 0x72be5d74, 0x80deb1fe, 0x9bdc06a7, 0xc19bf174,
        0xe49b69c1, 0xefbe4786, 0x0fc19dc6, 0x240ca1cc, 0x2de92c6f, 0x4a7484aa, 0x5cb0a9dc, 0x76f988da,
        0x983e5152, 0xa831c66d, 0xb00327c8, 0xbf597fc7, 0xc6e00bf3, 0xd5a79147, 0x06ca6351, 0x14292967,
        0x27b70a85, 0x2e1b2138, 0x4d2c6dfc, 0x53380d13, 0x650a7354, 0x766a0abb, 0x81c2c92e, 0x92722c85,
        0xa2bfe8a1, 0xa81a664b, 0xc24b8b70, 0xc76c51a3, 0xd192e819, 0xd6990624, 0xf40e3585, 0x106aa070,
        0x19a4c116, 0x1e376c08, 0x2748774c, 0x34b0bcb5, 0x391c0cb3, 0x4ed8aa4a, 0x5b9cca4f, 0x682e6ff3,
        0x748f82ee, 0x78a5636f, 0x84c87814, 0x8cc70208, 0x90befffa, 0xa4506ceb, 0xbef9a3f7, 0xc67178f2
    ]
    
    length = len(input_bytes) * 8
    input_bytes += b'\x80'
    while (len(input_bytes) * 8 + 64) % 512 != 0:
        input_bytes += b'\x00'
    input_bytes += length.to_bytes(8, 'big')
    
    for i in range(0, len(input_bytes), 64):
        block = input_bytes[i:i+64]
        w = [0] * 64
        
        for t in range(16):
            w[t] = int.from_bytes(block[t*4:t*4+4], 'big')
        for t in range(16, 64):
            s0 = (right_rotate(w[t-15], 7) ^ right_rotate(w[t-15], 18) ^ (w[t-15] >> 3))
            s1 = (right_rotate(w[t-2], 17) ^ right_rotate(w[t-2], 19) ^ (w[t-2] >> 10))
            w[t] = (w[t-16] + s0 + w[t-7] + s1) & 0xFFFFFFFF
        
        a, b, c, d, e, f, g, hh = h
        
        for t in range(64):
            S1 = (right_rotate(e, 6) ^ right_rotate(e, 11) ^ right_rotate(e, 25))
            ch = (e & f) ^ ((~e) & g)
            temp1 = (hh + S1 + ch + k[t] + w[t]) & 0xFFFFFFFF
            S0 = (right_rotate(a, 2) ^ right_rotate(a, 13) ^ right_rotate(a, 22))
            maj = (a & b) ^ (a & c) ^ (b & c)
            temp2 = (S0 + maj) & 0xFFFFFFFF
            
            hh = g
            g = f
            f = e
            e = (d + temp1) & 0xFFFFFFFF
            d = c
            c = b
            b = a
            a = (temp1 + temp2) & 0xFFFFFFFF
        
        h[0] = (h[0] + a) & 0xFFFFFFFF
        h[1] = (h[1] + b) & 0xFFFFFFFF
        h[2] = (h[2] + c) & 0xFFFFFFFF
        h[3] = (h[3] + d) & 0xFFFFFFFF
        h[4] = (h[4] + e) & 0xFFFFFFFF
        h[5] = (h[5] + f) & 0xFFFFFFFF
        h[6] = (h[6] + g) & 0xFFFFFFFF
        h[7] = (h[7] + hh) & 0xFFFFFFFF
    
    return b''.join(x.to_bytes(4, 'big') for x in h)

def right_rotate(value, shift):
    """Циклический сдвиг вправо"""
    return (value >> shift) | (value << (32 - shift)) & 0xFFFFFFFF

if __name__ == "__main__":
    print("Введите строку для хеширования:")
    user_input = input().strip()
    
    try:
        input_bytes = user_input.encode('utf-8')
    except UnicodeEncodeError:
        print("Ошибка: Невозможно закодировать ввод в UTF-8")
        exit(1)
    
    hashed = custom_hash(input_bytes)
    
    print("\nРезультат хеширования:")
    print(f"Входная строка: {user_input}")
    print(f"Хэш (hex): {hashed.hex()}")
    print(f"Длина хэша: {len(hashed)} байт")