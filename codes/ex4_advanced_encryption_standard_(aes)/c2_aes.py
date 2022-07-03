Rcon = ['', '01000000', '02000000', '04000000', '08000000', '10000000',
        '20000000', '40000000', '80000000', '1b000000', '36000000']

sbox = [[99, 124, 119, 123, 242, 107, 111, 197, 48, 1, 103, 43, 254, 215, 171, 118],
        [202, 130, 201, 125, 250, 89, 71, 240, 173, 212, 162, 175, 156, 164, 114, 192],
        [183, 253, 147, 38, 54, 63, 247, 204, 52, 165, 229, 241, 113, 216, 49, 21],
        [4, 199, 35, 195, 24, 150, 5, 154, 7, 18, 128, 226, 235, 39, 178, 117],
        [9, 131, 44, 26, 27, 110, 90, 160, 82, 59, 214, 179, 41, 227, 47, 132],
        [83, 209, 0, 237, 32, 252, 177, 91, 106, 203, 190, 57, 74, 76, 88, 207],
        [208, 239, 170, 251, 67, 77, 51, 133, 69, 249, 2, 127, 80, 60, 159, 168],
        [81, 163, 64, 143, 146, 157, 56, 245, 188, 182, 218, 33, 16, 255, 243, 210],
        [205, 12, 19, 236, 95, 151, 68, 23, 196, 167, 126, 61, 100, 93, 25, 115],
        [96, 129, 79, 220, 34, 42, 144, 136, 70, 238, 184, 20, 222, 94, 11, 219],
        [224, 50, 58, 10, 73, 6, 36, 92, 194, 211, 172, 98, 145, 149, 228, 121],
        [231, 200, 55, 109, 141, 213, 78, 169, 108, 86, 244, 234, 101, 122, 174, 8],
        [186, 120, 37, 46, 28, 166, 180, 198, 232, 221, 116, 31, 75, 189, 139, 138],
        [112, 62, 181, 102, 72, 3, 246, 14, 97, 53, 87, 185, 134, 193, 29, 158],
        [225, 248, 152, 17, 105, 217, 142, 148, 155, 30, 135, 233, 206, 85, 40, 223],
        [140, 161, 137, 13, 191, 230, 66, 104, 65, 153, 45, 15, 176, 84, 187, 22]]

inv_sbox = [[82, 9, 106, 213, 48, 54, 165, 56, 191, 64, 163, 158, 129, 243, 215, 251],
            [124, 227, 57, 130, 155, 47, 255, 135, 52, 142, 67, 68, 196, 222, 233, 203],
            [84, 123, 148, 50, 166, 194, 35, 61, 238, 76, 149, 11, 66, 250, 195, 78],
            [8, 46, 161, 102, 40, 217, 36, 178, 118, 91, 162, 73, 109, 139, 209, 37],
            [114, 248, 246, 100, 134, 104, 152, 22, 212, 164, 92, 204, 93, 101, 182, 146],
            [108, 112, 72, 80, 253, 237, 185, 218, 94, 21, 70, 87, 167, 141, 157, 132],
            [144, 216, 171, 0, 140, 188, 211, 10, 247, 228, 88, 5, 184, 179, 69, 6],
            [208, 44, 30, 143, 202, 63, 15, 2, 193, 175, 189, 3, 1, 19, 138, 107],
            [58, 145, 17, 65, 79, 103, 220, 234, 151, 242, 207, 206, 240, 180, 230, 115],
            [150, 172, 116, 34, 231, 173, 53, 133, 226, 249, 55, 232, 28, 117, 223, 110],
            [71, 241, 26, 113, 29, 41, 197, 137, 111, 183, 98, 14, 170, 24, 190, 27],
            [252, 86, 62, 75, 198, 210, 121, 32, 154, 219, 192, 254, 120, 205, 90, 244],
            [31, 221, 168, 51, 136, 7, 199, 49, 177, 18, 16, 89, 39, 128, 236, 95],
            [96, 81, 127, 169, 25, 181, 74, 13, 45, 229, 122, 159, 147, 201, 156, 239],
            [160, 224, 59, 77, 174, 42, 245, 176, 200, 235, 187, 60, 131, 83, 153, 97],
            [23, 43, 4, 126, 186, 119, 214, 38, 225, 105, 20, 99, 85, 33, 12, 125]]

