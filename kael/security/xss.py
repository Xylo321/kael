"""
XSS漏洞检测

markdown检测:
* <, >
* <img ...javascript>
"""


def replace_unsafe_chars(content):
    tmp = list(tuple(content))

    # 如果content中有不是``包含的<, >
    # 如果content中有不是```包含的<, >，但是当前元素紧接着3个，如果不是img（忽略大小写）就替换
    # <, > 替换为 &lt; &gt;

    sig = 0
    img_sig = 0
    img_start = 0
    img_end = 0
    pre = None
    i = 0
    l = len(tmp)
    while i < l:
        # 如果sig 等于0，如果遇到了`,```则将标志位设置为1，并记录是什么代码
        # 例如`, ```
        if sig == 0:
            if tmp[i] == "`" and "```" != content[i: i+3]:
                sig = 1
                pre = '`'
                i += 1
                continue
            if "```" == content[i: i+3]:
                sig = 1
                pre = '```'
                i += 3
                continue

            # 如果在代码段之外遇到了<则替换为&lt;
            if tmp[i] == '<':
                # 如果不是<img则替换，是则将img_sig变为1
                if tmp[i + 1].lower() != "i" or tmp[i + 2].lower() != 'm' or tmp[i + 3].lower() != 'g':
                    tmp[i] = "&lt;"
                else:
                    # 并且记录<img的位置，主要是用来发现是不是有javascript在img中
                    img_start = i
                    img_sig = 1

            if tmp[i] == '>':
                # 如果img_sig不为1，则说明不是<img，那么替换，是则将img_sig变为0
                if img_sig != 1:
                    tmp[i] = "&gt;"
                else:
                    # img标签结束了，那么记录img的结束位置
                    img_end = i

                    # 检测<img>中是否包含javascript
                    check_img_javascript = ''.join(list(tuple(tmp[img_start: img_end]))).lower()
                    # 如果有，则将<,>替换为&lt;, &gt;
                    if 'javascript' in check_img_javascript:
                        tmp[img_start] = "&lt;"
                        tmp[img_end] = "&gt;"

                    img_sig = 0

        # 如果为1，则表示进入了代码段
        else:
            # 在代码段中遇到了<,>则不替换
            if tmp[i] == '<' or tmp[i] == '>':
                i += 1
                continue
            # 当遇到代码段的结束，则设置标志为0
            if pre == tmp[i]:
                sig = 0
            if pre == content[i: i+3]:
                sig = 0
                i += 3
                continue
        i += 1

    return "".join(tmp)


if __name__ == '__main__':
    xss = '`<script>alert("hello");</script>`'
    content = replace_unsafe_chars(xss)
    print(content)

    xss = '```<script></script>```<script>'
    content = replace_unsafe_chars(xss)
    print(content)

    xss = '<img>'
    content = replace_unsafe_chars(xss)
    print(content)

    xss = '<img javascript>'
    content = replace_unsafe_chars(xss)
    print(content)