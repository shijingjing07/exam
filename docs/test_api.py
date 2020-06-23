import requests
import json

url = 'http://127.0.0.1:8000/'
# requests.post方法调三方接口（用的是data）
# r = requests.post(url + 'company/add_friend/', data={'id': zid, 'com_key': com_key})
# key = json.loads(r.text)


# requests.get方法调三方接口（用的是params）
# r = requests.get(url + 'company/search_user/', params={'id': id, 'pub_key': pub_key})
# key = json.loads(r.text)

headers = {
    'Cookie': 'blueking_language=None; csrftoken=azdkFNxhrnOA2sOhRQhvCGUVOLF6sVHG0JUYrb72JeGsn8JIv5qOaa5CeXtxZQRe; bk_token=pwT9MrKlZ9_BncKppFPFTx_7u7bRQDyL0vv0b_GCni4'
}

def test_syncHosts():
    r = requests.get(url + 'syncHosts', headers=headers)
    result = json.loads(r.text)
    print(result)


def test_getHosts():
    r = requests.get(url + 'getHosts', headers=headers, params={'bk_biz_id': '', 'owner': '', 'cur_page': 1, 'per_page': 10})
    print(r.text)


def test_executeSql():
    r = requests.post(url + 'executeSql/', headers=headers, data={'bk_biz_id': 8, 'ips': ['172.25.0.20']})
    print(r.text)


def test_pushFile():
    r = requests.post(url + 'pushFile/', headers=headers, data={'bk_biz_id': 8})
    print(r.text)


def test_createTask():
    r = requests.post(url + 'createTask/', headers=headers, data={'bk_biz_id': 4, 'template_id': 2, 'name': 'ceshi-0622-02', 'sleep_time': 60})
    print(r.text)


def test_startTask():
    r = requests.post(url + 'operateTask/', headers=headers, data={'bk_biz_id': 4, 'task_id': 11, 'action': 'start'})
    print(r.text)


def test_pauseTask():
    r = requests.post(url + 'operateTask/', headers=headers, data={'bk_biz_id': 4, 'task_id': 11, 'action': 'pause'})
    print(r.text)


def test_resumeTask():
    r = requests.post(url + 'operateTask/', headers=headers, data={'bk_biz_id': 4, 'task_id': 11, 'action': 'resume'})
    print(r.text)


def test_revokeTask():
    r = requests.post(url + 'operateTask/', headers=headers, data={'bk_biz_id': 4, 'task_id': 11, 'action': 'revoke'})
    print(r.text)


def test_taskStatus():
    r = requests.post(url + 'taskStatus/', headers=headers, data={'bk_biz_id': 4, 'task_id': 10})
    print(r.text)


def test_taskDetail():
    r = requests.post(url + 'taskDetail/', headers=headers, data={'bk_biz_id': 4, 'task_id': 10})
    print(r.text)


def test_api():
    r = requests.get(url + 'testApi/', headers=headers)
    print(r.text)


test_api()
