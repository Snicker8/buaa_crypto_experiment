# Mersenne Twister 19937
def _int32(x):
    return int(0xffffffff & x)


class MT19937:
    def __init__(self, seed):
        self.mt = [0] * 624
        self.mt[0] = seed
        for i in range(1, 624):
            self.mt[i] = _int32(0x6c078965 * (self.mt[i - 1] ^ (self.mt[i - 1] >> 30)) + i)

    def extract_number(self):
        self.twist()
        for i in range(0, 20):
            x = self.mt[i]
            y = x ^ ((x >> 11) & 0xffffffff)
            y = y ^ ((y << 7) & 0x9d2c5680)
            y = y ^ ((y << 15) & 0xefc60000)
            z = y ^ (y >> 18)
            print(_int32(z))
        return 0

    def twist(self):
        for i in range(0, 624):
            x = _int32((self.mt[i] & 0x80000000) + (self.mt[(i + 1) % 624] & 0x7fffffff))
            xA = x >> 1
            if x % 2 != 0:
                xA = xA ^ 0x9908b0df
            self.mt[i] = self.mt[(i + 397) % 624] ^ xA


def main():
    seed = _int32(int(input()))
    mt = MT19937(seed)
    mt.extract_number()


if __name__ == "__main__":
    main()
