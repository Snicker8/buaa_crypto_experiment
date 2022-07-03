import wordninja

f = open('texts/plaintext.txt')
plaintext = ''
for letter in f:
    plaintext += letter
f.close()

plaintext_ = wordninja.split(plaintext)

f = open('texts/plaintext_split.txt', 'w')
for text in plaintext_:
    f.write(text + ' ')
f.close()
