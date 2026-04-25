import logging
import re
from urllib.parse import urlparse, urlencode, parse_qs, urlunparse
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, filters, ContextTypes
from config import BOT_TOKEN, AFFILIATE_TAG, TARGET_CHANNELS, ALLOWED_USER_IDS

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Supported Amazon domains
AMAZON_DOMAINS = [
    "amazon.com", "amazon.co.jp", "amazon.co.uk", "amazon.de",
    "amazon.fr", "amazon.it", "amazon.es", "amazon.ca",
    "amazon.com.au", "amazon.in", "amzn.to", "amzn.eu", "a.co"
]

def is_amazon_url(url: str) -> bool:
    try:
        parsed = urlparse(url)
        domain = parsed.netloc.lower().lstrip("www.")
        return any(domain == d or domain.endswith("." + d) for d in AMAZON_DOMAINS)
    except:
        return False

def replace_affiliate_tag(url: str, new_tag: str) -> str:
    """Replace or inject affiliate tag into an Amazon URL."""
    try:
        parsed = urlparse(url)
        params = parse_qs(parsed.query, keep_blank_values=True)

        # Remove existing tag if present
        params.pop("tag", None)
        # Inject new tag
        params["tag"] = [new_tag]

        # Flatten params (parse_qs returns lists)
        flat_params = {k: v[0] for k, v in params.items()}
        new_query = urlencode(flat_params)

        new_url = urlunparse((
            parsed.scheme,
            parsed.netloc,
            parsed.path,
            parsed.params,
            new_query,
            parsed.fragment
        ))
        return new_url
    except Exception as e:
        logger.error(f"Error replacing tag in URL {url}: {e}")
        return url

def extract_urls(text: str) -> list[str]:
    url_pattern = r'https?://[^\s<>"\'()]+'
    return re.findall(url_pattern, text)

def process_message_text(text: str) -> tuple[str, bool]:
    """
    Find all Amazon URLs in text, replace affiliate tags.
    Returns (modified_text, was_modified).
    """
    urls = extract_urls(text)
    modified = False
    result = text

    for url in urls:
        if is_amazon_url(url):
            new_url = replace_affiliate_tag(url, AFFILIATE_TAG)
            if new_url != url:
                result = result.replace(url, new_url)
                modified = True
            else:
                modified = True  # Still an Amazon link, counts as processed

    return result, modified

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if ALLOWED_USER_IDS and user_id not in ALLOWED_USER_IDS:
        await update.message.reply_text("⛔ You are not authorized to use this bot.")
        return

    await update.message.reply_text(
        "👋 *Amazon Affiliate Bot*\n\n"
        "Send me any message containing Amazon links and I'll:\n"
        "• Replace affiliate tags with yours\n"
        "• Repost the message to your configured channels\n\n"
        f"Your affiliate tag: `{AFFILIATE_TAG}`\n"
        f"Target channels: {len(TARGET_CHANNELS)} configured\n\n"
        "Just paste your message with Amazon links!",
        parse_mode="Markdown"
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Only respond to DMs
    if update.effective_chat.type != "private":
        return

    user_id = update.effective_user.id
    if ALLOWED_USER_IDS and user_id not in ALLOWED_USER_IDS:
        await update.message.reply_text("⛔ You are not authorized to use this bot.")
        return

    text = update.message.text or update.message.caption or ""
    if not text:
        await update.message.reply_text("⚠️ Please send a text message with Amazon links.")
        return

    modified_text, has_amazon = process_message_text(text)

    if not has_amazon:
        await update.message.reply_text(
            "⚠️ No Amazon links found in your message.\n"
            "Make sure the link starts with https://amazon... or https://amzn.to/..."
        )
        return

    # Show preview to user
    await update.message.reply_text(
        f"✅ *Processed message:*\n\n{modified_text}\n\n"
        f"📤 Posting to {len(TARGET_CHANNELS)} channel(s)...",
        parse_mode="Markdown"
    )

    # Post to all target channels
    success_count = 0
    errors = []

    for channel in TARGET_CHANNELS:
        try:
            await context.bot.send_message(
                chat_id=channel,
                text=modified_text,
                parse_mode="Markdown",
                disable_web_page_preview=False
            )
            success_count += 1
            logger.info(f"Posted to channel {channel}")
        except Exception as e:
            error_msg = str(e)
            errors.append(f"• `{channel}`: {error_msg}")
            logger.error(f"Failed to post to {channel}: {e}")

    # Report back
    if success_count == len(TARGET_CHANNELS):
        await update.message.reply_text(
            f"🎉 Successfully posted to all {success_count} channel(s)!"
        )
    else:
        report = f"📊 Posted to {success_count}/{len(TARGET_CHANNELS)} channels."
        if errors:
            report += "\n\n❌ Errors:\n" + "\n".join(errors)
            report += "\n\nMake sure the bot is an admin in those channels."
        await update.message.reply_text(report, parse_mode="Markdown")

def main():
    if not BOT_TOKEN or BOT_TOKEN == "YOUR_BOT_TOKEN_HERE":
        raise ValueError("Please set BOT_TOKEN in config.py")
    if not AFFILIATE_TAG or AFFILIATE_TAG == "your-tag-20":
        raise ValueError("Please set AFFILIATE_TAG in config.py")
    if not TARGET_CHANNELS:
        raise ValueError("Please add at least one channel to TARGET_CHANNELS in config.py")

    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    logger.info("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
