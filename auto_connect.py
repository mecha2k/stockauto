from pywinauto import application
from dotenv import load_dotenv
import time
import os

load_dotenv(verbose=True)
user_id = os.getenv("USER_ID")
user_passwd = os.getenv("USER_PASSWD")
cert_passwd = os.getenv("CERT_PASSWD")

os.system("taskkill /IM coStarter* /F /T")
os.system("taskkill /IM CpStart* /F /T")
os.system("taskkill /IM DibServer* /F /T")
os.system("wmic process where \"name like '%coStarter%'\" call terminate")
os.system("wmic process where \"name like '%CpStart%'\" call terminate")
os.system("wmic process where \"name like '%DibServer%'\" call terminate")
time.sleep(5)

app = application.Application()
app_arg = "C:/Program Files (x86)/cybos5/STARTER/ncStarter.exe /prj:cp "
app_arg += f"/id:{user_id} /pwd:{user_passwd} /pwdcert:{cert_passwd} /autostart"
print(app_arg)
# app.start('C:\CREON\STARTER\coStarter.exe /prj:cp /id:userid /pwd:pa$$word /pwdcert:certPa$$word /autostart')
# time.sleep(60)