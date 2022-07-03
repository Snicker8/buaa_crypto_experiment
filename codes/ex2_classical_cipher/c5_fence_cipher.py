# 栅栏加解密(so easy)
def fence_enc(k, p):
    c = ''
    for i in range(k):
        c += p[i:: k]
    return c


def fence_dec(k, c):
    l = len(c) // k
    fence = []
    row = 0
    i = 0
    while row < len(c) % k:
        fence.append(c[i: i + l + 1])
        row += 1
        i = i + l + 1
    while row < k:
        fence.append(c[i: i + l])
        row += 1
        i = i + l
    p = ''
    for i in range(l + 1):
        for j in range(k):
            if i == l and j == len(c) % k:
                return p
            p += fence[j][i]


def main():
    k = int(input())
    s = input().strip().replace('\n', '').replace('\r', '')
    model_ = int(input())
    s = fence_enc(k, s) if model_ else fence_dec(k, s)
    print(s)


if __name__ == "__main__":
    main()
