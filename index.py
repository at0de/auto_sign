from check_in import check_in
import requests

def check_in_all():
	f = open("user_password.txt").readlines()

	account = {}
	success = 0
	for i in range(len(f)):
		a = f[i].split("----")
		account['userId'] = a[0]
		account['password'] = a[1][:-1]
		check_in(account)
		success += 1
	if success == len(f):
		#requests.post(url = "http://sc.ftqq.com/xxx.send",data = r"text=成功&desp=自动签到".encode('utf-8'),headers = {"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"})
		print("success")



#阿里云云函数
def handler():
	check_in_all()
#
# #腾讯云云函数
# def main_handler():
#	check_in_all()