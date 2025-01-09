from goodjob_web.crawl_contents import get_interview_links, get_interview_details
from goodjob_web.format_content import format_interview_info
from ptt_crawler.techjob_content_crawler import fetch_ptt_urls, fetch_ptt_article
from utils.session import create_session_with_retry
from utils.file_processor import save_interviews_to_file


def main():
    user_input = input("爬取平台:")

    if user_input == "goodjob":

        try:
            company_name = input("請輸入要爬取的公司名稱: ")
            print(f"開始爬取 {company_name} 的面試經驗")

            # 爬取所有面試連結
            links = get_interview_links(company_name)
            if not links:
                print(f"無法找到 {company_name} 的連結，程式結束")
                return

            print(f"\n共找到 {len(links)} 個面試經驗連結")

            # 建立 session 用於爬取詳細內容
            session = create_session_with_retry()

            # 爬取每個連結的詳細內容
            all_interviews = []
            for i, link in enumerate(links, 1):
                interview_info = get_interview_details(link, session)
                if interview_info:
                    all_interviews.append(interview_info)
                    print(format_interview_info(interview_info))

            session.close()

            if not all_interviews:
                print(f"無法獲取 {company_name} 的內容，程式結束")
                return

            save_interviews_to_file(all_interviews, company_name, user_input)

        except Exception as e:
            print(f"error: {str(e)}")

    elif user_input == "ptt":
        try:
            query = input("輸入要爬取的 PTT 文章主題: ")
            base_url = 'https://www.ptt.cc/bbs/Soft_Job'
            urls = fetch_ptt_urls(base_url, query)

            # 爬取文章內容
            for url in urls:
                article_content, time, title = fetch_ptt_article(url)
                save_interviews_to_file(article_content, f"ptt_{time}_{title}", user_input)

        except Exception as e:
            print(f"error: {str(e)}")
    else:
        print("目前只有支援 goodjob 和 ptt")


if __name__ == "__main__":
    main()
