# 密码调度算法KSA
def KSA(key):
    keylength = len(key) // 2
    S = [i for i in range(256)]
    j = 0
    for i in range(256):
        j = (j + S[i] + int(key[2 * (i % keylength):2 * (i % keylength + 1)], 16)) % 256
        S[i], S[j] = S[j], S[i]
    return S


# 伪随机生成算法PRGA
def PRGA(S, s):
    print('0x', end='')
    i = 0
    j = 0
    for k in range(len(s) // 2):
        i = (i + 1) % 256
        j = (j + S[i]) % 256
        S[i], S[j] = S[j], S[i]
        K = S[(S[i] + S[j]) % 256]
        c = int(s[2 * k:2 * (k + 1)], 16) ^ K
        print(hex(c)[2:].zfill(2), end='')


def RC4(key, s):
    S = KSA(key)
    PRGA(S, s)
    return 0


if __name__ == '__main__':
    k = input().strip().replace('\r', '').replace('\n', '')[2:]  # 密钥
    s = input().strip().replace('\r', '').replace('\n', '')[2:]  # 明密文
    RC4(k, s)
