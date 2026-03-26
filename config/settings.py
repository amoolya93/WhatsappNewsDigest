"""
Configuration for Firstpost → WhatsApp (Meta Cloud API).
All secrets are read from environment variables — never hardcode them here.
"""

import os

# ─────────────────────────────────────────────
# CREDENTIALS — set these as environment variables
# or as GitHub repository secrets for automated runs
# ─────────────────────────────────────────────
META_ACCESS_TOKEN    = os.getenv("META_ACCESS_TOKEN")
META_PHONE_NUMBER_ID = os.getenv("META_PHONE_NUMBER_ID")
YOUR_WHATSAPP_NUMBER = os.getenv("YOUR_WHATSAPP_NUMBER")
# ANTHROPIC_API_KEY is read directly via os.getenv() in news_sender.py


# ─────────────────────────────────────────────
# NEWS SECTIONS — Google News RSS filtered to Firstpost
# Comment out any categories you don't want
# ─────────────────────────────────────────────
SECTIONS = {
    "Top Stories":   "https://news.google.com/rss/search?q=site:firstpost.com&hl=en-IN&gl=IN&ceid=IN:en",
    "India":         "https://news.google.com/rss/search?q=site:firstpost.com+india&hl=en-IN&gl=IN&ceid=IN:en",
    "World":         "https://news.google.com/rss/search?q=site:firstpost.com+world&hl=en-IN&gl=IN&ceid=IN:en",
    "Politics":      "https://news.google.com/rss/search?q=site:firstpost.com+politics&hl=en-IN&gl=IN&ceid=IN:en",
    "Business":      "https://news.google.com/rss/search?q=site:firstpost.com+business&hl=en-IN&gl=IN&ceid=IN:en",
    "Technology":    "https://news.google.com/rss/search?q=site:firstpost.com+technology&hl=en-IN&gl=IN&ceid=IN:en",
    "Sports":        "https://news.google.com/rss/search?q=site:firstpost.com+sports&hl=en-IN&gl=IN&ceid=IN:en",
    "Entertainment": "https://news.google.com/rss/search?q=site:firstpost.com+entertainment&hl=en-IN&gl=IN&ceid=IN:en",
}

# Headlines per category (2-3 recommended for readable messages)
MAX_ARTICLES_PER_CATEGORY = 2
