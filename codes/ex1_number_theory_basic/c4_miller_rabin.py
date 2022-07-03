from random import randint


# 平方乘算法（由高位到低位）
# 计算 b^n (mod m)
def pow(b, n, m):
    # 计算n的二进制表示
    n_bin = bin(n)[2:]
    c = 1
    for n_i in n_bin:
        c = c * c % m
        if n_i == '1':
            c = c * b % m
    return c


# Miller Rabin 素性检测（素数返回1）
def miller_rabin(n):
    # n - 1 = 2 ^ k * q
    q = n - 1
    k = 0
    while q % 2 == 0:
        q, k = q // 2, k + 1

    for i in range(10):
        a = randint(n // 2, n - 2)
        if pow(a, q, n) == 1:
            return 'YES'
        for j in range(k):
            if pow(a, 2 ** j * q, n) == n - 1:
                return 'YES'
    return 'NO'


def main():
    n = int(input())
    flag = miller_rabin(n)
    print(flag)


if __name__ == '__main__':
    main()
