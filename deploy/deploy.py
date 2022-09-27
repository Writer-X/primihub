# 暂时假定我们需要启动的节点只有三个，分别是node0,node1,node2.
# node0:单独尝试

# distribute docker-compose.ymal
'''
usr0 = "xt"
passwd0 = "1"
ip0 = "192.168.91.130"
port0 = "22"
'''

import os
'''
os.system("scp docker-compose.yml " + usr0 + "@" + ip0 + ":/home/xt")
os.system("scp docker-compose-dev.yml " + usr0 + "@" + ip0 + ":/home/xt")
'''


# ssh execute docker—compose in different virtual machine
'''
import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())  
ssh.connect(ip0,port0)
os.system("docker-compose up -d")
'''

import paramiko
import sys

#远程连接cmd

def sshExeCMD(ip,username,password,port=22):
    #定义一个变量ssh_clint
    ssh_client=paramiko.SSHClient()
    #通过这个set_missing_host_key_policy方法用于实现登录是需要确认输入yes，否则保存
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    #使用cnnect类来连接服务器
    #ssh_client.connect(hostname=ip0, port=port0, username=usr0, password=passwd0)
    try:
    #使用cnnect类来连接服务器
        ssh_client.connect(hostname=ip, port=port, username=username, password=password)
    #如果上边命令报错吧报错信息定义到err变量，并输出。
    except Exception as err:
        print("服务器链接失败！！！"% ip)
        print(err)
        #如果报错使用sys的exit退出脚本
        sys.exit()

    #使用exec_command方法执行命令，并使用变量接收命令的返回值并用print输出
    stdin, stdout, stderr = ssh_client.exec_command("pwd")
    print(stdout.read().decode("utf-8"))

#    stdin, stdout, stderr = ssh_client.exec_command("docker-compose up -d")
#    print(stdout.read())

#   传输文件
def sshPutfile(ip, port, username, password, localfile, remotedir):
    #获取源文件的文件名,把进来的localfile变量的值处理只剩文件名
    file_name = os.path.basename(localfile)

    #处理服务器目录名，如果输入的目录名没有带后边的/(不是以/结尾)则添加一个，方便后边拼接文件名
    if not remotedir.endswith("/"):
        remotedir = remotedir + "/"
    dest_file_name = remotedir + file_name

    #创建ssh连接
    ssh_conn = paramiko.Transport((ip, port))
    ssh_conn.connect(username=username, password=password)
    #创建ftp工具（变量）
    ftp_client = paramiko.SFTPClient.from_transport(ssh_conn)
    #上传文件
    ftp_client.put(localfile, dest_file_name)
    # 关闭ssh连接
    ssh_conn.close()


if __name__ == '__main__':
    servers = {
        "192.168.91.130":{
            "username": "xt",
            "password": "1",
            "port": 22,
            "source_file": r"G:\xutong\start\docker-compose.yml",
            "remote_dir": "/home/xt"
        },
        # 添加对剩余的服务器
    }
    '''
    source_file = input("请输入源文件路径（绝对路径）：")
    remote_dir = input("服务器路径（绝对路径）：")
    '''

    for ip,info in servers.items():
        sshPutfile(
            ip=ip,
            port=info.get("port"),
            username=info.get("username"),
            password=info.get("password"),
            localfile=info.get("source_file"),
            remotedir=info.get("remote_dir"),
        ) 
        sshExeCMD(
            ip=ip,
            username=info.get("username"),
            password=info.get("password"),
            port=info.get("port")
        )
# sshExeCMD()




