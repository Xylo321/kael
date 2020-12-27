from kael.security.xss import replace_unsafe_chars

with open("code") as f:
    print(replace_unsafe_chars(f.read()))