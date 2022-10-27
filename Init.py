import json
import os
import time
from playwright.sync_api import sync_playwright
try:
    import pyautogui
except:
    pass
from Module import Microsoft_Request, PwdCrypto
from Module import Core
import requests

Core.Core_Config_Init()
print(f"---[Homework Manager]---")
print("欢迎使用 HomeworkManager, 初始化程序即将开始...")
print("在配置过程中可能会有弹窗，请注意您的任务栏是否有弹窗提示!")
time.sleep(5)


def BB_Platform_Init() -> None:
    os.system("cls")
    BB_Info = {
        "account": "",
        "pwd": "",
        "subjects_info": []
    }
    print("欢迎使用 BB平台 配置向导!")

    account = input("请输入您的 BB平台 账号: ")
    pwd = input("请输入您的 BB平台 密码: ")
    os.system("cls")

    print("请稍候...程序正在存储你的设置\n请勿关闭程序或计算机")
    BB_Info["account"] = account
    BB_Info["pwd"] = PwdCrypto.Crypto_Pwd_Encrypt(pwd)
    print("即将弹出一个浏览器会话，请按照程序要求继续操作...")
    playwright = sync_playwright().start()
    browser = playwright.firefox.launch(headless=False)
    context = browser.new_context(locale="zh-CN")
    page = context.new_page()
    page.goto(
        "http://id.ouc.edu.cn:8071/sso/login?service=https://wlkc.ouc.edu.cn/webapps/bb-sso-BBLEARN/index.jsp")
    page.get_by_placeholder("工号/学号").fill(account)
    page.get_by_placeholder("请输入密码").fill(pwd)
    pwd = ""
    page.get_by_placeholder("请输入密码").press("Enter")
    page.wait_for_url(
        "https://wlkc.ouc.edu.cn/webapps/portal/execute/tabs/tabAction?tab_tab_group_id=_1_1")

    page.get_by_role("button", name="确定").click()

    userSubjects = page.locator("[id=\"column1\"]").locator(
        "[id=\"_22_1termCourses_noterm\"]").locator(
        "[class=\"portletList-img courseListing coursefakeclass \"]").get_by_role("link").all_inner_texts()
    pyautogui.alert(  # type: ignore
        f"共找到{userSubjects.__len__()}个学科\n请返回程序页面选择您希望追踪的学科", "HomeworkManager")

    selectedSubject: list = []
    while(True):
        i = 0
        os.system("cls")
        print("请输入您希望追踪的学科，完成选择后，请输入\"quit\":")
        for subject in userSubjects:
            print(f"{i+1} : {subject}")
            i += 1
        user_input = input("请在此输入：")
        if user_input == "quit":
            break
        try:
            selectedSubject.append(userSubjects.pop(int(user_input)-1))
        except:
            print("输入有误，请重试")
            time.sleep(3)

    for subject in selectedSubject:
        redirect_url = []
        page.get_by_role("link", name=subject).click()
        page.wait_for_load_state()

        redirect_url.append(page.url)
        homework_link = input("请输入左侧菜单中，作业列表的链接全称: ")
        page.get_by_role("link", name=homework_link).click()
        page.wait_for_load_state()
        redirect_url.append(page.url)

        print(page.locator("[id=\"content_listContainer\"]").locator(
            "[class=\"item clearfix\"]").all_inner_texts())
        if(input("如果获取的作业表正确，请输入\"1\"，否则请随意输入一个值: \n") != "1"):
            selectedSubject.insert(0, subject)
        else:
            BB_Info["subjects_info"].append({
                "subject_entrance": subject,
                "subject_redirect_page": redirect_url,
                "homework_link": homework_link
            })

        page.goto(
            "https://wlkc.ouc.edu.cn/webapps/portal/execute/tabs/tabAction?tab_tab_group_id=_1_1")
    page.close()
    context.close()
    playwright.stop()
    Core.Core_Config_Save("BB_Info", BB_Info)


