"""日报推送模块：支持飞书群机器人 Webhook 和 SMTP 邮件推送。

所有配置均来自环境变量（本地写在 .env，勿提交）：
  LARK_WEBHOOK   飞书自定义机器人 Webhook 地址（可选）
  SMTP_HOST      SMTP 服务器，如 smtp.qq.com（可选）
  SMTP_PORT      SMTP 端口，QQ 邮箱 SSL 为 465
  SMTP_USER      发件邮箱账号
  SMTP_PASS      SMTP 授权码（不是邮箱登录密码！）
  MAIL_TO        收件人，多个用英文逗号分隔
"""
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import requests

# 飞书卡片里 markdown 元素的内容上限（保守值），超出则分段
FEISHU_CHUNK_LIMIT = 6000


def _split_text(text: str, limit: int = FEISHU_CHUNK_LIMIT):
    """按段落把长文本切成若干段，避免超过飞书单条消息上限。"""
    chunks, buf, size = [], [], 0
    for para in text.split("\n\n"):
        para_size = len(para) + 2
        if size + para_size > limit and buf:
            chunks.append("\n\n".join(buf))
            buf, size = [], 0
        buf.append(para)
        size += para_size
    if buf:
        chunks.append("\n\n".join(buf))
    return chunks


def send_feishu(title: str, md_text: str):
    """通过飞书自定义机器人发送 Markdown 卡片消息。"""
    webhook = os.getenv("LARK_WEBHOOK", "").strip()
    if not webhook:
        print("未配置 LARK_WEBHOOK，跳过飞书推送")
        return

    elements = []
    for chunk in _split_text(md_text):
        elements.append({"tag": "markdown", "content": chunk})

    payload = {
        "msg_type": "interactive",
        "card": {
            "config": {"wide_screen_mode": True},
            "header": {
                "title": {"tag": "plain_text", "content": title},
                "template": "blue",
            },
            "elements": elements,
        },
    }

    resp = requests.post(webhook, json=payload, timeout=15)
    data = resp.json()
    # 自定义机器人返回 {"code":0,...} 或 {"StatusCode":0,...}
    ok = data.get("code") == 0 or data.get("StatusCode") == 0
    if ok:
        print("✅ 飞书推送成功")
    else:
        print(f"⚠️ 飞书推送失败：{data}")


def _markdown_to_html(md_text: str) -> str:
    """把 Markdown 转成适合邮件阅读的 HTML。"""
    try:
        import markdown
        return markdown.markdown(md_text, extensions=["tables", "fenced_code"])
    except ImportError:
        # 兜底：纯文本展示
        return "<pre style='white-space:pre-wrap'>" + md_text + "</pre>"


def send_email(subject: str, md_text: str):
    """通过 SMTP 发送 HTML 邮件。任一必需配置缺失则跳过。"""
    host = os.getenv("SMTP_HOST", "").strip()
    user = os.getenv("SMTP_USER", "").strip()
    password = os.getenv("SMTP_PASS", "").strip()
    to_raw = os.getenv("MAIL_TO", "").strip()
    port = int(os.getenv("SMTP_PORT", "465").strip() or 465)

    if not (host and user and password and to_raw):
        print("SMTP 配置不完整（需 SMTP_HOST/SMTP_USER/SMTP_PASS/MAIL_TO），跳过邮件推送")
        return

    receivers = [addr.strip() for addr in to_raw.split(",") if addr.strip()]
    html = (
        "<html><body style='font-family:-apple-system,'Segoe UI',sans-serif;"
        "max-width:720px;margin:0 auto;line-height:1.7;color:#222'>"
        + _markdown_to_html(md_text)
        + "<hr><p style='color:#999;font-size:12px'>本邮件由 AI 双语日报 Agent 自动发送</p>"
        "</body></html>"
    )

    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = user
    msg["To"] = ", ".join(receivers)
    msg.attach(MIMEText(md_text, "plain", "utf-8"))
    msg.attach(MIMEText(html, "html", "utf-8"))

    with smtplib.SMTP_SSL(host, port, timeout=30) as server:
        server.login(user, password)
        server.sendmail(user, receivers, msg.as_string())
    print(f"✅ 邮件已发送至 {', '.join(receivers)}")


def notify_all(title: str, md_text: str):
    """把日报推送到所有已配置的渠道。"""
    try:
        send_feishu(title, md_text)
    except Exception as e:
        print(f"⚠️ 飞书推送异常：{e}")
    try:
        send_email(title, md_text)
    except Exception as e:
        print(f"⚠️ 邮件推送异常：{e}")
