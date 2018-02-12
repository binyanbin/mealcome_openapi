
import http.client
import urllib.parse
import time
import uuid

import hashlib

headers = {"Content-type": "application/json;charset:utf-8;", "Content-Encoding": "UTF-8"}
host = "openapi.mealcome.cn"
clientId = "8fa2bc6957b24a8b8bf3dfcbe3a34c81"
clientSecret = "79753124b23147fb82309b0ed9e14533"
accessToken = "2f3c70f34604c478d719e5f4e1bdb84"


def base():
    mytime = int(time.time())
    base_params = {"client_id": clientId, "accessToken": accessToken,
                   "timestamp": str(mytime), "nonce": uuid.uuid1()}
    return base_params


def request(url, params=None, data=None, delete=False):
    base_params = base()
    if params is not None:
        urlParams = dict(base_params, **params)
    else:
        urlParams = base_params
    if data is not None:
        body = json.dumps(data)
        bodymd = (body + clientSecret).encode("utf-8")
        bodySign = hashlib.sha256(bodymd).hexdigest()
        urlParams["bodySign"] = str(bodySign).upper()

    # 排序
    urlParams = sorted(urlParams.items(), key=lambda dict: dict[0])

    # 创建签名字符串并生成签名
    url = url + "?" + urllib.parse.urlencode(urlParams, False, "", "utf-8", None, urllib.parse.quote)
    md = (urllib.parse.unquote(url) + clientSecret).encode("utf-8")
    sign = hashlib.sha256(md).hexdigest()

    # 请求接口
    request = url + "&sign=" + str(sign).upper()
    print("http://" + host + request)
    httpClient = http.client.HTTPConnection(host)
    if delete:
        httpClient.request("DELETE", request)
    else:
        if data is None:
            httpClient.request("GET", request)
        else:
            httpClient.request("POST", request, body)

    response = httpClient.getresponse()
    print(response.read())


if __name__ == '__main__':
    request("/store", None)
    params1 = {"begin": "2018-01-07 00:00:00", "end": "2018-01-09 23:59:59"}
    request("/material/changes", params1)
    params = {"lastDate": "2017-11-04 10:00:00"}
    request("/purchase/receipt/changes", params1)
    request("/supplier/changes", params1)
    supplier = {
        "name": "测试供应商3",
        "fullName": "测试供应商3",
        "phone": "1375514440761",
        "pinyin": "csgys",
        "contacts": "ll",
        "representative": "ss",
        "businessLicense": "lskdfjsdl",
        "bankAccountCode": "sdlkfjsdlf",
        "bankAccountName": "asdfasdf",
        "bacnkBranch": "",
        "bankName": "",
        "note": "",
        "erpCode": "erpcode"
    }
    request("/suppliers", None, supplier)
    request("/suppliers/6014085", None, supplier)
