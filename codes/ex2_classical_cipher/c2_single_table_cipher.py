def single_table(p, c, s):
    for i in range(len(s)):
        s[i] = c[p.index(s[i])]
    return s


def main():
    p = list(input())
    c = list(input())
    s = list(input())
    model_ = int(input())
    single_table(p, c, s) if model_ else single_table(c, p, s)
    for i in s:
        print(i, end='')


if __name__ == "__main__":
    main()
