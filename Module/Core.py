import json


def Core_Config_Init() -> None:
    init_dict = {
        "BB_Info": {},
        "Microsoft_Info": {},
        "KTP_Info": {}
    }

    f = open("homeworkManager_info.json", "w", encoding="utf8")
    json.dump(init_dict, f, ensure_ascii=False)
    f.close()


def Core_Config_Load() -> dict:

    f = open("homeworkManager_info.json", "r", encoding="utf8")
    info_dict = json.load(f)
    f.close()

    return info_dict


def Core_Config_Save(unit: str, data) -> None:

    f = open("homeworkManager_info.json", "r", encoding="utf8")
    info_dict = json.load(f)
    f.close()
    info_dict[unit] = data
    f = open("homeworkManager_info.json", "w", encoding="utf8")
    json.dump(info_dict, f, ensure_ascii=False)
    f.close()
