import requests
import json
import time
import DES
import Login

# 学号和密码输入在这里:
global account
global result

get_data_url = "https://hainanu.campusphere.net/wec-counselor-sign-apps/stu/sign/getStuSignInfosInOneDay"
detial_url = "https://hainanu.campusphere.net/wec-counselor-sign-apps/stu/sign/detailSignInstance"
signurl = "https://hainanu.campusphere.net/wec-counselor-sign-apps/stu/sign/submitSign"
def get_headers(account):
    cookie = Login.GetCookie(account)
    headers = {
        "extension": "1",
        "Cpdaily-Extension": DES.GetExtension(account['userId']),
        "Cookie": 'acw_tc=' + cookie['acw_tc'] + '; MOD_AUTH_CAS=' + cookie['MOD_AUTH_CAS'],
        "Content-Type": "application/json; charset=utf-8",
        "User-Agent": "mmp"
    }
    return headers



def get_signAll(headers):
	res = requests.post(url = get_data_url, data = json.dumps({}), headers = headers, timeout = 10)
	print(res.text)
	try:
		data = json.loads(res.text)
		mmp = data["datas"]["unSignedTasks"]
		task = []
		for i in mmp:
			task.append((i["signInstanceWid"], i["signWid"]))
		return task
	except Exception as e:
		print(res.text)


def get_extraFieldItemWid(ids,headers):
	data = {
		"signInstanceWid": ids[0],
		"signWid": ids[1]
	}
	res = requests.post(url = detial_url, data = json.dumps(data), headers = headers, timeout = 10)
	mmp = json.loads(res.text)["datas"]["extraField"][0]["extraFieldItems"]
	for i in mmp:
		if "以下" in i["content"]:
			return i["wid"]


def signed(signInstanceWid, extraFieldItemWid,headers):
	data = {
		"signInstanceWid": str(signInstanceWid),
		"longitude": 110.336933,
		"latitude": 20.06208,
		"isMalposition": 0,
		"abnormalReason": "",
		"signPhotoUrl": "",
		"position": "中国海南省海口市美兰区椰风中路",
		"isNeedExtra": "1",
		"extraFieldItems": [{
			"extraFieldItemValue": "37.2℃及以下",
			"extraFieldItemWid": str(extraFieldItemWid)
		}]
	}
	res = requests.post(url = signurl, headers = headers, data = json.dumps(data), timeout = 100)# proxies = {'http': '127.0.0.1:8080','https': '127.0.0.1:8080'}, verify = False)
	print(res.text)
	if "SUCCESS" in res.text:
		print("[+] " + str([signInstanceWid, extraFieldItemWid]))
		#requests.post(url = "http://sc.ftqq.com/SCU129264Taa5a8b8efa2a1cc73e88a624fa611b6b5fbc68962dc03.send",data = r"text=成功&desp=自动签到".encode('utf-8'),headers = {"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"})
	else :
		print(str([signInstanceWid, extraFieldItemWid]))


def check_in(account):
    headers = get_headers(account)
    localtime = time.asctime(time.localtime(time.time()))
    print(localtime)
    print("======================================================================")
    tasks = get_signAll(headers)

    for i in tasks:
        signed(i[0], get_extraFieldItemWid(i,headers),headers)
    print("======================================================================")


