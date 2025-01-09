from utils.session import random_sleep, create_session_with_retry
from urllib.parse import urljoin
from bs4 import BeautifulSoup
import json
import random
from fake_useragent import UserAgent
import requests

ua = UserAgent()
user_agent = ua.random
headers = {'User-Agent': user_agent}


def get_interview_links(company_name):
    """
    爬取指定公司的所有面試經驗連結
    """

    base_url = "https://www.goodjob.life"
    company_url = f"{base_url}/companies/{company_name}/interview-experiences"
    interview_links = []
    page = 1
    session = create_session_with_retry()

    while True:
        try:
            current_url = company_url if page == 1 else f"{company_url}?p={page}"

            print(f"正在爬取第 {page} 頁的連結...")
            response = session.get(current_url, headers=headers)

            if page > 1 and response.status_code == 404:
                print("已到達最後一頁")
                break

            soup = BeautifulSoup(response.text, 'html.parser')
            experience_containers = soup.find_all('div', class_='InterviewExperiences-module__container___3Nkl0')

            if not experience_containers:
                print("沒有找到更多面試經驗，結束爬取")
                break

            for container in experience_containers:
                link_element = container.find('a')
                if link_element and 'href' in link_element.attrs:
                    relative_link = link_element['href']
                    full_link = urljoin(base_url, relative_link)
                    interview_links.append(full_link)

            page += 1
            random_sleep()

        except requests.exceptions.RequestException as e:
            print(f"爬取第 {page} 頁時發生錯誤: {str(e)}")
            if page > 1:
                break
            else:
                print("第一頁就發生錯誤，請檢查網路連線或公司名稱是否正確")
                break

    session.close()
    return interview_links


def get_interview_details(url, session):
    """
    爬取指定面試經驗連結的詳細內容
    """
    try:
        random_sleep()

        response = session.get(url, headers=headers)

        soup = BeautifulSoup(response.text, 'html.parser')
        script_tag = soup.find('script', string=lambda text: text and 'window.__data' in text)

        if not script_tag:
            return None

        json_text = script_tag.string.split('window.__data=')[1].strip(';')
        data = json.loads(json_text)

        experience_id = url.split('/')[-1]
        experience_data = data['experience']['experienceById'].get(experience_id, {}).get('data', {})

        if not experience_data:
            return None

        interview_info = {
            '面試地區': experience_data.get('region', '未提供'),
            '應徵職稱': experience_data.get('job_title', {}).get('name', '未提供'),
            '面試時間': f"{experience_data.get('interview_time', {}).get('year', '')} 年 {experience_data.get('interview_time', {}).get('month', '')} 月" if experience_data.get(
                'interview_time') else '未提供',
            '面試結果': experience_data.get('interview_result', '未提供')
        }

        sections = experience_data.get('sections', [])
        for section in sections:
            if section.get('subtitle') == '面試過程':
                interview_info['面試過程'] = section.get('content', '未提供')
            elif section.get('subtitle') == '給其他面試者的中肯建議':
                interview_info['給其他面試者的中肯建議'] = section.get('content', '未提供')

        interview_qas = experience_data.get('interview_qas', [])
        if interview_qas:
            interview_info['面試問答'] = [
                {
                    '問題': qa.get('question', '未提供'),
                    '回答': qa.get('answer', '未提供')
                }
                for qa in interview_qas
            ]
        else:
            interview_info['面試問答'] = []

        return interview_info

    except Exception as e:
        print(f"處理 {url} 時發生錯誤: {str(e)}")
        return None
