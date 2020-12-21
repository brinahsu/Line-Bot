import os
import json

from linebot import LineBotApi, WebhookParser
from linebot.models import MessageEvent, TextMessage, TextSendMessage
from linebot.models import *

channel_access_token = os.getenv("LINE_CHANNEL_ACCESS_TOKEN", None)


def send_text_message(reply_token, text):
    line_bot_api = LineBotApi(channel_access_token)
    line_bot_api.reply_message(reply_token, TextSendMessage(text=text))

    return "OK"


def send_sticker_message(reply_token, package_id, sticker_id):
    line_bot_api = LineBotApi(channel_access_token)
    message = StickerSendMessage(package_id=package_id, sticker_id=sticker_id)
    line_bot_api.reply_message(reply_token, message)

    return "OK"


def send_flex_message(reply_token, alt_text, s1):
    line_bot_api = LineBotApi(channel_access_token)
    message = FlexSendMessage(alt_text=alt_text, contents=json.loads(s1))
    line_bot_api.reply_message(reply_token, message)

    return "OK"


"""
def send_image_url(id, img_url):
    pass

def send_button_message(id, text, buttons):
    pass
"""
