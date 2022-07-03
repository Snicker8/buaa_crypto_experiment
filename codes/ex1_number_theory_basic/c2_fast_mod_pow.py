# 平方乘算法（由高位到低位）
# 计算 b^n (mod m)
def fast_mod_pow(b, n, m):
    # 计算n的二进制表示
    n_bin = bin(n)[2:]
    c = 1
    for n_i in n_bin:
        c = c * c % m
        if n_i == '1':
            c = c * b % m
    return c


def main():
    b, n, m = [int(i) for i in input().split()]
    print(fast_mod_pow(b, n, m))


if __name__ == '__main__':
    main()
