import requests
import api_url
import xml.etree.ElementTree as ET


from datetime import datetime, timedelta
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

current_date = datetime.now()

yesterday = current_date - timedelta(days=1)
yesterday_date = yesterday.date()


def filter_items_project(items, url):
    filtered_items = []
    instt_name = [
        "조달청",
        "국토",
        "과학",
        "중소",
        "경기",
        # "대구",
        "산업",
        "고용",
        "환경",
        "특허",
        "금융",
    ]
    filter_keyword_noticename = [
        "1인",
        "여성",
        "재도약","창업","재창업","의료","바이오","로봇","헬스케어","온라인"
        "[부산]",
        "[경북]",
        "[전북]",
        "[경남]",
        "[전남]",
        "[충북]",
        "[충남]",
        "[광주]",
        "[제주]",
        "[강원]",
        "[세종]",
        "[인천]",
        "[울산]",
        "[대전]",
    ]
    filter_keyword_exc = [
        "섬유",
        "농업","디자인"
    ]


    if url == api_url.URL_PROJECT_BIZINFO:  # 기업마당
        for item in items:
            creatPnttm = item.get("creatPnttm")  # 등록일시
            pblancNm = item.get("pblancNm")  # 공고명
            jrsdInsttNm = item.get("jrsdInsttNm")  # 소관부처
            excInsttNm =  item["excInsttNm"]  # 수행기관


            date = datetime.strptime(creatPnttm, "%Y-%m-%d %H:%M:%S")
            date_only = date.date()

            # 어제공고만 뽑기
            if date_only >= yesterday_date:
                if (
                    any(keyword in jrsdInsttNm for keyword in instt_name)
                    and not any(keyword in pblancNm for keyword in filter_keyword_noticename)
                    and not any(keyword in excInsttNm for keyword in filter_keyword_exc)
                ):
                    filtered_items.append(item)
            
            # # 쭉 다 뽑기
            # if (
            #         any(keyword in jrsdInsttNm for keyword in instt_name)
            #         and not any(keyword in pblancNm for keyword in filter_keyword_noticename)
            #         and not any(keyword in excInsttNm for keyword in filter_keyword_exc)
            #     ):
            #         filtered_items.append(item)


    return filtered_items


def get_project(url):
    params = {}
    if url == api_url.URL_PROJECT_BIZINFO:
        params["searchCnt"] = 500
        # params["pageUnit"] = 50
        # params["pageIndex"] = 12

    try:
        response = requests.get(url, params=params, verify=False, timeout=60)
        if response.status_code == 200:
            try:
                data = response.json()
                # print(data)
                total_count = data["jsonArray"][0]["totCnt"]
                print(total_count)
                items = data["jsonArray"]
                filtered_items = filter_items_project(items, url)
                print(len(filtered_items))
                return filtered_items
            except (KeyError, requests.exceptions.JSONDecodeError) as e:
                print(f"Error occurred while parsing JSON: {e}")
    except requests.exceptions.Timeout:
        print("서버 응답 시간이 초과되었습니다. 요청이 실패했습니다.")
        return None


def get_project_bizinfo():
    return get_project(api_url.URL_PROJECT_BIZINFO)
