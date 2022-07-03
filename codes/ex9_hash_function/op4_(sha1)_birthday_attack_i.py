from hashlib import sha1

if __name__ == '__main__':
    n = int(input()) // 4
    aim_value = input().strip().replace('\n', '').replace('\r', '')
    for i in range(1000000):
        try_value = sha1(str(i).encode()).hexdigest()
        if try_value[:n] == aim_value[:n]:
            print(str(i))
            break
