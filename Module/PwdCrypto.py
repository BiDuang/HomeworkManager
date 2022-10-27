try:
    import wmi
except:
    pass
import binascii
import os
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad


def Crypto_Pwd_Encrypt(pwd: str) -> str:
    # 加密存储的密码
    try:
        cpu_id = wmi.WMI().Win32_Processor()[0].ProcessorId.strip()
    except:
        r = os.popen("dmidecode -t 4 | grep ID")
        cpu_id = r.read().replace(" ", "").replace("ID:", "").strip()
    aes = AES.new(cpu_id.encode(), AES.MODE_ECB)

    comp_len = 32-pwd.__len__()
    for i in range(0, comp_len-2):
        pwd += "*"
    pwd += str(comp_len)
    result = aes.encrypt(pad(pwd.encode(), 32))
    return binascii.hexlify(result).decode()


def Crypto_Pwd_Decrypt(code: str) -> str:
    # 解密存储的密码
    try:
        cpu_id = wmi.WMI().Win32_Processor()[0].ProcessorId.strip()
    except:
        r = os.popen("dmidecode -t 4 | grep ID")
        cpu_id = r.read().replace(" ", "").replace("ID:", "").strip()
    aes = AES.new(cpu_id.encode(), AES.MODE_ECB)

    code = aes.decrypt(binascii.unhexlify(code)).decode().strip()
    comp_len = int(code[code.__len__()-2: code.__len__()])
    return code[:code.__len__()-comp_len]
