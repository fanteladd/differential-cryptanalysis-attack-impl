from utils import binToInt,intToBin,sboxInverse

"""
data una lista contenente 4 numeri a 4 bit,
restituisce una lista contenente 4 numeri a 4 bit tale che essa è la permutazione secondo l'spn definito
della lista in input
"""
def permutation(x):
    binary = intToBin(x)
    permuted = []
    for i in range(0,4):
        permuted.append(binary[0+i])
        permuted.append(binary[4+i])
        permuted.append(binary[8+i])
        permuted.append(binary[12+i])
    permuted = binToInt(permuted)
    return permuted

def inv_permutation(x):
    binary = intToBin(x)
    permuted = []
    for i in reversed(range(0,4)):
        permuted.append(binary[3-i])
        permuted.append(binary[7-i])
        permuted.append(binary[11-i])
        permuted.append(binary[15-i])
    permuted = binToInt(permuted)
    return permuted

"""
Data una chiave a 32 bit, ossia una lista dove ogni elemento della lista è un numero a 4 bit,
restituisce una lista di 5 chiavi a 16 bit, dove la i+1-esima chiave è la round key per il round i+1
"""
def keyschedule(k):
    listkey = []
    for i in range(0,5):
        ki = list(k[i:i+4])
        listkey.append(ki)
    return listkey


"""
Dato un plain text di 16 bit, una sbox e una lista contenente la key schedule data da una chiave k,
restituisce un ciphertext di 16 bit ottenuto usando la chiave k
"""
def encrypt(x,sbox,keyschedule):
    u = x.copy()
    for r in range(0,3):
        for i in range(0,len(u)):
            u[i] = (sbox[u[i] ^ keyschedule[r][i]])
        u = permutation(u)
    for i in range(0,len(u)):
        u[i] = (sbox[u[i] ^ keyschedule[3][i]])
    for i in range(0,len(u)):
        u[i] = (u[i] ^ keyschedule[4][i])
    return u

"""
Dato un cipher text di 16 bit, una sbox e una lista contenente la key schedule data da una chiave k,
restituisce un plain text di 16 bit ottenuto usando la chiave k
"""
def decrypt(y,sbox,keyschedule):
    u = y.copy()
    sbox_inv = sboxInverse(sbox) 
    for i in range(0,len(u)):
        u[i] = (u[i] ^ keyschedule[4][i])
    for i in range(0,len(u)):
        u[i] = sbox_inv[u[i]]
        u[i] = u[i] ^ keyschedule[3][i]
    for r in reversed(range(0,3)):
        u = inv_permutation(u)
        for i in range(0,len(u)):
            u[i] = sbox_inv[u[i]]
            u[i] = u[i] ^ keyschedule[r][i]
    return u
