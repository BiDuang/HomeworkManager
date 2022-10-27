import os
import platform
import json
from Module import Core
from Module import PwdCrypto

if platform.system() == 'Windows':
    clear = 'cls'
else:
    clear = 'clear'

BB_Platform_pwd = PwdCrypto.Crypto_Pwd_Encrypt(input("请重新输入您的BB平台密码: "))
os.system("cls")
KTP_Platform_pwd = PwdCrypto.Crypto_Pwd_Encrypt(input("请重新输入您的课堂派密码: "))
os.system("clear")
Microsoft_pwd = PwdCrypto.Crypto_Pwd_Encrypt(input("请重新输入您的微软账户密码: "))
os.system("clear")
print("请稍候...")
f = open("homeworkManager_info.json", "r", encoding="utf8")
info_dict = json.load(f)
f.close()
info_dict["BB_Info"]["pwd"] = BB_Platform_pwd
info_dict["Microsoft_Info"]["pwd"] = Microsoft_pwd
info_dict["KTP_Info"]["pwd"] = KTP_Platform_pwd
f = open("homeworkManager_info.json", "w", encoding="utf8")
json.dump(info_dict, f, ensure_ascii=False)
f.close()
print("跨平台设置已完成!")
