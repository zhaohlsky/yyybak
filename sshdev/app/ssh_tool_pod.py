import paramiko
import time,os,re
import pymysql

#任务list，装以下的类的实例
task_list = []
ip_mac = {}
mac_ip = {}
#数据表对应类
class Task():
    def __init__(self, id, name, ip, user, passwd, turn_on, check_over, cmd, type, port, sqlresult):  # 构造函数
        self.id = id
        self.name = name
        self.ip = ip
        self.user = user
        self.passwd = passwd
        self.turn_on = turn_on
        self.check_over = check_over
        self.cmd = cmd
        self.type = type
        self.port = port
        self.sqlresult = sqlresult
    def sshANDcmd(self):
        """连接ssh，并执行cmd"""
        print(self.name.title() + " is now pending.")
        # 创建SSH对象
        ssh = paramiko.SSHClient()
        # 允许连接不在know_hosts文件中的主机
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())  # 第一次登录的认证信息
        # 连接服务器
        ssh.connect(hostname=self.ip, port=self.port, username=self.user, password=self.passwd)
        # 执行命令
        stdin, stdout, stderr = ssh.exec_command(self.cmd)  #
        time.sleep(1)
        # 获取命令结果
        res, err = stdout.read(), stderr.read()
        result = res if res else err
        #print(result.decode())
        self.sqlresult = result.decode()
        # 关闭连接
        ssh.close()
    def arpResult(self):
        if self.type != "core":
            return
        for ipstr in self.sqlresult.split('\n'):
            result = re.findall(
                r"\b(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\b", ipstr)
            if result:
                ip = result[0]
                mac = ipstr.split()[2]
                ip_mac[ip] = mac
                mac_ip[mac] = ip

class MysqlConnect():
    def __init__(self):
        self.dbIp = "172.17.250.251"
        self.dbUser = "root"
        self.dbPasswd = "8888dhcc"
        self.db = "dev"
        self.dbPort = 22
    def getMysqlinfo(self):
        # 打开mysql数据库前的准备，获取环境变量
        self.dbIp = os.getenv("MYSQL_ADDR")
        self.dbUser = "root"
        self.dbPasswd = os.getenv("MYSQL_ROOT_PASSWORD")
        self.db = os.getenv("MYSQL_DB")
        self.dbPort = int(os.getenv("MYSQL_PORT"))
    def connectMysql(self):
        db = pymysql.connect(host=self.dbIp, user=self.dbUser, password=self.dbPasswd, database=self.db, port=self.dbPort)
        # 使用 cursor() 方法创建一个游标对象 cursor
        cursor = db.cursor()
        # 使用 execute()  方法执行 SQL 查询
        cursor.execute("SELECT * from task_dev where turn_on=1 ")
        data = cursor.fetchall()
        for task in data:
            task_list.append(Task(task[0], task[1], task[2], task[3], task[4], task[5], task[6], task[7], task[8], task[9],"no result"))
        db.close()
    def uploadMysql(self):
        db = pymysql.connect(host=self.dbIp, user=self.dbUser, password=self.dbPasswd, database=self.db, port=self.dbPort)
        # 使用 cursor() 方法创建一个游标对象 cursor
        cursor = db.cursor()
        # 使用 execute()  方法执行 SQL 查询
        for ip in ip_mac:
            mac = ip_mac[ip]
            sqluploadcmd = "INSERT INTO result_log(log) VALUES("+"'"+ip+":"+mac+"'"+");" #只有ip
            print(sqluploadcmd)
            cursor.execute(sqluploadcmd)
            # 涉及写操作要提交
        db.commit()
        cursor.close()
        db.close()


mysqlconnect = MysqlConnect()
mysqlconnect.getMysqlinfo()
mysqlconnect.connectMysql()
#测试类方法
for t in task_list:
    t.sshANDcmd()
    t.arpResult()

mysqlconnect.uploadMysql()






