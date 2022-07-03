from math import ceil
from hashlib import sha1


# 掩码生成函数——mask generate function
def MGF1(X, maskLen):
    T = b''
    k = ceil(maskLen / 20)
    for counter in range(k):
        C = counter.to_bytes(4, 'big')
        T = T + sha1(X + C).digest()
    return T[:maskLen]


# 消息编码算法：返回EM
def encode_message(M, salt, emBits):
    emLen = ceil(emBits / 8)
    mHash = sha1(M).digest()
    padding1 = bytes(8)
    padding2 = b'\x00' * (emLen - 20 - 20 - 2) + b'\x01'
    H = sha1(padding1 + mHash + salt).digest()
    DB = padding2 + salt
    DBmask = MGF1(H, emLen - 20 - 1)
    # 异或而已，只是转成整数了又转回来
    maskedDB = (int.from_bytes(DB, 'big') ^ int.from_bytes(DBmask, 'big')).to_bytes(emLen - 20 - 1, 'big')
    EM = maskedDB + H + b'\xbc'
    return EM


# 签名算法
def sign(EM, d, n):
    s = pow(int.from_bytes(EM, 'big'), d, n)
    return hex(s)[2:].zfill(256)


# 验证算法
def verify(M, S, e, n, emBits):
    s = int(S, 16)
    emLen = ceil(emBits / 8)
    m = pow(s, e, n)
    EM = m.to_bytes(emLen, 'big')
    maskedDB = EM[:emLen - 20 - 1]
    H = EM[emLen - 20 - 1:-1]
    mHash = sha1(M).digest()
    DBmask = MGF1(H, emLen - 20 - 1)
    DB = (int.from_bytes(maskedDB, 'big') ^ int.from_bytes(DBmask, 'big')).to_bytes(emLen - 20 - 1, 'big')
    salt = DB[-20:]
    M_ = bytes(8) + mHash + salt
    H_ = sha1(M_).digest()
    return H_ == H


def main():
    M = input().encode()
    n = int(input())
    emBits = int(input())
    mode = input()
    if mode == 'Sign':
        d = int(input())
        salt = bytes.fromhex(input())
        EM = encode_message(M, salt, emBits)
        S = sign(EM, d, n)
        print(S)
    else:
        e = int(input())
        S = input()
        print(verify(M, S, e, n, emBits))


if __name__ == '__main__':
    main()
