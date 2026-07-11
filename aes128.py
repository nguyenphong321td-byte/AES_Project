import hashlib
S_BOX = [
0x63,0x7C,0x77,0x7B,0xF2,0x6B,0x6F,0xC5,0x30,0x01,0x67,0x2B,0xFE,0xD7,0xAB,0x76,
0xCA,0x82,0xC9,0x7D,0xFA,0x59,0x47,0xF0,0xAD,0xD4,0xA2,0xAF,0x9C,0xA4,0x72,0xC0,
0xB7,0xFD,0x93,0x26,0x36,0x3F,0xF7,0xCC,0x34,0xA5,0xE5,0xF1,0x71,0xD8,0x31,0x15,
0x04,0xC7,0x23,0xC3,0x18,0x96,0x05,0x9A,0x07,0x12,0x80,0xE2,0xEB,0x27,0xB2,0x75,0x09,0x83,0x2C,0x1A,0x1B,0x6E,0x5A,0xA0,0x52,0x3B,0xD6,0xB3,0x29,0xE3,0x2F,0x84,
0x53,0xD1,0x00,0xED,0x20,0xFC,0xB1,0x5B,0x6A,0xCB,0xBE,0x39,0x4A,0x4C,0x58,0xCF,
0xD0,0xEF,0xAA,0xFB,0x43,0x4D,0x33,0x85,0x45,0xF9,0x02,0x7F,0x50,0x3C,0x9F,0xA8,
0x51,0xA3,0x40,0x8F,0x92,0x9D,0x38,0xF5,0xBC,0xB6,0xDA,0x21,0x10,0xFF,0xF3,0xD2,0xCD,0x0C,0x13,0xEC,0x5F,0x97,0x44,0x17,0xC4,0xA7,0x7E,0x3D,0x64,0x5D,0x19,0x73,
0x60,0x81,0x4F,0xDC,0x22,0x2A,0x90,0x88,0x46,0xEE,0xB8,0x14,0xDE,0x5E,0x0B,0xDB,
0xE0,0x32,0x3A,0x0A,0x49,0x06,0x24,0x5C,0xC2,0xD3,0xAC,0x62,0x91,0x95,0xE4,0x79,
0xE7,0xC8,0x37,0x6D,0x8D,0xD5,0x4E,0xA9,0x6C,0x56,0xF4,0xEA,0x65,0x7A,0xAE,0x08,0xBA,0x78,0x25,0x2E,0x1C,0xA6,0xB4,0xC6,0xE8,0xDD,0x74,0x1F,0x4B,0xBD,0x8B,0x8A,
0x70,0x3E,0xB5,0x66,0x48,0x03,0xF6,0x0E,0x61,0x35,0x57,0xB9,0x86,0xC1,0x1D,0x9E,
0xE1,0xF8,0x98,0x11,0x69,0xD9,0x8E,0x94,0x9B,0x1E,0x87,0xE9,0xCE,0x55,0x28,0xDF,
0x8C,0xA1,0x89,0x0D,0xBF,0xE6,0x42,0x68,0x41,0x99,0x2D,0x0F,0xB0,0x54,0xBB,0x16
]

RCON = [
    0x01, 0x02, 0x04, 0x08,
    0x10, 0x20, 0x40, 0x80,
    0x1B, 0x36
]

def rot_word(word):
    return word[1:] + word[:1]

def sub_word(word):
    return [S_BOX[x] for x in word]

def xor_word(word1, word2):
    result = []

    for i in range(4):
        result.append(word1[i] ^ word2[i])

    return result
def key_expansion(key_words):

    words = [word[:] for word in key_words]

    round_num = 0

    while len(words) < 44:

        temp = words[-1][:]

        if len(words) % 4 == 0:

            temp = rot_word(temp)
            temp = sub_word(temp)

            temp[0] ^= RCON[round_num]

            round_num += 1

        new_word = xor_word(words[-4], temp)

        words.append(new_word)

    return words