def KTP_Platform_Init() -> None:
    os.system("cls")
    KTP_Info = {
        "account": "",
        "pwd": "",
        "subjects_info": []
    }
    print("欢迎使用 课堂派 配置向导!")

    account = input("请输入您的 课堂派 账号: ")
    pwd = input("请输入您的 课堂派 密码: ")
    os.system("cls")

    print("请稍候...程序正在存储你的设置\n请勿关闭程序或计算机")
    KTP_Info["account"] = account
    KTP_Info["pwd"] = PwdCrypto.Crypto_Pwd_Encrypt(pwd)
    print("即将弹出一个浏览器会话，请按照程序要求继续操作...")
    playwright = sync_playwright().start()
    browser = playwright.firefox.launch(headless=False)
    context = browser.new_context(locale="zh-CN")
    page = context.new_page()
    page.goto("https://www.ketangpai.com/#/login")
    page.get_by_placeholder("请输入邮箱/手机号/账号").fill(account)
    page.get_by_placeholder("请输入密码").fill(pwd)
    pwd=""
    page.get_by_placeholder("请输入密码").press("Enter")
    page.wait_for_url("https://www.ketangpai.com/#/main")
    pyautogui.alert(  # type: ignore
        "请您点击您希望追踪的课程，并打开作业信息页面。\n完成后，请返回程序页面按要求操作。")
    while(True):
        print("请确认您已打开了作业信息页面后且页面加载完全，复制浏览器的链接至此处")
        print("如果不再准备添加追踪课程，请输入\"quit\"")
        user_in = input().strip()
        if(user_in == "quit"):
            break
        KTP_Info["subjects_info"].append(user_in)
        page.goto(user_in)
        page.wait_for_selector("[class=\"info-title\"]")
        print(page.locator("[class=\"info-title\"]").all_inner_texts())
        if(input("如果获取的作业表正确，请输入\"1\"，否则请随意输入一个值: \n") != "1"):
            KTP_Info["subjects_info"].pop()
            os.system("cls")
            print("已重置，请重新前往作业页面")
            continue
        page.goto("https://www.ketangpai.com/#/main")
    page.close()
    context.close()
    playwright.stop()
    Core.Core_Config_Save("KTP_Info", KTP_Info)


def Microsoft_Platform_Init() -> None:
    os.system("cls")
    Microsoft_Info = {
        "account": "",
        "pwd": "",
        "calendar_id": ""
    }
    print("欢迎使用 微软账户 配置向导!")
    print("本程序将代你向 Friendship Studio 授予程序所需的相关权限，详细信息请访问项目主页")
    print("你随时可以在 https://microsoft.com/consent 撤回你的权限许可 ")

    account = input("请输入您的 微软账户 账号: ")
    pwd = input("请输入您的 微软账户 密码: ")
    os.system("cls")
    print("请稍候...程序正在存储你的设置\n请勿关闭程序或计算机")
    Microsoft_Info["account"] = account
    Microsoft_Info["pwd"] = PwdCrypto.Crypto_Pwd_Encrypt(pwd)

    Core.Core_Config_Save("Microsoft_Info", Microsoft_Info)
    os.system("cls")
    print("请稍候...程序正在设置您的联机日历\n请勿关闭程序或计算机")
    post_dict = {
        "name": "作业日程_HomeworkManager",
        "color": "auto"
    }
    json_headers = {"Content-Type": "application/json",
                    "Accept": "application/json",
                    "Authorization": f"Bearer {Microsoft_Request.Microsoft_Get_Token()}"}
    print("正在新建日历...")
    r = requests.post("https://graph.microsoft.com/v1.0/me/calendars",
                      json=post_dict, headers=json_headers)
    calendar_id = json.loads(r.text)["id"]
    Microsoft_Info["calendar_id"] = calendar_id
    Core.Core_Config_Save("Microsoft_Info", Microsoft_Info)


Microsoft_Platform_Init()
BB_Platform_Init()
KTP_Platform_Init()
print("您已经完成所有的设置，向导程序即将退出!\n祝您使用愉快!")
print("Friendship Studio | Powered by BiDuang | 2022")
