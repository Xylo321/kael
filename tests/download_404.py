import requests

download_url = "http://t1.hxzdhn.com/mmonly/2012/201208/009/14.jpg"

r = requests.get(download_url, stream=True)
print(r.status_code)

with open('./x.' + download_url.rsplit('/')[-1], 'wb') as f:
    f.write(r.content)