# 列混淆矩阵
mix_column = [[0x02, 0x03, 0x01, 0x01],
              [0x01, 0x02, 0x03, 0x01],
              [0x01, 0x01, 0x02, 0x03],
              [0x03, 0x01, 0x01, 0x02]]
# 列混淆逆矩阵
inv_mix_column = [[0x0e, 0x0b, 0x0d, 0x09],
                  [0x09, 0x0e, 0x0b, 0x0d],
                  [0x0d, 0x09, 0x0e, 0x0b],
                  [0x0b, 0x0d, 0x09, 0x0e]]


# 有限域上不可约多项式，取不可约多项式为0x11b
# 输入为整数
def gmul(a):
    poly = 0x11b
    a <<= 1
    if (a & 0x100 == 0x100):
        a ^= poly
    return a & 0xff


def multiply(a1, a2):
    poly = 0x11b
    result = 0
    while a2 > 0:
        if (a2 & 1):
            result ^= a1
        a1 = gmul(a1)
        a2 >>= 1
    return result


# 有限域上2个4维矩阵的乘法
def matmulti(A, B):
    C = [[0] * 4 for _ in range(4)]
    for i in range(4):
        for j in range(4):
            for k in range(4):
                C[i][j] ^= multiply(A[i][k], B[k][j])
    return C


def RotWord(w):
    # w:8位16进制数
    return w[2:] + w[0:2]


def SubWord(w):
    # w:8位16进制数
    # 做4次字代换
    w_new_1 = hex(sbox[int(w[0], 16)][int(w[1], 16)])[2:].zfill(2)
    w_new_2 = hex(sbox[int(w[2], 16)][int(w[3], 16)])[2:].zfill(2)
    w_new_3 = hex(sbox[int(w[4], 16)][int(w[5], 16)])[2:].zfill(2)
    w_new_4 = hex(sbox[int(w[6], 16)][int(w[7], 16)])[2:].zfill(2)
    return w_new_1 + w_new_2 + w_new_3 + w_new_4


# 两个8位16进制数的异或，返回结果为8位16进制数
def XOR(a, b):
    return hex(int(a, 16) ^ int(b, 16))[2:].zfill(8)


