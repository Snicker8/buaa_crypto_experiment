#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

#define LB32_MASK   0x00000001
#define LB64_MASK   0x0000000000000001
#define L64_MASK    0x00000000ffffffff
#define H64_MASK    0xffffffff00000000


static char IP[] = {
    58, 50, 42, 34, 26, 18, 10,  2,
    60, 52, 44, 36, 28, 20, 12,  4,
    62, 54, 46, 38, 30, 22, 14,  6,
    64, 56, 48, 40, 32, 24, 16,  8,
    57, 49, 41, 33, 25, 17,  9,  1,
    59, 51, 43, 35, 27, 19, 11,  3,
    61, 53, 45, 37, 29, 21, 13,  5,
    63, 55, 47, 39, 31, 23, 15,  7
};


static char PI[] = {
    40,  8, 48, 16, 56, 24, 64, 32,
    39,  7, 47, 15, 55, 23, 63, 31,
    38,  6, 46, 14, 54, 22, 62, 30,
    37,  5, 45, 13, 53, 21, 61, 29,
    36,  4, 44, 12, 52, 20, 60, 28,
    35,  3, 43, 11, 51, 19, 59, 27,
    34,  2, 42, 10, 50, 18, 58, 26,
    33,  1, 41,  9, 49, 17, 57, 25
};


static char E[] = {
    32,  1,  2,  3,  4,  5,
     4,  5,  6,  7,  8,  9,
     8,  9, 10, 11, 12, 13,
    12, 13, 14, 15, 16, 17,
    16, 17, 18, 19, 20, 21,
    20, 21, 22, 23, 24, 25,
    24, 25, 26, 27, 28, 29,
    28, 29, 30, 31, 32,  1
};


static char P[] = {
    16,  7, 20, 21,
    29, 12, 28, 17,
     1, 15, 23, 26,
     5, 18, 31, 10,
     2,  8, 24, 14,
    32, 27,  3,  9,
    19, 13, 30,  6,
    22, 11,  4, 25
};


static char S[8][64] = {{14, 0, 4, 15, 13, 7, 1, 4, 2, 14, 15, 2, 11, 13, 8, 1, 3, 10, 10, 6, 6, 12, 12, 11, 5, 9, 9, 5, 0, 3, 7, 8, 4, 15, 1, 12, 14, 8, 8, 2, 13, 4, 6, 9, 2, 1, 11, 7, 15, 5, 12, 11, 9, 3, 7, 14, 3, 10, 10, 0, 5, 6, 0, 13},
                        {15, 3, 1, 13, 8, 4, 14, 7, 6, 15, 11, 2, 3, 8, 4, 14, 9, 12, 7, 0, 2, 1, 13, 10, 12, 6, 0, 9, 5, 11, 10, 5, 0, 13, 14, 8, 7, 10, 11, 1, 10, 3, 4, 15, 13, 4, 1, 2, 5, 11, 8, 6, 12, 7, 6, 12, 9, 0, 3, 5, 2, 14, 15, 9},
                        {10, 13, 0, 7, 9, 0, 14, 9, 6, 3, 3, 4, 15, 6, 5, 10, 1, 2, 13, 8, 12, 5, 7, 14, 11, 12, 4, 11, 2, 15, 8, 1, 13, 1, 6, 10, 4, 13, 9, 0, 8, 6, 15, 9, 3, 8, 0, 7, 11, 4, 1, 15, 2, 14, 12, 3, 5, 11, 10, 5, 14, 2, 7, 12},
                        {7, 13, 13, 8, 14, 11, 3, 5, 0, 6, 6, 15, 9, 0, 10, 3, 1, 4, 2, 7, 8, 2, 5, 12, 11, 1, 12, 10, 4, 14, 15, 9, 10, 3, 6, 15, 9, 0, 0, 6, 12, 10, 11, 1, 7, 13, 13, 8, 15, 9, 1, 4, 3, 5, 14, 11, 5, 12, 2, 7, 8, 2, 4, 14},
                        {2, 14, 12, 11, 4, 2, 1, 12, 7, 4, 10, 7, 11, 13, 6, 1, 8, 5, 5, 0, 3, 15, 15, 10, 13, 3, 0, 9, 14, 8, 9, 6, 4, 11, 2, 8, 1, 12, 11, 7, 10, 1, 13, 14, 7, 2, 8, 13, 15, 6, 9, 15, 12, 0, 5, 9, 6, 10, 3, 4, 0, 5, 14, 3},
                        {12, 10, 1, 15, 10, 4, 15, 2, 9, 7, 2, 12, 6, 9, 8, 5, 0, 6, 13, 1, 3, 13, 4, 14, 14, 0, 7, 11, 5, 3, 11, 8, 9, 4, 14, 3, 15, 2, 5, 12, 2, 9, 8, 5, 12, 15, 3, 10, 7, 11, 0, 14, 4, 1, 10, 7, 1, 6, 13, 0, 11, 8, 6, 13},
                        {4, 13, 11, 0, 2, 11, 14, 7, 15, 4, 0, 9, 8, 1, 13, 10, 3, 14, 12, 3, 9, 5, 7, 12, 5, 2, 10, 15, 6, 8, 1, 6, 1, 6, 4, 11, 11, 13, 13, 8, 12, 1, 3, 4, 7, 10, 14, 7, 10, 9, 15, 5, 6, 0, 8, 15, 0, 14, 5, 2, 9, 3, 2, 12},
                        {13, 1, 2, 15, 8, 13, 4, 8, 6, 10, 15, 3, 11, 7, 1, 4, 10, 12, 9, 5, 3, 6, 14, 11, 5, 0, 0, 14, 12, 9, 7, 2, 7, 2, 11, 1, 4, 14, 1, 7, 9, 4, 12, 10, 14, 8, 2, 13, 0, 15, 6, 12, 10, 9, 13, 0, 15, 3, 3, 5, 5, 6, 8, 11}};

