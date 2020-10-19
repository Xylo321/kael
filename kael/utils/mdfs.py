import requests
from requests_toolbelt import MultipartEncoder
from mimetypes import guess_type
import json


def upload(upload_url, api_key, third_user_id, category_id, title, file_name, file_path):
    m = MultipartEncoder(fields={
        'api_key': api_key,
        'category_id': str(category_id),
        'third_user_id': str(third_user_id),
        'title': title,
        'upload_file_name': (file_name, open(file_path, 'rb'), guess_type(file_name)[0] or "application/octet-stream")
    })
    r = requests.post(upload_url, data=m, headers={'Content-Type': m.content_type}, verify=False)
    r.raise_for_status()
    jd = r.json()
    if jd['status'] == 0:
        return 0
    elif jd['status'] == 1:
        return 1
    else:
        raise


def download(download_url, api_key, third_user_id, category_id, title, expire):
    form_data = {
        'api_key': api_key,
        'third_user_id': third_user_id,
        'category_id': category_id,
        'title': title,
        'expire': expire
    }
    r = requests.get(download_url, params=form_data, verify=False)
    r.raise_for_status()
    jd = r.json()
    if jd['status'] == 0:
        return None
    elif jd['status'] == 1:
        return jd['data'][0]['url']
    else:
        raise


def edit(edit_url, api_key,
         src_third_user_id, src_category_id, src_title, src_file_extension,
         new_third_user_id, new_category_id, new_title, new_file_extension,
         upload_file_name=None, upload_file_path=None):
    m = None
    if upload_file_name is None or upload_file_path is None:
        m = MultipartEncoder(fields={
            'api_key': api_key,
            'src_category_id': str(src_category_id),
            'src_third_user_id': str(src_third_user_id),
            'src_title': src_title,
            'src_file_extension': src_file_extension,
            'new_category_id': str(new_category_id),
            'new_third_user_id': str(new_third_user_id),
            'new_title': new_title,
            'new_file_extension': str(new_file_extension),
        })
    else:
        m = MultipartEncoder(fields={
            'api_key': api_key,
            'src_category_id': str(src_category_id),
            'src_third_user_id': str(src_third_user_id),
            'src_title': src_title,
            'src_file_extension': src_file_extension,
            'new_category_id': str(new_category_id),
            'new_third_user_id': str(new_third_user_id),
            'new_title': new_title,
            'new_file_extension': str(new_file_extension),
            'upload_file_name': (upload_file_name, open(upload_file_path, 'rb'), guess_type(upload_file_name)[0] or "application/octet-stream")
        })
    r = requests.post(edit_url, data=m, headers={'Content-Type': m.content_type}, verify=False)
    r.raise_for_status()
    jd = r.json()
    if jd['status'] == 0:
        return 0
    elif jd['status'] == 1:
        return 1
    else:
        raise


def download_many(download_many_url, api_key, tcts):
    """XXX: tcts: [{third_user_id, category_id, title}]"""
    form_data = {
        'api_key': api_key,
        'data': tcts
    }
    r = requests.get(download_many_url, data=json.dumps(form_data), verify=False)
    r.raise_for_status()
    jd = r.json()
    if jd['status'] == 0:
        # print(None)
        return None
    elif jd['status'] == 1:
        # 下载地址，也就是原来的数据中增加了一个url
        # print(jd['data']) # [{'third_user_id': xxx, 'category_id': xxx, 'title': xxx, 'url': xxx}]
        return jd['data']
    else:
        raise


def get_many_video_first_photo(get_many_video_first_photo_url, api_key, tcts):
    """XXX: tcts: [{third_user_id, category_id, title}]"""
    form_data = {
        'api_key': api_key,
        'data': tcts
    }
    r = requests.get(get_many_video_first_photo_url, data=json.dumps(form_data), verify=False)
    r.raise_for_status()
    jd = r.json()
    if jd['status'] == 0:
        # print(None)
        return None
    elif jd['status'] == 1:
        # 第一帧地址，也就是原来的数据中增加了一个url
        # print(jd['data']) # [{'third_user_id': xxx, 'category_id': xxx, 'title': xxx, 'url': xxx}]
        return jd['data']
    else:
        raise


def delete(delete_url, api_key, third_user_id, category_id, title):
    form_data = {
        'api_key': api_key,
        'third_user_id': third_user_id,
        'category_id': category_id,
        'title': title
    }
    r = requests.post(delete_url, data=form_data, verify=False)
    r.raise_for_status()
    jd = r.json()
    if jd['status'] == 0:
        return 0
    elif jd['status'] == 1:
        return 1
    else:
        raise