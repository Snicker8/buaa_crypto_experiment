'''
0x1f011f010e010e01 0x011f011f010e010e
0x1e001e000f000f00 0x001e001e000f000f
0xe001e001f101f101 0x01e001e001f101f1
0xe100e100f000f000 0x00e100e100f000f0
0xfee0fee0fef1fef1 0xe0fee0fef1fef1fe
0xffe1ffe1fff0fff0 0xe1ffe1fff0fff0ff
0xfe1ffe1ffe0efe0e 0x1ffe1ffe0efe0efe
0xff1eff1eff0fff0f 0x1eff1eff0fff0fff
0xfe01fe01fe01fe01 0x01fe01fe01fe01fe
0xff00ff00ff00ff00 0x00ff00ff00ff00ff
0xe01fe01ff10ef10e 0x1fe01fe00ef10ef1
0xe11ee11ef00ff00f 0x1ee11ee10ff00ff0
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

    pairs = []
    for i in range(48):
        for j in range(16):
            pairs.append([K_[i][j], K_[i][15 - j] + 64])

    groups = []
    # 有0的一组
    group = [0]
    for i in range(48 * 16):
        for j in range(2):
            if pairs[i][j] not in group and pairs[i][1 - j] in group:
                group.append(pairs[i][j])
    group.sort()
    groups.append(group)

    # 有3的一组
    group = [3]
    for i in range(48 * 16):
        for j in range(2):
            if pairs[i][j] not in group and pairs[i][1 - j] in group:
                group.append(pairs[i][j])
    group.sort()
    groups.append(group)

    # 有8的一组
    group = [8]
    for i in range(48 * 16):
        for j in range(2):
            if pairs[i][j] not in group and pairs[i][1 - j] in group:
                group.append(pairs[i][j])
    group.sort()
    groups.append(group)

    # 有11的一组
    group = [11]
    for i in range(48 * 16):
        for j in range(2):
            if pairs[i][j] not in group and pairs[i][1 - j] in group:
                group.append(pairs[i][j])
    group.sort()
    groups.append(group)

    # 奇偶校验位的一组
    group = []
    for i in range(128):
        flag = 1
        for j in range(len(groups)):
            if i in groups[j]:
                flag = 0
                break
        if flag: group.append(i)
    groups.append(group)

    for group in groups: print(group)

    # 每一组遍历0, 1
    res_list = []
    temp = 0
    for i in range(128):
        if i in groups[0]:
            res_list.append(0)
        # if i in groups[0]: res_list.append(1)
        elif i in groups[1]:
            res_list.append(1)
        # elif i in groups[1]: res_list.append(0)
        elif i in groups[2]:
            res_list.append(1)
        # elif i in groups[2]: res_list.append(0)
        elif i in groups[3]:
            res_list.append(1)
        # elif i in groups[3]: res_list.append(0)
        else:
            for j in range(i - 7, i):
                temp += res_list[j]
            # 奇偶校验位
            res_list.append(temp & 1)
            # res_list.append(temp+1 & 1)
            temp = 0

    res_str = ''
    for i in range(128):
        res_str += str(res_list[i])
    print(b2h(res_str[:64]), b2h(res_str[64:]))


if __name__ == "__main__":
    main()
