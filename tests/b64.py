import base64

s = base64.b64encode('武汉'.encode('utf-8'))
print(s.decode())

d = base64.b64decode(b'JUU2JTg4JTkx').decode('utf-8')
print(d)