def KeyExpansion(key, w, Nk):
    # key长4*Nk字节，w长Nb*(Nr+1)字
    temp = '0' * 8
    Nr = 0
    if Nk == 4:
        Nr = 10
    elif Nk == 6:
        Nr = 12
    elif Nk == 8:
        Nr = 14

    i = 0
    while i < Nk:
        w[i] = key[(8 * i): (8 * i) + 2] + key[(8 * i) + 2: (8 * i) + 4] + key[(8 * i) + 4: (8 * i) + 6] + key[(
                                                                                                                       8 * i) + 6: (
                                                                                                                                           8 * i) + 8]
        i = i + 1

    i = Nk

    while i < 4 * (Nr + 1):
        temp = w[i - 1]
        if i % Nk == 0:
            temp = XOR(SubWord((RotWord(temp))), Rcon[i // Nk])
        elif (Nk > 6) & (i % Nk == 4):
            temp = SubWord(temp)
        w[i] = XOR(w[i - Nk], temp)
        i = i + 1
    return 0


def AddRoundKey(state, w):
    # state：状态矩阵，w：4个字
    for j in range(4):
        word = state[0][j] + state[1][j] + state[2][j] + state[3][j]
        word_xor = XOR(word, w[j])
        state[0][j] = word_xor[0:2]
        state[1][j] = word_xor[2:4]
        state[2][j] = word_xor[4:6]
        state[3][j] = word_xor[6:8]
    return state


# 对状态矩阵做字节代替
def SubBytes(state):
    for i in range(4):
        for j in range(4):
            temp = state[i][j]
            state[i][j] = hex(sbox[int(temp[0], 16)][int(temp[1], 16)])[2:].zfill(2)


# 行移位
def ShiftRows(state):
    # 第0行不动
    # 第1行左移1字节
    state[1] = [state[1][1], state[1][2], state[1][3], state[1][0]]
    # 第2行左移2字节
    state[2] = [state[2][2], state[2][3], state[2][0], state[2][1]]
    # 第3行左移3字节
    state[3] = [state[3][3], state[3][0], state[3][1], state[3][2]]
    return state


# 列混淆
def MixColumns(state):
    for i in range(4):
        for j in range(4):
            state[i][j] = int(state[i][j], 16)
    afterCol = matmulti(mix_column, state)
    for i in range(4):
        for j in range(4):
            state[i][j] = afterCol[i][j]
    for i in range(4):
        for j in range(4):
            state[i][j] = hex(state[i][j])[2:].zfill(2)
    return state


# AES加密
def Encrypt(state, w, Nr):
    AddRoundKey(state, w[0:4])

    for round in range(1, Nr):
        SubBytes(state)
        ShiftRows(state)
        MixColumns(state)
        AddRoundKey(state, w[round * 4:round * 4 + 4])

    # 最后一轮不做列混淆
    SubBytes(state)
    ShiftRows(state)
    AddRoundKey(state, w[Nr * 4:Nr * 4 + 4])

    return state


# 逆字节代替
def InvSubBytes(state):
    for i in range(4):
        for j in range(4):
            temp = state[i][j]
            state[i][j] = hex(inv_sbox[int(temp[0], 16)][int(temp[1], 16)])[2:].zfill(2)


# 逆向行移位
def InvShiftRows(state):
    # 第0行不变
    # 第1行右移1位
    state[1] = [state[1][3], state[1][0], state[1][1], state[1][2]]
    # 第2行右移2位
    state[2] = [state[2][2], state[2][3], state[2][0], state[2][1]]
    # 第3行右移3位
    state[3] = [state[3][1], state[3][2], state[3][3], state[3][0]]
    return state


# 逆向列混淆
def InvMixColumns(state):
    for i in range(4):
        for j in range(4):
            state[i][j] = int(state[i][j], 16)
    afterCol = matmulti(inv_mix_column, state)
    for i in range(4):
        for j in range(4):
            state[i][j] = afterCol[i][j]
    for i in range(4):
        for j in range(4):
            state[i][j] = hex(state[i][j])[2:].zfill(2)
    return state


# AES解密
def Decrypt(state, w, Nr):
    AddRoundKey(state, w[Nr * 4:Nr * 4 + 4])

    for round in range(Nr - 1, 0, -1):
        InvShiftRows(state)
        InvSubBytes(state)
        AddRoundKey(state, w[round * 4:(round + 1) * 4])
        InvMixColumns(state)

    InvShiftRows(state)
    InvSubBytes(state)
    AddRoundKey(state, w[0:4])
    return state


def main():
    # key_length = int(input())
    T = int(input())  # 加解密次数
    s = input().strip().replace('\n', '').replace('\r', '')[2:]
    k = input().strip().replace('\n', '').replace('\r', '')[2:]
    mode = int(input())  # 加/解密模式

    # 状态矩阵 4*4 每个位置放一个字节
    state = [['0'] * 4 for _ in range(4)]
    for i in range(4):
        for j in range(4):
            state[i][j] = s[8 * j + 2 * i: 8 * j + 2 * i + 2]

    # 确定Nk,Nr的值，分配密钥的存储空间
    Nk = len(k) // 8
    w = ['0'] * (4 * (14 + 1))

    if Nk == 4:
        Nr = 10
    elif Nk == 6:
        Nr = 12
    else:
        Nr = 14
    # 密钥扩展
    KeyExpansion(k, w, Nk)

    # 加密/解密
    if mode:
        for i in range(T):
            Encrypt(state, w, Nr)
    elif ~mode:
        for i in range(T):
            Decrypt(state, w, Nr)

    # 将状态矩阵转化为输出
    c = ['0'] * 16
    i = 0
    for col in range(4):
        for row in range(4):
            c[i] = state[row][col]
            i += 1

    print('0x' + ''.join(c))


if __name__ == "__main__":
    main()
