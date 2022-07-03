from hashlib import sha1


def mr(x, p):
    '''
    :return: x ^ -1 mod p
    '''
    x %= p
    u1, u2, u3 = 1, 0, x
    v1, v2, v3 = 0, 1, p
    while v3 != 0:
        q = u3 // v3
        v1, v2, v3, u1, u2, u3 = (u1 - q * v1), (u2 - q * v2), (u3 - q * v3), v1, v2, v3
    return u1 % p


def sign(m, s, r):
    global p, q, g
    x = pow(g, r, p)
    e = int(sha1((m + str(x)).encode('utf-8')).hexdigest(), 16)
    y = (r + s * e) % q
    return e, y


def verify(m, v, e, y):
    global p, g
    x = pow(g, y, p) * pow(v, e, p) % p
    e_ = int(sha1((m + str(x)).encode('utf-8')).hexdigest(), 16)
    return e_ == e


def main():
    global p, q, g
    p = int(input())
    q = int(input())
    g = int(input())
    m = input()
    mode = input()
    if mode == 'Sign':
        s = int(input())
        r = int(input())
        e, y = sign(m, s, r)
        print(e, y)
    else:
        v = int(input())
        e, y = map(int, input().split())
        print(verify(m, v, e, y))


if __name__ == '__main__':
    main()
