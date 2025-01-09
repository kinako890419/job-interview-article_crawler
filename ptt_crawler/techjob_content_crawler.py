import requests
from bs4 import BeautifulSoup
from utils.session import random_sleep


def fetch_ptt_urls(base_url, query_topic):
    urls = []
    page = 1

    while True:
        try:
            complete_url = f"{base_url}/search?page={page}&q={query_topic}"
            response = requests.get(complete_url)
            response.encoding = 'utf-8'
            soup = BeautifulSoup(response.text, 'html.parser')
            entries = soup.find_all('div', class_='r-ent')
            if not entries:
                print('No more entries')
                break
            for entry in entries:
                # print(entries)
                title_tag = entry.find('div', class_='title').find('a')
                if title_tag:
                    article_url = f"https://www.ptt.cc{title_tag['href']}"
                    print(article_url)
                    urls.append(article_url)
            page += 1
            random_sleep()

        except Exception as e:
            print(f"Error fetching URLs on page {page}: {str(e)}")
            break
    return urls


def fetch_ptt_article(url_link):
    response = requests.get(url_link)
    response.encoding = 'utf-8'
    soup = BeautifulSoup(response.text, 'html.parser')

    # 文章標題&時間
    title = soup.find_all('span', class_='article-meta-value')[-2].text
    time = soup.find_all('span', class_='article-meta-value')[-1].text

    # 內文
    main_content = soup.find(id='main-content')
    for tag in main_content.find_all(['div', 'span']):
        tag.decompose()
    content = main_content.text.strip()

    # 排版
    formatted_content = f"""
## {title}
### 發文時間：{time}

{content}
"""

    return formatted_content, time, title


if __name__ == "__main__":
    base_url = 'https://www.ptt.cc/bbs/Soft_Job'
    query = '軟體面試心得'
    urls = fetch_ptt_urls(base_url, query)

    for url in urls:
        print(fetch_ptt_article(url))
