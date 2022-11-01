#!/usr/bin/env python3

from diffAttack import differentialAttack,calcolaCombinazioni,sbox_esercizio
from spn import encrypt,keyschedule
x1 = [2,6,11,7]
x2 = [3,4,1,14]
k = [3,10,9,4,9,4,3,15]

key = differentialAttack(calcolaCombinazioni(9),sbox_esercizio)
print(key)

print("x1: ", x1)
print("x2: ", x2)
print("crittiamo x1 e x2 usando chiave k!")

y1 = encrypt(x1,sbox_esercizio,keyschedule(k))
y2 = encrypt(x2,sbox_esercizio,keyschedule(k))


def searchKey(x,z,y,yy):
    print("inizio bruteforce")
    for x1 in range(0,16):
        print(x1)
        for x2 in range(0,16):
            for x3 in range(0,16):
                for x4 in range(0,16):
                    for x7 in range(0,16):
                        for x8 in range(0,16):
                            k = [x1,x2,x3,x4,key[0],key[1],x7,x8]
                            y1 = encrypt(x,sbox_esercizio,keyschedule(k))
                            y2 = encrypt(z,sbox_esercizio,keyschedule(k))
                            if y[0] == y1[0] and y[1] == y1[1] and y[2] == y1[2] and y[3] == y1[3]:
                                if yy[0] == y2[0] and yy[1] == y2[1] and yy[2] == y2[2] and yy[3] == y2[3]:
                                    print("found!!!")
                                    return k

k2 = searchKey(x1,x2,y1,y2)
print(k2)

