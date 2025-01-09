import os

from goodjob_web.format_content import format_interview_info


def save_interviews_to_file(articles, title, web_name):
    """
    將所有面試資訊保存到 txt 檔案

    Args:
        articles (list): 所有面試資訊的列表
        title (str): 公司名稱或是文章標題
        web_name (str): 爬取網站名稱
    """

    # 指定資料夾路徑，如果指定資料夾不存在，則創建資料夾
    folder_name = f'./content_folder/{web_name}'
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

    # 定義檔案名稱和路徑
    if web_name == "goodjob":
        title = title.replace(':', '_').replace('/', '_').replace('\\', '_').replace(' ', '_')
        filename = os.path.join(folder_name, f"{title}_{web_name}_面試心得.txt")
    elif web_name == "ptt":
        title = title.replace(':', '_').replace('/', '_').replace('\\', '_').replace(' ', '_')
        filename = os.path.join(folder_name, f"{title}.txt")
    else:
        print("目前只有支援 goodjob 和 ptt")
        return

    try:
        with open(filename, 'w', encoding='utf-8') as f:
            # 寫入標題
            if web_name == "goodjob":
                f.write(f"{title}\n")
                f.write(f"共 {len(articles)} 筆面試經驗\n")
                f.write("\n\n")

                # 寫入每筆面試資訊
                for idx, interview in enumerate(articles, 1):
                    try:
                        # 提取面試時間和應徵職稱
                        interview_time = interview.get('面試時間', '未知時間')
                        job_title = interview.get('應徵職稱', '未知職稱')
                        # 寫入標題
                        f.write("---\n\n")
                        f.write(f"## {interview_time}_{job_title}_面試心得\n")
                        # 寫入排版後的面試資訊
                        f.write(format_interview_info(interview))
                        f.write("\n")
                    except Exception as e:
                        print(f"寫入第 {idx} 筆面試資訊時發生錯誤: {str(e)}")
                        f.write("寫入面試資訊時發生錯誤\n")
                        continue
            elif web_name == "ptt":
                f.write(articles)

        print(f"\n面試資訊已保存至 {filename}")

    except Exception as e:
        print(f"保存檔案時發生錯誤: {str(e)}")
