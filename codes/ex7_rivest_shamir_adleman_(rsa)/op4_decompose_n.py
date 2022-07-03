import gmpy2


def main():
    e = int(input())
    d = int(input())
    N = int(input())

    k_ = (e * d) // N
    while (e * d - 1) % k_ != 0:
        k_ += 1
    phi = (e * d - 1) // k_
    a = N - phi + 1
    b = N
    p = (a - gmpy2.iroot(a * a - 4 * b, 2)[0]) // 2
    q = (a + gmpy2.iroot(a * a - 4 * b, 2)[0]) // 2
    print(p)
    print(q)


if __name__ == "__main__":
    main()
