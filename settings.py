"""
Configuration for Firstpost → WhatsApp (Meta Cloud API).
"""

import os

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
