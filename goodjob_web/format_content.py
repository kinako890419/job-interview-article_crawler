import os


def format_interview_info(info):
    """
    格式化面試資訊為易讀的文字格式
    """

    if not info:
        return "無法獲取面試資訊"

    try:
        formatted_text = f"""
面試地區：{info['面試地區']}
應徵職稱：{info['應徵職稱']}
面試時間：{info['面試時間']}
面試結果：{info['面試結果']}

【面試過程】
{info['面試過程']}

【給其他面試者的建議】
{info['給其他面試者的中肯建議']}"""

        if info['面試問答']:
            formatted_text += f"\n\n【面試問答】"
            for i, qa in enumerate(info['面試問答'], 1):
                formatted_text += f"\n{i}. 問：{qa['問題']}"
                if qa['回答']:
                    formatted_text += f"\n   答：{qa['回答']}"

        formatted_text += f"\n"

        return formatted_text

    except Exception as e:
        print(f"格式化面試資訊時發生錯誤: {str(e)}")
        return "格式化面試資訊時發生錯誤"