static uint32_t SP[8][64] = {{8421888, 0, 32768, 8421890, 8421378, 33282, 2, 32768, 512, 8421888, 8421890, 512, 8389122, 8421378, 8388608, 2, 514, 8389120, 8389120, 33280, 33280, 8421376, 8421376, 8389122, 32770, 8388610, 8388610, 32770, 0, 514, 33282, 8388608, 32768, 8421890, 2, 8421376, 8421888, 8388608, 8388608, 512, 8421378, 32768, 33280, 8388610, 512, 2, 8389122, 33282, 8421890, 32770, 8421376, 8389122, 8388610, 514, 33282, 8421888, 514, 8389120, 8389120, 0, 32770, 33280, 0, 8421378},
                        {1074282512, 1073758208, 16384, 540688, 524288, 16, 1074266128, 1073758224, 1073741840, 1074282512, 1074282496, 1073741824, 1073758208, 524288, 16, 1074266128, 540672, 524304, 1073758224, 0, 1073741824, 16384, 540688, 1074266112, 524304, 1073741840, 0, 540672, 16400, 1074282496, 1074266112, 16400, 0, 540688, 1074266128, 524288, 1073758224, 1074266112, 1074282496, 16384, 1074266112, 1073758208, 16, 1074282512, 540688, 16, 16384, 1073741824, 16400, 1074282496, 524288, 1073741840, 524304, 1073758224, 1073741840, 524304, 540672, 0, 1073758208, 16400, 1073741824, 1074266128, 1074282512, 540672},
                        {260, 67174656, 0, 67174404, 67109120, 0, 65796, 67109120, 65540, 67108868, 67108868, 65536, 67174660, 65540, 67174400, 260, 67108864, 4, 67174656, 256, 65792, 67174400, 67174404, 65796, 67109124, 65792, 65536, 67109124, 4, 67174660, 256, 67108864, 67174656, 67108864, 65540, 260, 65536, 67174656, 67109120, 0, 256, 65540, 67174660, 67109120, 67108868, 256, 0, 67174404, 67109124, 65536, 67108864, 67174660, 4, 65796, 65792, 67108868, 67174400, 67109124, 260, 67174400, 65796, 4, 67174404, 65792},
                        {2151682048, 2147487808, 2147487808, 64, 4198464, 2151678016, 2151677952, 2147487744, 0, 4198400, 4198400, 2151682112, 2147483712, 0, 4194368, 2151677952, 2147483648, 4096, 4194304, 2151682048, 64, 4194304, 2147487744, 4160, 2151678016, 2147483648, 4160, 4194368, 4096, 4198464, 2151682112, 2147483712, 4194368, 2151677952, 4198400, 2151682112, 2147483712, 0, 0, 4198400, 4160, 4194368, 2151678016, 2147483648, 2151682048, 2147487808, 2147487808, 64, 2151682112, 2147483712, 2147483648, 4096, 2151677952, 2147487744, 4198464, 2151678016, 2147487744, 4160, 4194304, 2151682048, 64, 4194304, 4096, 4198464},
                        {128, 17039488, 17039360, 553648256, 262144, 128, 536870912, 17039360, 537133184, 262144, 16777344, 537133184, 553648256, 553910272, 262272, 536870912, 16777216, 537133056, 537133056, 0, 536871040, 553910400, 553910400, 16777344, 553910272, 536871040, 0, 553648128, 17039488, 16777216, 553648128, 262272, 262144, 553648256, 128, 16777216, 536870912, 17039360, 553648256, 537133184, 16777344, 536870912, 553910272, 17039488, 537133184, 128, 16777216, 553910272, 553910400, 262272, 553648128, 553910400, 17039360, 0, 537133056, 553648128, 262272, 16777344, 536871040, 262144, 0, 537133056, 17039488, 536871040},
                        {268435464, 270532608, 8192, 270540808, 270532608, 8, 270540808, 2097152, 268443648, 2105352, 2097152, 268435464, 2097160, 268443648, 268435456, 8200, 0, 2097160, 268443656, 8192, 2105344, 268443656, 8, 270532616, 270532616, 0, 2105352, 270540800, 8200, 2105344, 270540800, 268435456, 268443648, 8, 270532616, 2105344, 270540808, 2097152, 8200, 268435464, 2097152, 268443648, 268435456, 8200, 268435464, 270540808, 2105344, 270532608, 2105352, 270540800, 0, 270532616, 8, 8192, 270532608, 2105352, 8192, 2097160, 268443656, 0, 270540800, 268435456, 2097160, 268443656},
                        {1048576, 34603009, 33555457, 0, 1024, 33555457, 1049601, 34604032, 34604033, 1048576, 0, 33554433, 1, 33554432, 34603009, 1025, 33555456, 1049601, 1048577, 33555456, 33554433, 34603008, 34604032, 1048577, 34603008, 1024, 1025, 34604033, 1049600, 1, 33554432, 1049600, 33554432, 1049600, 1048576, 33555457, 33555457, 34603009, 34603009, 1, 1048577, 33554432, 33555456, 1048576, 34604032, 1025, 1049601, 34604032, 1025, 33554433, 34604033, 34603008, 1049600, 0, 1, 34604033, 0, 1049601, 34603008, 1024, 33554433, 33555456, 1024, 1048577},
                        {134219808, 2048, 131072, 134350880, 134217728, 134219808, 32, 134217728, 131104, 134348800, 134350880, 133120, 134350848, 133152, 2048, 32, 134348800, 134217760, 134219776, 2080, 133120, 131104, 134348832, 134350848, 2080, 0, 0, 134348832, 134217760, 134219776, 133152, 131072, 133152, 131072, 134350848, 2048, 32, 134348832, 2048, 133152, 134219776, 32, 134217760, 134348800, 134348832, 134217728, 131072, 134219808, 0, 134350880, 131104, 134217760, 134348800, 134219776, 134219808, 0, 134350880, 133120, 133120, 2080, 2080, 131104, 134217728, 134350848}};

