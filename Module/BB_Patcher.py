from playwright.sync_api import sync_playwright
from Module import PwdCrypto
from Module import Core
from Module import Microsoft_Request

global bb_info

bb_info = Core.Core_Config_Load()["BB_Info"]


def BB_Homework_Time_Formatter(datestr: str, timestr: str) -> str:
    datestr = datestr.replace("年", "-").replace("月", "-").replace("日", "T")
    if(timestr.startswith("星期")):
        timestr = timestr[3:]
    if(timestr.startswith("上午")):
        timestr = timestr[2:]
        if(int(timestr.split(":")[0]) < 10):
            timestr = timestr.replace(
                timestr[:1], "0"+str(int(timestr[:1])))
    elif(timestr.startswith("下午")):
        timestr = timestr[2:]
        if(int(timestr.split(":")[0]) >= 10):
            timestr = timestr.replace(timestr[:2], str(int(timestr[:2])+12))
        else:
            timestr = timestr.replace(
                timestr[:1], str(int(timestr[:1])+12))
    if(timestr[:2] == "24"):
        timestr = "23:59"

    return datestr+timestr


def BB_Homework_Iter(homework: list) -> list:
    homework_name = []
    for i in homework:
        homework_name.append(i["name"])
    return homework_name


def BB_Platform_Patcher(token:str) -> None:

    with sync_playwright() as playwright:
        browser = playwright.firefox.launch(headless=True)
        context = browser.new_context(locale="zh-CN")

        page = context.new_page()
        page.goto(
            "http://id.ouc.edu.cn:8071/sso/login?service=https://wlkc.ouc.edu.cn/webapps/bb-sso-BBLEARN/index.jsp")
        page.get_by_placeholder("工号/学号").fill(bb_info["account"])

        page.get_by_placeholder("请输入密码").fill(
            PwdCrypto.Crypto_Pwd_Decrypt(bb_info["pwd"]))

        page.get_by_placeholder("请输入密码").press("Enter")

        page.get_by_role("button", name="确定").click()

        page.wait_for_url(
            "https://wlkc.ouc.edu.cn/webapps/portal/execute/tabs/tabAction?tab_tab_group_id=_1_1")
        i = 0
        Microsoft_Request.Microsoft_Calendar_Refresh(token)
        for subject in bb_info["subjects_info"]:
            page.get_by_role("link", name=subject["subject_entrance"]).click()
            page.wait_for_url(subject["subject_redirect_page"][0])

            page.get_by_role("link", name=subject["homework_link"]).click()
            page.wait_for_url(subject["subject_redirect_page"][1])

            homework = page.locator("[id=\"content_listContainer\"]").locator(
                "[class=\"item clearfix\"]").all_inner_texts()
            print(homework)
            for h in homework:
                isFinished = False
                page.get_by_role("link", name=h).click()
                page.wait_for_load_state()
                if(page.locator(
                        "[class=\"attempt gradingPanelSection\"]").count() != 0):
                    deadline_time = page.locator(
                        "[class=\"attempt gradingPanelSection\"]").inner_text().split("\n")[5].strip()
                    print("[!] 此任务已完成")
                    isFinished = True
                else:
                    deadline_time = page.locator(
                        "[class=\"metaField\"]").all_inner_texts()[0].replace("\n", "").strip()
                deadline_list = deadline_time.split(" ")
                if(isFinished):
                    event_prefix = "[已完成]"
                else:
                    event_prefix = ""
                Microsoft_Request.Microsoft_Event_Add(event_prefix+subject["subject_entrance"][27:], h, BB_Homework_Time_Formatter(
                    deadline_list[0], deadline_list[1]), "BB平台", token)
                page.go_back()
            i += 1
            page.goto(
                "https://wlkc.ouc.edu.cn/webapps/portal/execute/tabs/tabAction?tab_tab_group_id=_1_1")
        context.close()
        browser.close()
