#!/usr/bin/env python3
"""
Firstpost → WhatsApp Daily News Snapshot
Fetches headlines via Google News RSS, summarizes with Claude,
and sends via Meta's WhatsApp Cloud API.
"""

import os
import time
from datetime import datetime
import requests
import anthropic
from bs4 import BeautifulSoup
from config.settings import (
    META_ACCESS_TOKEN,
    META_PHONE_NUMBER_ID,
    YOUR_WHATSAPP_NUMBER,
    SECTIONS,
    MAX_ARTICLES_PER_CATEGORY,
)

META_API_URL = f"https://graph.facebook.com/v19.0/{META_PHONE_NUMBER_ID}/messages"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/120.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
}


# ─────────────────────────────────────────────
# 1. SUMMARIZE WITH CLAUDE
# ─────────────────────────────────────────────

def summarize_from_text(title: str, description: str) -> str:
    """Summarize a news item using its title and RSS description."""
    try:
        content = description if len(description) > 50 else title
        client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
        message = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=120,
            messages=[{
                "role": "user",
                "content": (
                    "Write a 2 sentence summary of this news story. "
                    "Be factual and concise. No intro, just the summary:\n\n"
                    f"Headline: {title}\n\n"
                    f"Context: {content[:1000]}"
                ),
            }],
        )
        return message.content[0].text.strip()
    except Exception as e:
        print(f"      ⚠️  Summarization failed: {e}")
        return title


# ─────────────────────────────────────────────
# 2. FETCH HEADLINES FROM GOOGLE NEWS RSS
# ─────────────────────────────────────────────

def fetch_section(name: str, url: str) -> list[dict]:
    """Fetch Firstpost headlines for a category via Google News RSS."""
    try:
        response = requests.get(url, timeout=15, headers=HEADERS)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "xml")

        articles = []
        for item in soup.find_all("item")[:MAX_ARTICLES_PER_CATEGORY]:
            title       = item.find("title")
            link        = item.find("link")
            description = item.find("description")

            if title and link:
                clean_title = title.get_text(strip=True).replace(" - Firstpost", "").strip()
                desc_text   = BeautifulSoup(
                    description.get_text(strip=True) if description else "",
                    "html.parser"
                ).get_text(strip=True)

                print(f"      ✍️  Summarizing: {clean_title[:50]}...")
                summary = summarize_from_text(clean_title, desc_text)
                articles.append({
                    "title": clean_title,
                    "summary": summary,
                    "category": name,
                })
        return articles

    except Exception as e:
        print(f"⚠️  Failed to fetch [{name}]: {e}")
        return []


def fetch_all_news() -> dict[str, list[dict]]:
    """Fetch and summarize news from all configured sections."""
    all_news = {}
    for name, url in SECTIONS.items():
        print(f"📡 Fetching {name}...")
        articles = fetch_section(name, url)
        if articles:
            all_news[name] = articles
            print(f"   ✅ {len(articles)} articles")
        else:
            print(f"   ⚠️  No articles found")
    return all_news


# ─────────────────────────────────────────────
# 3. FORMAT WHATSAPP MESSAGES
# ─────────────────────────────────────────────

CATEGORY_EMOJI = {
    "Top Stories":   "🔥",
    "India":         "🇮🇳",
    "World":         "🌍",
    "Politics":      "🏛",
    "Business":      "💼",
    "Technology":    "💻",
    "Sports":        "⚽",
    "Entertainment": "🎬",
}


def format_message(all_news: dict[str, list[dict]]) -> list[str]:
    """Format news into clean, concise WhatsApp message chunks."""
    now = datetime.now().strftime("%A, %d %B %Y")
    chunks = []

    # Header
    chunks.append(
        f"🗞 *Firstpost Daily Digest*\n"
        f"📅 {now}\n"
        f"━━━━━━━━━━━━━━━━━━━━"
    )

    # One message per category
    for category, articles in all_news.items():
        emoji = CATEGORY_EMOJI.get(category, "📌")
        lines = [f"{emoji} *{category}*"]
        for article in articles:
            lines.append(f"\n• *{article['title']}*")
            lines.append(f"{article['summary']}")
        chunks.append("\n".join(lines))

    # Footer
    chunks.append("━━━━━━━━━━━━━━━━━━━━\n_Stay informed • Firstpost_")
    return chunks


# ─────────────────────────────────────────────
# 4. SEND VIA META WHATSAPP CLOUD API
# ─────────────────────────────────────────────

def send_text_message(text: str) -> bool:
    """Send a single text message via Meta WhatsApp Cloud API."""
    headers = {
        "Authorization": f"Bearer {META_ACCESS_TOKEN}",
        "Content-Type": "application/json",
    }
    payload = {
        "messaging_product": "whatsapp",
        "recipient_type": "individual",
        "to": YOUR_WHATSAPP_NUMBER,
        "type": "text",
        "text": {"preview_url": False, "body": text},
    }
    try:
        response = requests.post(META_API_URL, headers=headers, json=payload, timeout=10)
        response.raise_for_status()
        msg_id = response.json().get("messages", [{}])[0].get("id", "unknown")
        print(f"   ✅ Sent (id: {msg_id})")
        return True
    except requests.HTTPError as e:
        print(f"   ❌ HTTP {e.response.status_code}: {e.response.text}")
        return False
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False


def send_digest(chunks: list[str]) -> bool:
    """Send all message chunks with a short delay between each."""
    print(f"\n📤 Sending {len(chunks)} message(s) to {YOUR_WHATSAPP_NUMBER}...")
    success = True
    for i, chunk in enumerate(chunks, 1):
        print(f"   Sending part {i}/{len(chunks)}...")
        if not send_text_message(chunk):
            success = False
        if i < len(chunks):
            time.sleep(1)
    return success


# ─────────────────────────────────────────────
# 5. MAIN
# ─────────────────────────────────────────────

def main():
    print("=" * 50)
    print("🚀 Firstpost → WhatsApp (Meta Cloud API)")
    print("=" * 50)

    if not META_ACCESS_TOKEN or "EAA" not in META_ACCESS_TOKEN:
        print("❌ META_ACCESS_TOKEN not configured.")
        return
    if not META_PHONE_NUMBER_ID or META_PHONE_NUMBER_ID == "YOUR_PHONE_NUMBER_ID":
        print("❌ META_PHONE_NUMBER_ID not configured.")
        return
    if not os.getenv("ANTHROPIC_API_KEY"):
        print("❌ ANTHROPIC_API_KEY not set.")
        return

    all_news = fetch_all_news()
    if not all_news:
        print("❌ No news fetched. Aborting.")
        return

    chunks = format_message(all_news)
    print(f"\n📝 Prepared {len(chunks)} message chunk(s)")

    success = send_digest(chunks)
    print("\n🎉 Digest sent successfully!" if success else "\n💥 Some messages failed.")


if __name__ == "__main__":
    main()
