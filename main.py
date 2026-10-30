import os
from datetime import datetime
from src.fetcher import fetch_daily_news
from src.daily_agent import generate_report
from src.notifier import notify_all

def main():
    print("正在抓取今日资讯...")
    news_list = fetch_daily_news()
    print(f"抓取完成，共 {len(news_list)} 条")

    if not news_list:
        print("无可用资讯，退出")
        return

    print("正在生成日报...")
    report_content = generate_report(news_list)

    # 保存到 daily 文件夹
    today_str = datetime.now().strftime("%Y-%m-%d")
    os.makedirs("daily", exist_ok=True)
    file_path = f"daily/{today_str}.md"

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(f"# AI 行业双语日报 | {today_str}\n\n")
        f.write(report_content)
        f.write("\n\n---\n*本日报由 AI 自动生成，基于公开 RSS 资讯整理*")

    print(f"✅ 日报已生成：{file_path}")

    # 推送到已配置的渠道（飞书 / 邮箱），未配置则自动跳过
    notify_all(f"AI 行业双语日报 | {today_str}", report_content)

if __name__ == "__main__":
    main()