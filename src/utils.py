from bitstring import BitArray

def intToBin(a):
    binary = []
    for i in a:
        cifraBin = []
        for j in bin(i).replace("0b",""):
            cifraBin.append(j)
        x = cifraBin[::-1]
        while len(x) < 4:
            x += '0'
        cifraBin = x[::-1]
        binary += cifraBin
    return binary

def binToInt(a):
    b = []
    for i in a:
        b.append(int(i))
    intt = []
    i = 0
    for i in range(3, len(a), 4):
        bitlist = b[i-3:i+1]
        c = BitArray(bitlist)
        intt.append(c.uint)
    return intt

def sboxInverse(sbox):
    inv_sbox = {}
    for k,v in sbox.items():
        inv_sbox[v] = k
    return inv_sbox 
