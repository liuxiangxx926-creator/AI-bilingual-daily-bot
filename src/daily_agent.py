import os
from dotenv import load_dotenv
from openai import OpenAI

# 读取 .env 里的配置
load_dotenv()

# 系统提示词（Agent 的核心规则）
SYSTEM_PROMPT = """
你是AI行业资深编辑与专业中英译者。
任务：处理输入的AI资讯列表，完成筛选、要点总结、中英双语翻译、分类与排序，最终生成一份精简的行业日报。

严格遵守以下规则：
1. 筛选：从全部资讯中选出4-6条最具行业价值的内容，排除重复、纯营销、无实质信息的内容。
2. 每条内容严格固定结构，顺序和符号绝对不能改：
   ### 【分类】中文标题
   🔗 来源：媒体名称 | [原文链接](url)
   📝 中文摘要：1-2句话，直接陈述核心事实与行业意义，专业凝练
   🌐 English Summary: 对应英文精简摘要，符合海外科技媒体地道表达
3. 标题统一使用三级标题（###），禁止使用四级或其他层级。
4. 每条内容之间空一行，整体排版干净整齐。
5. 分类仅可选：模型发布 | 产品更新 | 行业动态 | 安全监管 | 开源生态
6. 排序：按事件重要性从高到低排列
7. 翻译要求：AI专有名词统一使用业内通用译法，避免生硬机翻；中文正式流畅，英文简洁地道。
8. 严谨性要求：涉及内部测试、未证实的消息，需自然体现审慎性，但不要使用“所提供资讯称”“据报道”这类套话。
9. 只输出标准Markdown正文，不要任何开场白、解释语、结束语、多余符号。

【输出示例，严格参照此格式】
### 【安全监管】Anthropic提出联邦AI安全框架，设50人致死风险作为模型拦截门槛
🔗 来源：TechCrunch | [原文链接](https://techcrunch.com)
📝 中文摘要：Anthropic推出一项联邦AI安全政策方案，建议仅当法官判定模型可能造成至少50人死亡的致命风险时，才可禁止其发布。该方案旨在以高风险阈值划定监管边界，避免对主流AI系统造成过度监管。
🌐 English Summary: Anthropic has proposed a federal AI safety policy framework that would allow judges to block model releases only if they pose a lethal risk to 50 or more people. The proposal aims to draw a regulatory line at high-risk scenarios without overburdening mainstream AI systems.
"""

def generate_report(news_list):
    # 把新闻列表拼成输入文本
    news_text = "\n\n".join([
        f"标题：{n['title']}\n来源：{n['source']}\n链接：{n['link']}\n摘要：{n['summary']}"
        for n in news_list
    ])

    # 初始化客户端
    client = OpenAI(
        base_url=os.getenv("LLM_BASE_URL"),
        api_key=os.getenv("LLM_API_KEY")
    )

    # 调用模型生成
    response = client.chat.completions.create(
        model=os.getenv("LLM_MODEL"),
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"以下是今日AI资讯列表：\n{news_text}\n\n请生成今日双语日报。"}
        ]
    )

    return response.choices[0].message.content.strip()
