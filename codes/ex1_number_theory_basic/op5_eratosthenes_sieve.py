def eratos(n):
    l = list(range(1, n + 1))
    l[0] = 0
    for i in range(2, n + 1):
        if l[i - 1] != 0:
            for j in range(i * 2, n + 1, i):
                l[j - 1] = 0
    result = [x for x in l if x != 0]
    return result


def main():
    n = int(input())
    for m in eratos(n):
        print(m, end=' ')


if __name__ == '__main__':
    main()
