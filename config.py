# ============================================================
#  AMAZON AFFILIATE TELEGRAM BOT — CONFIGURATION
# ============================================================

# 1. Your Telegram Bot Token (get from @BotFather on Telegram)
BOT_TOKEN = "8751962828:AAFMkmB85r1wqoM4ycKl9RPDPNTHMgMNlIc"

# 2. Your Amazon affiliate tag (e.g. "yourtag-20")
AFFILIATE_TAG = "abid0d0-21"

# 3. Channels to post to.
#    Use @channelusername format OR the numeric channel ID (e.g. -1001234567890)
#    The bot MUST be an admin with "Post Messages" permission in each channel.
TARGET_CHANNELS = [
    "-1002088363884",
    "-1003313180875",
    # "-1001234567890",   # numeric ID example
]

# 4. (Optional) Restrict bot to specific Telegram user IDs.
#    Leave as empty list [] to allow anyone who finds the bot to use it.
#    Find your user ID by messaging @userinfobot on Telegram.
ALLOWED_USER_IDS = [
    # 123456789,   # your Telegram user ID
]
