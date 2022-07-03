def n2l(n):
    return chr(n + 97)


f = open('texts/ciphertext.txt')
ct = ''
for line in f:
    ct += line
f.close()

times = {}
for i in range(26):
    times[n2l(i)] = round(ct.count(n2l(i)) / len(ct) * 100, 3)

times = {k: v for k, v in sorted(times.items(), key=lambda item: item[1])}

# pt_frqc = ['z', 'q', 'x', 'j', 'k', 'v', 'b', 'p', 'y', 'g', 'f', 'w', 'm', 'u', 'c', 'l', 'd', 'r', 'h', 's', 'n', 'i', 'o', 'a', 't', 'e']
# ct_frqc = ['t', 'v', 'p', 'r', 'z', 'b', 'a', 'u', 'y', 'h', 'd', 'e', 'k', 'x', 'w', 'o', 's', 'm', 'q', 'f', 'g', 'i', 'c', 'l', 'n', 'j']
# ct_frqc = ['t', 'v', 'p', 'r', 'z', 'b', 'a', 'u', 'y', 'h', 'd', 'e', 'k', 'w', 'x', 'o', 's', 'm', 'q', 'f', 'i', 'g', 'c', 'l', 'n', 'j']
# ct_frqc = ['t', 'v', 'p', 'r', 'z', 'b', 'a', 'u', 'y', 'h', 'd', 'e', 'k', 'w', 'x', 'o', 's', 'm', 'f', 'q', 'i', 'g', 'c', 'l', 'n', 'j']
# ct_frqc = ['t', 'v', 'p', 'r', 'z', 'b', 'a', 'u', 'y', 'h', 'd', 'e', 'x', 'w', 'k', 'o', 's', 'm', 'f', 'q', 'i', 'g', 'c', 'l', 'n', 'j']
ct_frqc = ['t', 'v', 'r', 'p', 'z', 'b', 'a', 'u', 'y', 'h', 'd', 'e', 'x', 'w', 'k', 'o', 's', 'm', 'f', 'q', 'i', 'g',
           'c', 'l', 'n', 'j']
pt_frqc = ['z', 'q', 'x', 'j', 'k', 'v', 'b', 'p', 'y', 'g', 'f', 'w', 'm', 'u', 'c', 'l', 'd', 'r', 'h', 's', 'n', 'i',
           'o', 'a', 't', 'e']

pt = ''
for c in ct:
    p = pt_frqc[ct_frqc.index(c)]
    pt += p

f = open('texts/plaintext_v4.txt', 'w')
f.write(pt)
f.close()
