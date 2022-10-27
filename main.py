import os
import platform
from Module import BB_Patcher, KTP_Patcher, Microsoft_Request

version = "Dev 1.5.5"
if platform.system() == 'Windows':
    clear = 'cls'
    env = "Windows"
else:
    clear = 'clear'
    env = "Linux"
os.system(clear)

print(f"===== HomeworkManager {version} =====")
print(f"  HomeworkManager 正在运行在{env}环境中")

token = Microsoft_Request.Microsoft_Get_Token()
BB_Patcher.BB_Platform_Patcher(token)
KTP_Patcher.KTP_Platform_Patcher(token)

print("日程设置完毕，程序结束")