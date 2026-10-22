import feedparser
from datetime import datetime, timezone

# 新闻源列表
RSS_SOURCES = [
    {"name": "TechCrunch AI", "url": "https://techcrunch.com/category/artificial-intelligence/feed/"},
    {"name": "The Verge AI", "url": "https://www.theverge.com/rss/ai/index.xml"},
    {"name": "Hugging Face Blog", "url": "https://huggingface.co/blog/feed.xml"},
]

def fetch_daily_news():
    news_list = []

    for source in RSS_SOURCES:
        print(f"正在抓取：{source['name']}...")
        try:
            feed = feedparser.parse(source["url"])
            source_name = source["name"]
            print(f"  抓到 {len(feed.entries)} 条内容")

            for entry in feed.entries:
                try:
                    pub_time = datetime(*entry.published_parsed[:6], tzinfo=timezone.utc)
                    news_list.append({
                        "title": entry.title,
                        "link": entry.link,
                        "summary": entry.summary,
                        "source": source_name,
                        "published": pub_time.isoformat()
                    })
                except Exception:
                    continue
        except Exception as e:
            print(f"  抓取失败：{e}")

    # 按标题去重
    unique_news = list({n["title"]: n for n in news_list}.values())
    # 按发布时间从新到旧排序
    unique_news.sort(key=lambda x: x["published"], reverse=True)
    return unique_news

if __name__ == "__main__":
    news = fetch_daily_news()
    print(f"\n总共抓到 {len(news)} 条新闻")
    # 打印前3条看看效果
    for n in news[:3]:
        print(f"\n- [{n['source']}] {n['title']}")