static char PC1[] = {
    57, 49, 41, 33, 25, 17,  9,
     1, 58, 50, 42, 34, 26, 18,
    10,  2, 59, 51, 43, 35, 27,
    19, 11,  3, 60, 52, 44, 36,

    63, 55, 47, 39, 31, 23, 15,
     7, 62, 54, 46, 38, 30, 22,
    14,  6, 61, 53, 45, 37, 29,
    21, 13,  5, 28, 20, 12,  4
};


static char PC2[] = {
    14, 17, 11, 24,  1,  5,
     3, 28, 15,  6, 21, 10,
    23, 19, 12,  4, 26,  8,
    16,  7, 27, 20, 13,  2,
    41, 52, 31, 37, 47, 55,
    30, 40, 51, 45, 33, 48,
    44, 49, 39, 56, 34, 53,
    46, 42, 50, 36, 29, 32
};


static char iteration_shift[] = {

    1,  1,  2,  2,  2,  2,  2,  2,  1,  2,  2,  2,  2,  2,  2,  1
};


uint64_t des(uint64_t input, uint64_t key) {

    int i, j;

    /* 8 bits */
    char row, column;

    /* 28 bits */
    uint32_t C                  = 0;
    uint32_t D                  = 0;


    /* 32 bits */
    uint32_t L                  = 0;
    uint32_t R                  = 0;
    uint32_t s_output           = 0;
    uint32_t f_function_res     = 0;
    uint32_t temp               = 0;

    /* 48 bits */
    uint64_t sub_key[16]        = {0};
    uint64_t s_input            = 0;

    /* 56 bits */
    uint64_t permuted_choice_1  = 0;
    uint64_t permuted_choice_2  = 0;

    /* 64 bits */
    uint64_t init_perm_res      = 0;
    uint64_t inv_init_perm_res  = 0;
    uint64_t pre_output         = 0;
    uint64_t idx                = 0;

    /* initial permutation */
    for (i = 0; i < 64; i++) {

        init_perm_res <<= 1;
        init_perm_res |= (input >> (64-IP[i])) & LB64_MASK;

    }

    L = (uint32_t) (init_perm_res >> 32) & L64_MASK;
    R = (uint32_t) init_perm_res & L64_MASK;

    /* initial key schedule calculation */
    for (i = 0; i < 56; i++) {

        permuted_choice_1 <<= 1;
        permuted_choice_1 |= (key >> (64-PC1[i])) & LB64_MASK;

    }

    C = (uint32_t) ((permuted_choice_1 >> 28) & 0x000000000fffffff);
    D = (uint32_t) (permuted_choice_1 & 0x000000000fffffff);

    /* Calculation of the 16 keys */
    for (i = 0; i< 16; i++) {

        /* key schedule */
        // shifting Ci and Di
        for (j = 0; j < iteration_shift[i]; j++) {

            C = 0x0fffffff & (C << 1) | 0x00000001 & (C >> 27);
            D = 0x0fffffff & (D << 1) | 0x00000001 & (D >> 27);

        }

        permuted_choice_2 = 0;
        permuted_choice_2 = (((uint64_t) C) << 28) | (uint64_t) D ;

        sub_key[i] = 0;

        for (j = 0; j < 48; j++) {

            sub_key[i] <<= 1;
            sub_key[i] |= (permuted_choice_2 >> (56-PC2[j])) & LB64_MASK;

        }

    }

    for (i = 0; i < 16; i++) {

        /* f(R,k) function */
        s_input = 0;
        /*  expand */
        s_input = (s_input<<1) + ((R)&1);
        s_input = (s_input<<5) + ((R>>27)&0x1f);
        s_input = (s_input<<6) + ((R>>23)&0x3f);
        s_input = (s_input<<6) + ((R>>19)&0x3f);
        s_input = (s_input<<6) + ((R>>15)&0x3f);
        s_input = (s_input<<6) + ((R>>11)&0x3f);
        s_input = (s_input<<6) + ((R>>7 )&0x3f);
        s_input = (s_input<<6) + ((R>>3 )&0x3f);
        s_input = (s_input<<5) + (R&0x1f);
        s_input = (s_input<<1) + ((R>>31)&1);

        s_input = s_input ^ sub_key[i];

        f_function_res = 0;
        /* S-Box Tables */
        s_output = 0;
        idx = (s_input)&(0b111111);
        s_input >>= 6;
        f_function_res |= SP[7][idx];
        idx = (s_input)&(0b111111);
        s_input >>= 6;
        f_function_res |= SP[6][idx];
        idx = (s_input)&(0b111111);
        s_input >>= 6;
        f_function_res |= SP[5][idx];
        idx = (s_input)&(0b111111);
        s_input >>= 6;
        f_function_res |= SP[4][idx];
        idx = (s_input)&(0b111111);
        s_input >>= 6;
        f_function_res |= SP[3][idx];
        idx = (s_input)&(0b111111);
        s_input >>= 6;
        f_function_res |= SP[2][idx];
        idx = (s_input)&(0b111111);
        s_input >>= 6;
        f_function_res |= SP[1][idx];
        idx = (s_input)&(0b111111);
        s_input >>= 6;
        f_function_res |= SP[0][idx];


        temp = R;
        R = L ^ f_function_res;
        L = temp;

    }

    pre_output = (((uint64_t) R) << 32) | (uint64_t) L;


    for (i = 0; i < 64; i++) {

        inv_init_perm_res <<= 1;
        inv_init_perm_res |= (pre_output >> (64-PI[i])) & LB64_MASK;

    }

    return inv_init_perm_res;

}

int main(int argc, const char * argv[]) {

    int i,T;
    scanf("%d\n",&T);

    uint64_t input;
    uint64_t key;
    scanf("0x%016llx\n",&input);
    uint64_t result = input;
    scanf("0x%016llx",&key);

    result = des(input, key);

    for(int i=0;i<T-1;i++)
        {input = result;
        result = des(result, key);
        }
    printf ("0x%016llx\n", result);

    exit(0);

}