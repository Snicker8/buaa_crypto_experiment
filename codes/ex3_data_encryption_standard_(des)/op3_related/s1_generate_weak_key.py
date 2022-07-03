'''
0x0101010101010101
0x0000000000000000
0x1f1f1f1f0e0e0e0e
0x1e1e1e1e0f0f0f0f
0xe0e0e0e0f1f1f1f1
0xe1e1e1e1f0f0f0f0
0xfefefefefefefefe
0xffffffffffffffff
'''


def h2b(x): return bin(int(x, 16))[2:].zfill(4 * len(x))


def b2h(x): return hex(int(x, 2))[2:].zfill(len(x) // 4)


def PC_1(k):
    k_pc_1 = []
    pc_1 = [57, 49, 41, 33, 25, 17, 9, 1, 58, 50, 42, 34, 26, 18,
            10, 2, 59, 51, 43, 35, 27, 19, 11, 3, 60, 52, 44, 36,
            63, 55, 47, 39, 31, 23, 15, 7, 62, 54, 46, 38, 30, 22,
            14, 6, 61, 53, 45, 37, 29, 21, 13, 5, 28, 20, 12, 4]
    for i in range(56): k_pc_1.append(k[pc_1[i] - 1])
    return k_pc_1


def PC_2(k):
    k_pc_2 = []
    pc_2 = [14, 17, 11, 24, 1, 5, 3, 28, 15, 6, 21, 10,
            23, 19, 12, 4, 26, 8, 16, 7, 27, 20, 13, 2,
            41, 52, 31, 37, 47, 55, 30, 40, 51, 45, 33, 48,
            44, 49, 39, 56, 34, 53, 46, 42, 50, 36, 29, 32]
    for i in range(48): k_pc_2.append(k[pc_2[i] - 1])
    return k_pc_2


def LS(s, i):
    ls = [1, 1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1]
    s = s[ls[i]:] + s[:ls[i]]
    return s


def key_gen(k):
    k = PC_1(k)
    C, D = k[:28], k[28:]
    K = []
    for i in range(16):
        C, D = LS(C, i), LS(D, i)
        K.append(PC_2(C + D))
    return K


def main():
    index = [i for i in range(64)]

    K = key_gen(index)

    # 转置一下
    K_ = []
    for j in range(48):
        temp = []
        for i in range(16):
            temp.append(K[i][j])
        K_.append(temp)

    # 取有1的一组
    group_1 = []
    for i in range(48):
        if 1 in K_[i]:
            for j in range(16):
                if K_[i][j] not in group_1:
                    group_1.append(K_[i][j])
    group_1.sort()
    print(group_1)

    # 取有3的一组
    group_2 = []
    for i in range(48):
        if 3 in K_[i]:
            for j in range(16):
                if K_[i][j] not in group_2:
                    group_2.append(K_[i][j])
    group_2.sort()
    print(group_2)

    # 剩下的一组
    group_3 = []
    for i in range(64):
        if i not in group_1 and i not in group_2:
            group_3.append(i)
    print(group_3)

    # 每一组遍历0, 1
    res_list = []
    temp = 0
    for i in range(64):
        if i in group_1:
            res_list.append(0)
        # if i in group_1: res_list.append(1)
        elif i in group_2:
            res_list.append(1)
        # elif i in group_2: res_list.append(0)
        else:
            for j in range(i - 7, i):
                temp += res_list[j]
            # 奇偶校验位
            res_list.append(temp & 1)
            # res_list.append(temp+1 & 1)
            temp = 0

    res_str = ''
    for i in range(64):
        res_str += str(res_list[i])
    print(b2h(res_str))


if __name__ == "__main__":
    main()
