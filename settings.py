"""
Configuration for Firstpost → WhatsApp (Meta Cloud API).
"""

import os

# ─────────────────────────────────────────────
# META WHATSAPP CLOUD API CREDENTIALS
# ─────────────────────────────────────────────
META_ACCESS_TOKEN    = os.getenv("META_ACCESS_TOKEN",    "EAAW9oNxbt3QBRIoBP7AJQOoTNpXWX9AiZCNLS8Xwb4iTkgDaaNEnkaO8sL3eO8IlUmbkoWj6D6YiA8naoY3mrMX9z9ZCu7F0tEcZCQuBOGem7VgPfR2XfcTCX1PuSdu2oqZBvVtgPW79Ty2DE6uks62Kzxe4evxVCener4icuCesah7GUU87LrqWMfZB89YIxiQZDZD")
META_PHONE_NUMBER_ID = os.getenv("META_PHONE_NUMBER_ID", "1008724628996675")
YOUR_WHATSAPP_NUMBER = os.getenv("YOUR_WHATSAPP_NUMBER", "0919844154991")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "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")

# ─────────────────────────────────────────────
# FIRSTPOST SECTION PAGES TO SCRAPE
# Comment out any sections you don't want
# ─────────────────────────────────────────────
SECTIONS = {
    "Top Stories":   "https://www.firstpost.com/",
    "India":         "https://www.firstpost.com/india/",
    "World":         "https://www.firstpost.com/world/",
    "Politics":      "https://www.firstpost.com/politics/",
    "Business":      "https://www.firstpost.com/business/",
    "Technology":    "https://www.firstpost.com/tech/",
    "Sports":        "https://www.firstpost.com/firstcricket/",
    "Entertainment": "https://www.firstpost.com/entertainment/",
}

# Headlines per category
MAX_ARTICLES_PER_CATEGORY = 3
