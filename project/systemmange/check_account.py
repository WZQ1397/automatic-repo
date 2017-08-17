#python day 2
#author zach.wang
import getpass
import time
i = flag = 0
account = {
    "wzq": "123456",
    "xyc": "123456"}
username = input("input your name:")
pwd = getpass.getpass("input your password:")
for key in account:
    if username == key and pwd == account[key]:
        print("\033[52;1mwelcome %s\033[0m;"%(username))
        motd = "this is zach server"
        print(time.ctime())
        #print(time.strftime("%Y-%m-%d %X"))
        print(motd.capitalize().center(50,'-'))
        flag = 1
        time.sleep(30)
if flag != 1:
    print("\033[31;1mno vaild user exist or wrong password!\033[0m")
    exit()


