key = b'' # надо запомнить что размер ключа 5, главное не забыть блин

with open("flag.png", 'rb') as ff:
    flag = ff.read()

data = b''
for byte, num in zip(flag,range(len(flag))):
    data += bytes([byte^key[num % len(key)]])

with open("output.png", 'wb') as fn:
    fn.write(data)