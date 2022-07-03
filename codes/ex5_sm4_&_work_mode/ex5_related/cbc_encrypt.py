import os

# FK
FK0 = 'A3B1BAC6'
FK1 = '56AA3350'
FK2 = '677D9197'
FK3 = 'B27022DC'

# CK
CK = [
    '00070e15', '1c232a31', '383f464d', '545b6269',
    '70777e85', '8c939aa1', 'a8afb6bd', 'c4cbd2d9',
    'e0e7eef5', 'fc030a11', '181f262d', '343b4249',
    '50575e65', '6c737a81', '888f969d', 'a4abb2b9',
    'c0c7ced5', 'dce3eaf1', 'f8ff060d', '141b2229',
    '30373e45', '4c535a61', '686f767d', '848b9299',
    'a0a7aeb5', 'bcc3cad1', 'd8dfe6ed', 'f4fb0209',
    '10171e25', '2c333a41', '484f565d', '646b7279'
]

# Sbox
Sbox = [
    0xd6, 0x90, 0xe9, 0xfe, 0xcc, 0xe1, 0x3d, 0xb7, 0x16, 0xb6, 0x14, 0xc2, 0x28, 0xfb, 0x2c, 0x05,
    0x2b, 0x67, 0x9a, 0x76, 0x2a, 0xbe, 0x04, 0xc3, 0xaa, 0x44, 0x13, 0x26, 0x49, 0x86, 0x06, 0x99,
    0x9c, 0x42, 0x50, 0xf4, 0x91, 0xef, 0x98, 0x7a, 0x33, 0x54, 0x0b, 0x43, 0xed, 0xcf, 0xac, 0x62,
    0xe4, 0xb3, 0x1c, 0xa9, 0xc9, 0x08, 0xe8, 0x95, 0x80, 0xdf, 0x94, 0xfa, 0x75, 0x8f, 0x3f, 0xa6,
    0x47, 0x07, 0xa7, 0xfc, 0xf3, 0x73, 0x17, 0xba, 0x83, 0x59, 0x3c, 0x19, 0xe6, 0x85, 0x4f, 0xa8,
    0x68, 0x6b, 0x81, 0xb2, 0x71, 0x64, 0xda, 0x8b, 0xf8, 0xeb, 0x0f, 0x4b, 0x70, 0x56, 0x9d, 0x35,
    0x1e, 0x24, 0x0e, 0x5e, 0x63, 0x58, 0xd1, 0xa2, 0x25, 0x22, 0x7c, 0x3b, 0x01, 0x21, 0x78, 0x87,
    0xd4, 0x00, 0x46, 0x57, 0x9f, 0xd3, 0x27, 0x52, 0x4c, 0x36, 0x02, 0xe7, 0xa0, 0xc4, 0xc8, 0x9e,
    0xea, 0xbf, 0x8a, 0xd2, 0x40, 0xc7, 0x38, 0xb5, 0xa3, 0xf7, 0xf2, 0xce, 0xf9, 0x61, 0x15, 0xa1,
    0xe0, 0xae, 0x5d, 0xa4, 0x9b, 0x34, 0x1a, 0x55, 0xad, 0x93, 0x32, 0x30, 0xf5, 0x8c, 0xb1, 0xe3,
    0x1d, 0xf6, 0xe2, 0x2e, 0x82, 0x66, 0xca, 0x60, 0xc0, 0x29, 0x23, 0xab, 0x0d, 0x53, 0x4e, 0x6f,
    0xd5, 0xdb, 0x37, 0x45, 0xde, 0xfd, 0x8e, 0x2f, 0x03, 0xff, 0x6a, 0x72, 0x6d, 0x6c, 0x5b, 0x51,
    0x8d, 0x1b, 0xaf, 0x92, 0xbb, 0xdd, 0xbc, 0x7f, 0x11, 0xd9, 0x5c, 0x41, 0x1f, 0x10, 0x5a, 0xd8,
    0x0a, 0xc1, 0x31, 0x88, 0xa5, 0xcd, 0x7b, 0xbd, 0x2d, 0x74, 0xd0, 0x12, 0xb8, 0xe5, 0xb4, 0xb0,
    0x89, 0x69, 0x97, 0x4a, 0x0c, 0x96, 0x77, 0x7e, 0x65, 0xb9, 0xf1, 0x09, 0xc5, 0x6e, 0xc6, 0x84,
    0x18, 0xf0, 0x7d, 0xec, 0x3a, 0xdc, 0x4d, 0x20, 0x79, 0xee, 0x5f, 0x3e, 0xd7, 0xcb, 0x39, 0x48,
]


# xor for 32 bit (input a0 & a1 for hex)
def xor_32(a0, a1):
    return '{:08x}'.format(int(a0, 16) ^ int(a1, 16))


# nonlinear transformation - τ (return B = (b0, b1, b2, b3))
def tao(A):
    b0 = '{:02x}'.format(Sbox[int(A[0:2], 16)])
    b1 = '{:02x}'.format(Sbox[int(A[2:4], 16)])
    b2 = '{:02x}'.format(Sbox[int(A[4:6], 16)])
    b3 = '{:02x}'.format(Sbox[int(A[6:8], 16)])
    return b0 + b1 + b2 + b3


