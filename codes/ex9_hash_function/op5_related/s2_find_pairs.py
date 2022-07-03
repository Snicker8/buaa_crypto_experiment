from hashlib import sha1


def hash_value(msg):
    return sha1(msg.encode()).hexdigest()


if __name__ == '__main__':
    with open('msg1_.txt', mode='r', encoding='gbk') as file1:
        msg1 = file1.read().split('\n')[:-1]
        file1.close()
    with open('msg3_.txt', mode='r', encoding='gbk') as file2:
        msg2 = file2.read().split('\n')[:-1]
        file2.close()

    for m1 in msg1:
        for m2 in msg2:
            if hash_value(m1)[:6] == hash_value(m2)[:6]:
                print('原始报文1：', m1.replace(' ', ''))
                print('变形报文1：', m1)
                print('原始报文2：', m2.replace(' ', ''))
                print('变形报文2：', m2)
                print('变形报文1的SHA1值：', hash_value(m1))
                print('变形报文2的SHA1值：', hash_value(m2))
                exit(0)
    exit(1)
