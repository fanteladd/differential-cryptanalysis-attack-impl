from spn import encrypt,keyschedule
from utils import sboxInverse

# sbox_esempio = {0x0: 0xE,0x1: 0x4,0x2: 0xD,0x3: 0x1,0x4: 0x2,0x5: 0xF,0x6: 0xB,0x7: 0x8,0x8: 0x3,0x9: 0xA,0xA: 0x6,0xB: 0xC,0xC: 0x5,0xD: 0x9,0xE: 0x0,0xF: 0x7}
sbox_esercizio = {0x0: 0xE,0x1: 0x2,0x2: 0x1,0x3: 0x3,0x4: 0xD,0x5: 0x9,0x6: 0x0,0x7: 0x6,0x8: 0xF,0x9: 0x4,0xA: 0x5,0xB: 0xA,0xC: 0x8,0xD: 0xC,0xE: 0x7,0xF: 0xB}

"""
punto a: generazione tabella contenente i valori di Nd
"""
a = [0x0,0x1,0x2,0x3,0x4,0x5,0x6,0x7,0x8,0x9,0xA,0xB,0xC,0xD,0xE,0xF]

t = []

for k in range(0,len(a)):
    delta = []
    for i in a:
        for j in a:
            if hex(i ^ j) == hex(a[k]):
                delta.append(j)
    t.append(delta)

d = []

# zeros matrix
for i in range(0,len(a)):
    e = []
    for j in range(0,len(a)):
        e.append(0)
    d.append(e)


for i in range(0,len(a)):
    for j in range(0,len(a)):
        p = ( sbox_esercizio[a[j]] ^ sbox_esercizio[t[i][j]] )
        d[i][p] += 1

for i in d:
    print(i)

"""
punto d: implementazione dell'attacco
"""

x1 = [2,6,11,7]
x2 = [3,4,1,14]
k = [3,10,9,4,13,6,3,15]
k1 = [0, 0, 0, 0, 5, 0, 12, 12]

def differentialAttack(T,sbox):
    sbox_inv = sboxInverse(sbox) 
    count = []
    for l1 in range(0,16):
        countRow = []
        for l2 in range(0,16):
            countRow.append(0)
        count.append(countRow)

    for (_,y,_,ystar) in T:
        if(y[2] == ystar[2] and y[3] == ystar[3]):
            for l1 in range(0,16):
                for l2 in range(0,16):
                    u4_1 = sbox_inv[l1 ^ y[0]]
                    u4_2 = sbox_inv[l2 ^ y[1]]
                    ustar4_1 = sbox_inv[l1 ^ ystar[0]]
                    ustar4_2 = sbox_inv[l2 ^ ystar[1]]
                    u4_1p = u4_1 ^ ustar4_1
                    u4_2p = u4_2 ^ ustar4_2
                    if u4_1p == 1 and u4_2p == 1:
                        count[l1][l2] += 1
    max = -1
    for l1 in range(0,16):
        for l2 in range(0,16):
            if (count[l1][l2] > max):
                max = count[l1][l2]
                maxkey = (l1,l2)
    return maxkey

"""
Dato in input un numero x a 4 bit,
restituisce tutte le coppie di numeri a 4 bit tali che la loro differenza è proprio x
"""
def deltaX(x):
    my_deltaX = []
    for i in range(0,16):
        my_deltaX.append((i,x^i))
    return my_deltaX

"""
Generatore di quadruple del tipo (x,x*,y,y*), strettamente specifico per il nostro attacco
"""

def calcolaCombinazioni(x_p):
    print("inizio generazione parole")
    delta_x_p = deltaX(x_p)
    combinazioni = []

    for (x1,x1_s) in delta_x_p:
        for x2 in range(0,16):
            for x3 in range(0,16):
                for (x4,x4_s) in delta_x_p:
                    x = [x1,x2,x3,x4]
                    x_s= [x1_s,x2,x3,x4_s]
                    y = encrypt(x,sbox_esercizio,keyschedule(k))
                    y_s= encrypt(x_s,sbox_esercizio,keyschedule(k))
                    combinazioni.append((x,y,x_s,y_s))
                    if (x2 != x3):
                        x = [x1,x3,x2,x4]
                        x_s = [x1_s,x3,x2,x4_s]
                        y = encrypt(x,sbox_esercizio,keyschedule(k))
                        y_s = encrypt(x_s,sbox_esercizio,keyschedule(k))
                        combinazioni.append((x,y,x_s,y_s))

    print("fine generazione parole")
    return combinazioni


key = differentialAttack(calcolaCombinazioni(9),sbox_esercizio)
print(key)

# print("x1: ", x1)
# print("x2: ", x2)
# print("crittiamo x1 e x2 usando chiave k!")

# y1 = encrypt(x1,sbox_esempio,keyschedule(k))
# y2 = encrypt(x2,sbox_esempio,keyschedule(k))

# print("x1 crittato con chiave k: y1 = ", y1)
# print("x2 crittato con chiave k: y2 = ", y2)
# print("\n")
# print("crittiamo x1 e x2 usando chiave k1!")
# y3 = encrypt(x1,sbox_esempio,keyschedule(k1))
# y4 = encrypt(x2,sbox_esempio,keyschedule(k1))
# print("x1 crittato con chiave k1: y3 = ", y3)
# print("x2 crittato con chiave k1: y4 = ", y4)
# print("\n")


# print("y1: ", y1)
# print("y2: ", y2)
# print("decrittiamo y1 e y2 usando chiave k1!")
# h1 = decrypt(y1,sbox_esempio,keyschedule(k1))
# h2 = decrypt(y2,sbox_esempio,keyschedule(k1))
# print("y1 decrittato con chiave k: ", h1)
# print("y2 decrittato con chiave k: ", h2)
# print("\n")
# print("y3: ", y3)
# print("y4: ", y4)
# print("decrittiamo y3 e y4 usando chiave k!")
# h3 = decrypt(y3,sbox_esempio,keyschedule(k))
# h4 = decrypt(y4,sbox_esempio,keyschedule(k))
# print("y3 decrittato con chiave k: ", h3)
# print("y4 decrittato con chiave k: ", h4)
# print("\n")

# def searchKey(x,y):
#     print("inizio bruteforce")
#     for x1 in range(0,16):
#         for x2 in range(0,16):
#             for x3 in range(0,16):
#                 for x4 in range(0,16):
#                     for x5 in range(0,16):
#                         for x6 in range(0,16):
#                             for x7 in range(0,16):
#                                 for x8 in range(0,16):
#                                     k = [x1,x2,x3,x4,x5,x6,x7,x8]
#                                     y1 = encrypt(x,sbox_esempio,keyschedule(k))
#                                     if y[0] == y1[0] and y[1] == y1[1] and y[2] == y1[2] and y[3] == y1[3]:
#                                         print("found!!!")
#                                         print(y1)
#                                         return k

# k2 = searchKey(a,y)
# print(k2)

# z = encrypt(b,sbox_esempio,keyschedule(k2))
# print("z con chiave k1")
# print(z)
