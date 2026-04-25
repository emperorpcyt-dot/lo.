# Amazon Affiliate Telegram Bot

Replaces Amazon affiliate tags in any message and reposts to your Telegram channels.

## Setup (5 minutes)

### 1. Create your bot
1. Open Telegram and message **@BotFather**
2. Send `/newbot` and follow the prompts
3. Copy the **API token** you receive

### 2. Get your channel IDs
- Add the bot as an **Admin** to each target channel
- Give it "Post Messages" permission

### 3. Configure the bot
Edit `config.py`:
```python
BOT_TOKEN    = "123456:ABC-your-token-here"
AFFILIATE_TAG = "yourtag-20"          # your Amazon affiliate tag
TARGET_CHANNELS = ["@yourchannel"]    # channels to post to
ALLOWED_USER_IDS = [123456789]        # your Telegram user ID (optional but recommended)
```

### 4. Install & run
```bash
pip install -r requirements.txt
python bot.py
```

## Usage
1. DM your bot any message containing Amazon links
2. The bot replaces all affiliate tags with yours
3. It automatically reposts to all configured channels
4. You get a confirmation with success/error per channel

## Supported Amazon domains
amazon.com · amazon.co.jp · amazon.co.uk · amazon.de · amazon.fr
amazon.it · amazon.es · amazon.ca · amazon.com.au · amazon.in
amzn.to · amzn.eu · a.co (short links)

## Run 24/7 (optional)
To keep it always running on a server:
```bash
# Using screen
screen -S affiliatebot
python bot.py
# Press Ctrl+A then D to detach

# Or using systemd / PM2 / Docker as preferred
```
