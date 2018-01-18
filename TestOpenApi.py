
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


def get(url, params):
    base_params = base()
    if params is not None:
        urlParams = dict(base_params, **params)
    else:
        urlParams = base_params \
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
    httpClient.request("GET", request)
    response = httpClient.getresponse()
    print(response.read())




if __name__ == '__main__':
    get("/store", None)
    params1 = {"begin": "2018-01-07 00:00:00", "end": "2018-01-09 23:59:59"}
    get("/material/changes", params1)
    params = {"lastDate": "2017-11-04 10:00:00"}
    get("/purchase/receipt/changes", params1)
    get("/supplier/changes",params1)
