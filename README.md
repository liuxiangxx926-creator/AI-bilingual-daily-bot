# AI 行业双语日报 Agent

基于 RSS 资讯抓取 + 大模型生成的自动化 AI 行业双语日报，每日聚合海外前沿 AI 资讯，输出中英双语精简行业摘要。

## ✨ 功能特点
- 自动抓取 TechCrunch、Hugging Face 等海外主流 AI 媒体资讯
- 智能筛选高价值行业新闻，过滤重复与营销内容
- 专业中英双语翻译，统一行业术语
- 规范 Markdown 格式输出，分类清晰
- 兼容所有 OpenAI 格式的模型网关接口

## 🛠️ 技术栈
- Python 3
- feedparser：RSS 资讯抓取
- OpenAI SDK：大模型调用
- 结构化 Prompt Engineering：输出质量与格式控制

## 🚀 快速开始
1. 安装依赖
```bash
pip install feedparser python-dotenv openai
