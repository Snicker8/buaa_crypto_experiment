if __name__ == '__main__':
    with open('msg3.txt', mode='r', encoding='utf-8') as file:
        msg = file.read()
        file.close()

    SPACE_LEN = 2
    with open('msg3_.txt', mode='w') as file:
        for space_len in range(1, SPACE_LEN + 1):
            for i in range(len(msg)):
                file.write(msg[:i] + space_len * ' ' + msg[i:] + '\n')

        for space_len1 in range(1, SPACE_LEN + 1):
            for space_len2 in range(1, SPACE_LEN + 1):
                for i in range(len(msg) - 1):
                    for j in range(i + 1, len(msg)):
                        file.write(msg[:i] + space_len1 * ' ' + msg[i:j] + space_len2 * ' ' + msg[j:] +
                                   '\n')
        file.close()