# linear transformation - L (return C = L(B))
def L_encrypt(B):
    B = '{:032b}'.format(int(B, 16))
    B_2 = B[2:] + B[:2]
    B_10 = B[10:] + B[:10]
    B_18 = B[18:] + B[:18]
    B_24 = B[24:] + B[:24]
    return '{:08x}'.format(int(B, 2) ^ int(B_2, 2) ^ int(B_10, 2) ^ int(B_18, 2) ^ int(B_24, 2))


# linear transformation - L (return C = L(B))
def L_extendkey(B):
    B = '{:032b}'.format(int(B, 16))
    B_13 = B[13:] + B[:13]
    B_23 = B[23:] + B[:23]
    return '{:08x}'.format(int(B, 2) ^ int(B_13, 2) ^ int(B_23, 2))


# wheel function - F_ (return X4 = F_(X, rk))
# mode=0: encrypt mode=1: decrypt
def F_(X, rk, mode):
    X0, X1, X2, X3 = X[0:8], X[8:16], X[16:24], X[24:32]
    if mode == 'encrypt':
        C = L_encrypt(tao('{:08x}'.format(int(rk, 16) ^ int(X1, 16) ^ int(X2, 16) ^ int(X3, 16))))
    else:
        C = L_extendkey(tao('{:08x}'.format(int(rk, 16) ^ int(X1, 16) ^ int(X2, 16) ^ int(X3, 16))))
    return xor_32(C, X0)


def Extendkey(MK):
    MK0, MK1, MK2, MK3 = MK[0:8], MK[8:16], MK[16:24], MK[24:32]
    K0 = xor_32(MK0, FK0)
    K1 = xor_32(MK1, FK1)
    K2 = xor_32(MK2, FK2)
    K3 = xor_32(MK3, FK3)
    K = [K0, K1, K2, K3]
    rk = []
    for i in range(0, 32):
        a = F_(K[i] + K[i + 1] + K[i + 2] + K[i + 3], CK[i], 'extendkey')
        K.append(a)
        rk.append(a)
    return rk


def Encrypt(X, MK):
    X0, X1, X2, X3 = X[0:8], X[8:16], X[16:24], X[24:32]
    rk = Extendkey(MK)
    X_list = [X0, X1, X2, X3]
    for i in range(0, 32):
        X_list.append(F_(X_list[i] + X_list[i + 1] + X_list[i + 2] + X_list[i + 3], rk[i], 'encrypt'))
    Y = ''
    for i in range(0, 4):
        Y += X_list[35 - i]
    return Y


def Decrypt(Y, MK):
    Y0, Y1, Y2, Y3 = Y[0:8], Y[8:16], Y[16:24], Y[24:32]
    rk = Extendkey(MK)
    Y_list = [Y0, Y1, Y2, Y3]
    for i in range(0, 32):
        Y_list.append(F_(Y_list[i] + Y_list[i + 1] + Y_list[i + 2] + Y_list[i + 3], rk[31 - i], 'encrypt'))
    X = ''
    for i in range(0, 4):
        X += Y_list[35 - i]
    return X


def xor(a, b):
    return hex(int(a, 16) ^ int(b, 16))[2:].zfill(32)


def CBC_encrypt(s, k, iv):
    # PKCS#7填充
    a = (32 - (len(s) % 32)) // 2
    for i in range(a):
        s += hex(a)[2:].zfill(2)
    # CBC工作模式
    s_ecb = ''
    for i in range(len(s) // 32):
        iv = Encrypt(xor(s[32 * i:32 * (i + 1)], iv), k)
        s_ecb += iv
    return s_ecb


def CBC_decrypt(s, k, iv):
    s_ecb = ''
    for i in range(len(s) // 32):
        if i:
            iv = s[32 * (i - 1):32 * i]
        m = xor(iv, Decrypt(s[32 * i:32 * (i + 1)], k))
        s_ecb += m
    # PKCS#7填充
    a = int(s_ecb[-2:], 16)
    s_ecb = s_ecb[:-2 * a]
    return s_ecb


def print_s(s):
    for i in range(len(s) // 2):
        if (i + 1) % 16 == 0:
            print('0x' + s[2 * i:2 * (i + 1)], end='\n')
        else:
            print('0x' + s[2 * i:2 * (i + 1)], end=' ')


def fileload(filename):
    file_pth = os.path.dirname(__file__) + '/' + filename
    file_in = os.open(file_pth, os.O_BINARY | os.O_RDONLY)
    file_size = os.stat(file_in)[6]
    data = os.read(file_in, file_size)
    os.close(file_in)
    return data


def filesave(data_after, filename):
    file_pth = os.path.dirname(__file__) + '/' + filename
    file_open = os.open(file_pth, os.O_WRONLY | os.O_CREAT | os.O_BINARY)
    os.write(file_open, data_after)
    os.close(file_open)


t = fileload('figures/figure.bmp')
s = ''
# 前54字节为
for i in range(54, len(t)):
    s += hex(t[i])[2:].zfill(2)
# print(s)
# 密钥
k = '9241921686391cf123780b56ced56fdc'
iv = 'a8638d2fb23cc49206edd7c84532eaab'
c = CBC_encrypt(s, k, iv)
# print(c)
# 加密后的bytes
c_bytes = b''
for i in range(0, len(t) - 54):
    c_bytes += (int(c[2 * i:2 * (i + 1)], 16).to_bytes(length=1, byteorder='big'))
# print(c_bytes)

# 加上文件头
c_bytes = t[0:54] + c_bytes
print(c_bytes)
filesave(c_bytes, 'figures/figure_cbc.bmp')
