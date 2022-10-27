import json
import requests
from playwright.sync_api import sync_playwright
from Module import Core
from Module import PwdCrypto


def Microsoft_Get_Token() -> str:
    print("请稍候...正在请求微软令牌")
    Microsoft_Info = Core.Core_Config_Load()["Microsoft_Info"]
    playwright = sync_playwright().start()
    browser = playwright.firefox.launch(headless=True)
    context = browser.new_context(locale="zh-CN")
    page = context.new_page()
    page.goto("https://login.microsoftonline.com/consumers/oauth2/v2.0/authorize?client_id=1aefa904-b887-4fbf-98fc-10185b7b8049&response_type=token&redirect_uri=https%3A%2F%2Fstudio.friendship.org.cn%2F&scope=Calendars.ReadWrite+offline_access&state=114514&response_mode=fragment")
    page.wait_for_load_state()
    page.locator("[name=\"loginfmt\"]").fill(
        Microsoft_Info["account"])
    page.locator("[id=\"idSIButton9\"]").click()

    page.locator("[name=\"passwd\"]").fill(
        PwdCrypto.Crypto_Pwd_Decrypt(Microsoft_Info["pwd"]))
    page.locator("[id=\"idSIButton9\"]").click()

    page.locator("[id=\"idBtn_Back\"]").click()

    if(page.get_by_role("heading", name="是否允许此应用访问你的信息?").count() != 0):
        page.get_by_role("button", name="是").click()

    page.wait_for_url(
        "https://studio.friendship.org.cn/*", timeout=180000)
    token = page.url.split("&")[0].removeprefix(
        "https://studio.friendship.org.cn/#access_token=")

    page.close()
    context.close()
    playwright.stop()
    return token


def Microsoft_Calendar_Refresh(token: str) -> None:
    Microsoft_Info = Core.Core_Config_Load()["Microsoft_Info"]
    post_dict = {
        "name": "作业日程_HomeworkManager",
        "color": "auto"
    }
    json_headers = {"Content-Type": "application/json",
                    "Accept": "application/json",
                    "Authorization": f"Bearer {token}"}
    r = requests.delete(
        f"https://graph.microsoft.com/v1.0/me/calendars/{Microsoft_Info['calendar_id']}",
        headers=json_headers)
    r = requests.post("https://graph.microsoft.com/v1.0/me/calendars",
                      json=post_dict, headers=json_headers)
    calendar_id = json.loads(r.text)["id"]
    Microsoft_Info["calendar_id"] = calendar_id
    Core.Core_Config_Save("Microsoft_Info", Microsoft_Info)


def Microsoft_Event_Add(subject: str, homework_name: str, dead_line: str, platform: str, token: str) -> None:

    Microsoft_Info = Core.Core_Config_Load()["Microsoft_Info"]
    post_dict = {
        "subject": f"{subject} {homework_name}",
        "body": {
            "contentType": "HTML",
            "content": f"{subject}课程的{homework_name}将在今日截止提交!\n请前往{platform}进行提交。"
        },
        "start": {
            "dateTime": f"{dead_line}",
            "timeZone": "China Standard Time"
        },
        "end": {
            "dateTime": f"{dead_line}",
            "timeZone": "China Standard Time"
        },
        "location": {
            "displayName": f"{platform}"
        },
        "importance": "high",
        "isReminderOn": True
    }

    json_headers = {"Content-Type": "application/json",
                    "Accept": "application/json",
                    "Authorization": f"Bearer {token}"}

    r = requests.post(f"https://graph.microsoft.com/v1.0/me/calendars/{Microsoft_Info['calendar_id']}/events",
                      json=post_dict, headers=json_headers)
    if(r.status_code == 201):
        print("日程已添加")
