# -*- coding:utf-8 -*-
__author__ = "zhaohlsky"

import paramiko

ssh = paramiko.SSHClient()  # 创建SSH对象
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())  # 允许连接不在know_hosts文件中的主机
ssh.connect(hostname='192.168.3.230', port=22, username='root', password='ag.localhost')  # 连接服务器

stdin, stdout, stderr = ssh.exec_command("/etc/init.d/teleport status | grep not | wc -l")  # 执行命令并获取命令结果
# stdin为输入的命令
# stdout为命令返回的结果
# stderr为命令错误时返回的结果
res, err = stdout.read(), stderr.read()
result = res if res else err
resultnum = int(bytes.decode(result))
if resultnum > 0:
    print("AG STATUS:  "+str(resultnum)+"  IS NOT WORKING")
    print("NEW TASK:   /etc/init.d/teleport restart")
    stdin, stdout, stderr = ssh.exec_command('/etc/init.d/teleport start')
    result = res if res else err
else:
    print("AG STATUS:  "+str(resultnum)+"  IS NOT WORKING")
    print("NO NEW TASK")
ssh.close()  # 关闭连接
