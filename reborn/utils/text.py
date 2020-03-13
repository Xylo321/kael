import html2text


def html_to_markdown(html):
    return html2text.html2text(html)
