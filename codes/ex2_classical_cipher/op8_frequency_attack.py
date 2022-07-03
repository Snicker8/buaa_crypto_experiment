# 数字转字母
def n2l(n):
    return chr(n + 97)


# 字母频率攻击
def frqc_att(s):
    times = []
    for i in range(26):
        times.append(s.count(n2l(i)))
    print((times.index(max(times)) - 4) % 26)


def main():
    s = input()
    frqc_att(s)


if __name__ == "__main__":
    main()
