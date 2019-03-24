import os
import datetime
import time
import ftplib
import paramiko
import sys

# 需要监听的本地文件夹，需要修改
minitor_dir="XXX/XXX"

# 远程目录
remote_file="XXX/XXX"
# 服务器ip
host = '**.**.**.**'
#用户名
username = '******'
# 密码
password = '******'

laste_time_recoder=[]
now_time_recoder=[]
need_updata_files=[]

client = paramiko.Transport((host,22))
client.connect( username=username,password=password)
sftp = paramiko.SFTPClient.from_transport(client)

# 监听函数
def monitor():
	global laste_time_recoder
	global now_time_recoder
	global need_updata_files
	list_= os.listdir(minitor_dir)

	filelist = []
	for i in os.walk(minitor_dir):
		root=i[0]
		f_list=i[2]
		for f in f_list:
			filelist.append(os.path.join(root,f))


	if laste_time_recoder==[]:
		for path in filelist:
			if os.path.isdir(path):
				continue
			timestamp = os.path.getmtime(path)
			laste_time_recoder.append((path,timestamp))
	else:
		now_time_recoder=[]
		for path in filelist:
			if os.path.isdir(path):
				continue
			timestamp = os.path.getmtime(path)
			now_time_recoder.append((path,timestamp))

	need_updata_files=[item for item in now_time_recoder if item not in laste_time_recoder]


# 处理文件更新
def process():
	for updata_f,timestamp in need_updata_files:
		sftp.put(updata_f,os.path.join(remote_file,updata_f.split("/")[-1]))
		print("更新了文件{}".format(updata_f))

def main():
	global laste_time_recoder
	global now_time_recoder
	global need_updata_files


	while True :
		monitor()
		if need_updata_files!=[]:
			process()
			now_time_recoder=[]
			need_updata_files=[]
			laste_time_recoder=[]
		time.sleep(1)



if __name__ == '__main__':
	main()
