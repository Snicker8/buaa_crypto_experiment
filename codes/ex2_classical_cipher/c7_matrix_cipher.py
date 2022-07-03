def matrix_enc(n, k, s):
    i = 0
    while i < len(s):
        k.append(s[i: i + n])
        i += n
    i = 1
    while i <= n:
        index = k[0].index(i)
        for j in range(1, len(k)):
            print(k[j][index], end='')
        i += 1


def matrix_dec(n, k, s):
    i = 0
    while i < len(s):
        k.append(s[i: i + len(s) // n])
        i += len(s) // n
    for col in range(len(s) // n):
        for index in k[0]:
            print(k[index][col], end='')


def main():
    n = int(input())
    k = [list(input().strip().replace('\n', '').replace('\r', ''))]
    for i in range(n): k[0][i] = int(k[0][i])
    s = list(input().strip().replace('\n', '').replace('\r', ''))
    model_ = int(input())

    matrix_enc(n, k, s) if model_ else matrix_dec(n, k, s)


if __name__ == "__main__":
    main()
