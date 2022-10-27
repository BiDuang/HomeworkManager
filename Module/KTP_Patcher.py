from playwright.sync_api import sync_playwright
from Module import PwdCrypto
from Module import Core
from Module import Microsoft_Request

global ktp_info

ktp_info = Core.Core_Config_Load()["KTP_Info"]


def KTP_Homework_Time_Formatter(datestr: str, timestr: str) -> str:
    datestr = "20"+datestr

    return datestr+"T"+timestr


def KTP_Platform_Patcher(token: str) -> None:

    playwright = sync_playwright().start()
    browser = playwright.firefox.launch(headless=True)
    context = browser.new_context(locale="zh-CN")
    page = context.new_page()
    page.goto("https://www.ketangpai.com/#/login")
    page.get_by_placeholder("请输入邮箱/手机号/账号").fill(ktp_info["account"])
    page.get_by_placeholder("请输入密码").fill(
        PwdCrypto.Crypto_Pwd_Decrypt(ktp_info["pwd"]))
    page.get_by_placeholder("请输入密码").press("Enter")
    page.wait_for_url("https://www.ketangpai.com/#/main")
    for subject in ktp_info["subjects_info"]:
        page.goto(subject)
        page.wait_for_selector("[class=\"info-title\"]", state="visible")

        subject_name = page.locator(
            "[class=\"text_overflow1\"]").all_inner_texts()[0]
        homework_info = page.locator(
            "[class=\"layout-right-info\"]").all_inner_texts()

        for h in homework_info:
            cur_h = h.split("\n")
            print(cur_h)
            homework_name = cur_h[0]
            deadline_list = cur_h[1].replace(
                "提交截止时间：", "").replace("已结束", "")[:14].split(" ")
            deadline = KTP_Homework_Time_Formatter(
                deadline_list[0], deadline_list[1])
            event_prefix = ""
            if(cur_h[3] != "未提交"):
                print("[!] 此任务已完成")
                event_prefix = "[已完成]"
            Microsoft_Request.Microsoft_Event_Add(
                event_prefix+subject_name, homework_name, deadline, "课堂派", token)
    page.close()
    context.close()
    playwright.stop()
