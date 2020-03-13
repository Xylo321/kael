def str_to_hex(s):
    return ' '.join([hex(ord(c)) for c in s])


def hex_to_str(s):
    return ''.join([chr(i) for i in [int(b, 16) for b in s.split(' ')]])


def str_to_bin(s):
    return ' '.join([bin(ord(c)) for c in s])


def bin_to_str(s):
    return ''.join([chr(i) for i in [int(b, 2) for b in s.split(' ')]])


s = str_to_hex('我是你爸爸...')
print(s)

print(hex_to_str(s))

s1 = str_to_bin('我是你爸爸')
print(s1)

print(bin_to_str(s1))
