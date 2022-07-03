import hashlib


class rsa:
    @staticmethod
    def encode(n, e, m):
        return rsa.fast_mod(m, e, n)

    @staticmethod
    def decode1(n, d, c):
        return rsa.fast_mod(c, d, n)

    @staticmethod
    def fast_mod(x, k, m):
        a = 1
        x = x % m
        while k:
            if k & 1:
                a = a * x % m
            k = k >> 1
            x = x * x % m
        return a


def get_str_sha1_secret_str(res):
    sha = hashlib.sha1(res)
    encrypts = sha.hexdigest()
    return encrypts


def encode(n, e, m, seed='', l=b''):
    n_hex = hex(n)[2:]
    if len(n_hex) & 1 == 1:
        n_hex = '0' + n_hex

    k = len(n_hex) // 2

    em = oeap_encode(n, e, m, seed=seed, l=l)
    if em == 'Err':
        return em
    c = rsa.encode(n, e, int(em, 16))

    res = "%0*x" % (k * 2, c)
    return bytearray.fromhex(res)


def decode(key, c, l=b''):
    n = key[0]
    n_hex = hex(n)[2:]
    if len(n_hex) & 1 == 1:
        n_hex = '0' + n_hex

    k = len(n_hex) // 2
    hLen = 20
    if len(c) != k or (k < 2 * hLen + 2):
        return 'Ree'

    cc = int(c.hex(), 16)
    em = rsa.decode1(key[0], key[1], cc)
    EM = '%0*x' % (k * 2, em)
    return oeap_decode(EM, k, hLen, l)


def oeap_encode(n, e, m, seed='', l=b''):
    n_hex = hex(n)[2:]
    if len(n_hex) & 1 == 1:
        n_hex = '0' + n_hex
    k = len(n_hex) // 2
    hLen = 20
    mLen = len(m)
    if mLen > (k - 2 - 2 * hLen):
        return 'Err'

    lhash = get_str_sha1_secret_str(l)
    if (k - mLen - 2 * hLen - 2) > 0:
        ps = '00' * (k - mLen - 2 * hLen - 2) + '01'
    else:
        ps = '01'
    DB = lhash + ps + m.hex()

    dbMask = MGF(seed, k - hLen - 1, hLen)
    maskedDB = hex_xor(dbMask, DB, (k - hLen - 1) * 2)
    seedMask = MGF(maskedDB, hLen, hLen)
    maskedSeed = hex_xor(seed, seedMask, hLen * 2)
    EM = '00' + maskedSeed + maskedDB
    return EM


def oeap_decode(EM, k, hLen, l=b''):
    lhash = get_str_sha1_secret_str(l)
    Y = EM[:2]
    if Y != '00':
        return 'Ree'
    maskedSeed = EM[:2 + 2 * hLen]
    maskedDB = EM[2 + 2 * hLen:]
    seedMask = MGF(maskedDB, hLen, hLen)
    seed = hex_xor(seedMask, maskedSeed, 2 * hLen)
    dbMask = MGF(seed, k - hLen - 1, hLen)
    DB = hex_xor(dbMask, maskedDB, (k - hLen - 1) * 2)
    index = 2 * hLen
    llhash = DB[:index]
    if lhash != llhash:
        return "Ree"
    while DB[index:index + 2] == '00':
        index += 2
    if DB[index:index + 2] != '01':
        return "Ree"
    index = index + 2
    m = DB[index:]
    return bytearray.fromhex(m)


def MGF(x, maskLen, hLen):
    T = bytearray(b'')
    k = maskLen // hLen
    if len(x) & 1 == 1:
        x = '0' + x
    X = bytearray.fromhex(x)
    if maskLen % hLen == 0:
        k -= 1
    for i in range(k + 1):
        tmp = X + bytearray.fromhex('%08x' % i)
        T = T + bytearray.fromhex(get_str_sha1_secret_str(tmp))
    mask = T[:maskLen]
    return mask.hex()


def hex_xor(a, b, l):
    return "%0*x" % (l, int(a, 16) ^ int(b, 16))


def main():
    op = int(input())  # 1/0 加密/解密
    if op:
        k = int(input())  # RSA安全参数
        e = int(input()[2:], 16)  # 加密指数
        n = int(input()[2:], 16)  # 模数
        m = input().strip().replace('\n', '').replace('\r', '')[2:]  # 明文
        m = bytes.fromhex(m)
        l = input().strip().replace('\n', '').replace('\r', '')[2:]  # 标签
        l = bytes.fromhex(l)
        seed = input().strip().replace('\n', '').replace('\r', '')[2:]  # 种子
        c = encode(n, e, m, seed=seed, l=l)
        if c == "Err":
            print(c)
            return 0
        else:
            c = c.hex()
            print('0x' + c)
            return 0
    else:
        k = int(input())  # RSA安全参数
        d = int(input()[2:], 16)  # 解密指数
        n = int(input()[2:], 16)  # 模数
        c = input().strip().replace('\n', '').replace('\r', '')[2:]  # 密文
        c = bytes.fromhex(c)
        l = input().strip().replace('\n', '').replace('\r', '')[2:]  # 标签
        l = bytes.fromhex(l)
        mm = decode([n, d], c, l)
        if mm == 'Ree':
            print(mm)
            return 0
        else:
            mm = mm.hex()
            mm = int(mm, 16)
            print(hex(mm))
            return 0


if __name__ == '__main__':
    main()
