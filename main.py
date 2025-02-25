import api
import spreadsheet
import slack
import config
import datetime
import time


today = datetime.date.today().strftime("%Y-%m-%d")  # 오늘 날짜 가져오기 (YYYY-MM-DD 형식)
message_bid = f"*{today}*\n"
message_project = f"*{today}*\n"


def process_data_project(data, category):
    global message_project

    if data:
        if category == "기업마당":
            sheet_index = 0
        else:
            print(f"sheet_index error. category =={category}")
            return
        spreadsheet.save_data_project(data, sheet_index)  # sheet1 = 0,  sheet2 = 1 ...
        message_project += f"*{category}* 지원사업을 스크랩했습니다 ({len(data)})\n"
    else:
        print(f" {category} 지원사업 데이터를 가져오는데 실패했습니다.")
        message_project += f"*{category}* 지원사업 데이터가 없습니다 \n"

    if category == "기업마당":
        message_project += f"{config.SPREADSHEET_LINK2}"
        print(message_project)
        slack.send_message(message_project)



def main():
   
    # 기업마당 api
    project_bizinfo = api.get_project_bizinfo()
    process_data_project(project_bizinfo, "기업마당")
    time.sleep(1)


if __name__ == "__main__":
    main()
