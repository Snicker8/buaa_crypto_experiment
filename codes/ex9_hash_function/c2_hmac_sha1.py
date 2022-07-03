Kt = [0x5A827999] * 20 + [0x6ED9EBA1] * 20 + [0x8F1BBCDC] * 20 + [0xCA62C1D6] * 20


# 32比特数循环左移k位
def shift_32(n_32bit, k):
    return ((n_32bit << k) | (n_32bit >> (32 - k))) & 0xffffffff


# 原始逻辑函数f_logical
def f_logical(t, B, C, D):
    if t <= 19:
        return (B & C) | ((B ^ 0xffffffff) & D)
    elif t <= 39 or t > 59:
        return B ^ C ^ D
    elif t <= 59:
        return (B & C) | (B & D) | (C & D)


# SHA1初始化——填充
def padding(msg):
    msg_bitlen = len(msg) * 8
    int_msg = int.from_bytes(msg, 'big')
    int_msg = ((int_msg << 1) | 1) << (512 - (msg_bitlen + 64) % 512) - 1
    int_msg = int_msg << 64 | msg_bitlen
    return int_msg, (msg_bitlen + 64) // 512 + 1


# 报文分组
def gourping(msg, group_len):
    msg_groups = []
    for _ in range(group_len):
        msg_groups.append(msg & ((1 << 512) - 1))
        msg >>= 512
    return msg_groups[::-1]


# 压缩函数f_compress
def f_compress(Y_i, CV_i):
    Wt = []
    for i in range(16):
        Wt.append(Y_i & 0xffffffff)
        Y_i >>= 32
    Wt = Wt[::-1]
    for i in range(16, 80):
        Wt.append(shift_32(Wt[i - 3] ^ Wt[i - 8] ^ Wt[i - 14] ^ Wt[i - 16], 1))

    A, B, C, D, E = CV_i
    for i in range(80):
        A, B, C, D, E = (E + f_logical(i, B, C, D) + shift_32(A, 5) + Wt[i] + Kt[i]) & 0xffffffff, A, shift_32(B,
                                                                                                               30), C, D
    CV_i = [(CV_i[0] + A) & 0xffffffff, (CV_i[1] + B) & 0xffffffff, (CV_i[2] + C) & 0xffffffff,
            (CV_i[3] + D) & 0xffffffff, (CV_i[4] + E) & 0xffffffff]
    return CV_i


# 哈希函数——SHA1
def hash_sha1(msg):
    msg, group_len = padding(msg)
    msg = gourping(msg, group_len)
    CV = [0x67452301, 0xEFCDAB89, 0x98BADCFE, 0x10325476, 0xC3D2E1F0]
    for i in range(group_len):
        CV = f_compress(msg[i], CV)
    return hex((((CV[0] << 32 | CV[1]) << 32 | CV[2]) << 32 | CV[3]) << 32 | CV[4])[2:].zfill(40)


# SHA1-HMAC算法
def hmac_sha1(key, msg):
    key_bitlen = len(key) * 4
    key = int(key, 16)
    key <<= (512 - key_bitlen)
    ipad = int('00110110' * 64, 2)
    opad = int('01011100' * 64, 2)
    S_i = (key ^ ipad).to_bytes(64, 'big')
    S_0 = (key ^ opad).to_bytes(64, 'big')
    return hash_sha1(S_0 + int(hash_sha1(S_i + msg), 16).to_bytes(20, 'big'))


if __name__ == '__main__':
    key = input().strip().replace('\n', '').replace('\r', '')
    msg = input().strip().replace('\n', '').replace('\r', '').encode()
    print(hmac_sha1(key, msg))
