# 扩展欧几里得算法——返回x, y, (a, b)
def euclid(e1, e2):
    a11, a12, a13 = e1, 1, 0
    a21, a22, a23 = e2, 0, 1
    while a21 != 0:
        r = a11 // a21
        a11, a12, a13, a21, a22, a23 = a21, a22, a23, a11 - r * a21, a12 - r * a22, a13 - r * a23
    return a12, a13, a11


def main():
    e1, e2 = [int(i) for i in input().split()]
    x, y, g = euclid(e1, e2)

    # 负数暴力处理
    if g < 0:
        x, y, g = -1 * x, -1 * y, -1 * g

    # x暴力处理
    while x < 0:
        if e2 >= 0:
            x += e2 // g
            y -= e1 // g
        else:
            x -= e2 // g
            y += e1 // g
    print(x, y, g)


if __name__ == '__main__':
    main()
