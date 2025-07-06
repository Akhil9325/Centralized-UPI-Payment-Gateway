import time

def rol(x, r, bits=32):
    return ((x << r) & ((1 << bits) - 1)) | (x >> (bits - r))

def ror(x, r, bits=32):
    return (x >> r) | ((x << (bits - r)) & ((1 << bits) - 1))

def speck64_key_schedule(key_words, rounds=27):
    alpha = 8
    beta = 3
    keys = [key_words[0]]
    l = list(key_words[1:])
    for i in range(rounds - 1):
        new_k = ((ror(l[i], beta, 32) + keys[i]) % (1 << 32)) ^ i
        keys.append(new_k)
        new_l = rol(keys[i], alpha, 32) ^ new_k
        l.append(new_l)
    return keys

def speck64_encrypt(plaintext, key):
    rounds = 27
    alpha = 8
    beta = 3
    mask32 = (1 << 32) - 1
    x = (plaintext >> 32) & mask32
    y = plaintext & mask32
    key_words = [
        (key >> 96) & mask32,
        (key >> 64) & mask32,
        (key >> 32) & mask32,
        key & mask32,
    ]
    round_keys = speck64_key_schedule(key_words, rounds)
    for k in round_keys:
        x = (((ror(x, beta, 32) + y) % (1 << 32)) ^ k) & mask32
        y = (rol(y, alpha, 32) ^ x) & mask32
    ciphertext = (x << 32) | y
    return ciphertext

def encrypt_merchant_id_speck(mid):
    """
    Encrypts the Merchant ID using SPECK64/128.
    mid: A 16-character hex string.
    Returns a 16-character hex string ciphertext.
    """
    plaintext = int(mid, 16)
    key = 0x0F0E0D0C0B0A09080706050403020100
    ciphertext = speck64_encrypt(plaintext, key)
    encrypted = format(ciphertext, '016x')
    return encrypted

def generate_virtual_merchant_id(mid):
    """
    Generates a Virtual Merchant ID by encrypting the Merchant ID.
    Returns a 16-character hex string.
    """
    return encrypt_merchant_id_speck(mid)