def sub_bytes(state):
    for i in range(4):
        for j in range(4):
            state[i][j] = S_BOX[state[i][j]]
    return state


def shift_rows(state):
    state[1] = state[1][1:] + state[1][:1]
    state[2] = state[2][2:] + state[2][:2]
    state[3] = state[3][3:] + state[3][:3]
    return state

def gmul(a, b):
    p = 0

    for i in range(8):
        if b & 1:
            p ^= a
        hi_bit = a & 0x80
        a <<= 1
        if hi_bit:
            a ^= 0x1b
        b >>= 1
    return p & 0xff
def mix_columns(state):
    for i in range(4):
        a = state[i][:]
        
        state[i][0] = (gmul(a[0], 2) ^ gmul(a[1], 3) ^ a[2] ^ a[3])
        state[i][1] = (a[0] ^ gmul(a[1], 2) ^ gmul(a[2], 3) ^ a[3])
        state[i][2] = (a[0] ^ a[1] ^ gmul(a[2], 2) ^ gmul(a[3], 3))
        state[i][3] = (gmul(a[0], 3) ^ a[1] ^ a[2] ^ gmul(a[3], 2))

    return state
def add_round_key(state, round_key):
    for i in range(4):
        for j in range(4):
            state[i][j] ^= round_key[i][j]

    return state
def generate_key(full_name):
    return hashlib.sha256(full_name.encode("utf-8")).digest()[:16]

def create_state(text_bytes):
    state = []

    for i in range(0, 16, 4):
        state.append(list(text_bytes[i:i+4]))

    return state

def split_key(aes_key):
    words = []

    for i in range(0, 16, 4):
        words.append(list(aes_key[i:i+4]))

    return words


def main():
    name = "Nguyễn Văn Hồng Phong"
    plaintext = "NGVANHONGPHONG00"

    sha256_hash = hashlib.sha256(name.encode("utf-8")).hexdigest().upper()
    aes_key = generate_key(name)

    plaintext_bytes = plaintext.encode("utf-8")
    state = create_state(plaintext_bytes)

    key_words = split_key(aes_key)
    all_words = key_expansion(key_words)
    round_keys = []

    for i in range(0, len(all_words), 4):
        round_keys.append(all_words[i:i+4])

    state = add_round_key(state, round_keys[0])

    print("After Initial AddRoundKey")
    print(state)

    for r in range(1, 10):
        state = sub_bytes(state)
        state = shift_rows(state)
        state = mix_columns(state)
        state = add_round_key(state, round_keys[r])
        print("Round", r)
        print(state)

    state = sub_bytes(state)
    state = shift_rows(state)
    state = add_round_key(state, round_keys[10])

    print("Ciphertext")
    print(state)

    print("Student Name :", name)
    print("SHA-256 Hash :", sha256_hash)
    print("AES-128 Key  :", aes_key.hex().upper())
    print("\nPlaintext    :", plaintext)
    print("Plaintext HEX:", plaintext_bytes.hex().upper())

    print("\n========== STATE MATRIX ==========")
    for row in state:
        print(" ".join(f"{x:02X}" for x in row))

    print("\n========== SUB BYTES ==========")
    state = sub_bytes(state)
    for row in state:
        print(" ".join(f"{x:02X}" for x in row))

    print("\n========== SHIFT ROWS ==========")
    state = shift_rows(state)
    for row in state:
        print(" ".join(f"{x:02X}" for x in row))

    print("\n========== MIX COLUMNS ==========")
    state = mix_columns(state)
    for row in state:
        print(" ".join(f"{x:02X}" for x in row))

    print("\n========== ORIGINAL KEY ==========")
    for word in key_words:
        print(" ".join(f"{x:02X}" for x in word))

    print("\n========== KEY EXPANSION ==========")
    for i, word in enumerate(all_words):
        print(f"W{i:02}: ", end="")
        print(" ".join(f"{b:02X}" for b in word))

if __name__ == "__main__":
    main()