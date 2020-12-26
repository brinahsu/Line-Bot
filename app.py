import os
import sys

from flask import Flask, jsonify, request, abort, send_file
from dotenv import load_dotenv
from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, PostbackEvent

from fsm import TocMachine
from utils import send_text_message

load_dotenv()


machine = TocMachine(
    states=["user", "preview",
            "welcome", "select_version", "movie_intro", "select_cinema", "show_time", "show_location"],
    transitions=[
        {
            "trigger": "want",
            "source": ["welcome", "user", "show_location"],
            "dest": "preview",
            "conditions": "is_going_to_preview",
        },
        {
            "trigger": "advance",
            "source": "user",
            "dest": "welcome",
            "conditions": "is_going_to_welcome",
        },
        {
            "trigger": "intro",
            "source": ["user", "preview", "welcome", "select_version", "select_cinema", "show_time"],
            "dest": "movie_intro",
            "conditions": "is_going_to_movie_intro",
        },
        {
            "trigger": "search",
            "source": ["user", "preview", "welcome", "movie_intro", "select_cinema", "show_time"],
            "dest": "select_version",
            "conditions": "is_going_to_select_version",
        },
        {
            "trigger": "select_cinema",
            "source": ["select_version"],
            "dest": "select_cinema",
            "conditions": "is_going_to_select_cinema",
        },
        {
            "trigger": "show_time",
            "source": ["select_cinema"],
            "dest": "show_time",
            "conditions": "is_going_to_show_time",
        },
        {
            "trigger": "where",
            "source": ["user", "preview", "welcome", "select_version", "movie_intro", "select_cinema", "show_time"],
            "dest": "show_location",
            "conditions": "is_going_to_show_location",
        },
        {
            "trigger": "go_back",
            "source": ["preview", "welcome", "select_versions", "movie_intro", "select_cinema", "show_time", "show_location"],
            "dest": "user"
        },

    ],
    initial="user",
    auto_transitions=False,
    show_conditions=True,
)

app = Flask(__name__, static_url_path="")


# get channel_secret and channel_access_token from your environment variable
channel_secret = os.getenv("LINE_CHANNEL_SECRET", None)
channel_access_token = os.getenv("LINE_CHANNEL_ACCESS_TOKEN", None)
if channel_secret is None:
    print("Specify LINE_CHANNEL_SECRET as environment variable.")
    sys.exit(1)
if channel_access_token is None:
    print("Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.")
    sys.exit(1)

line_bot_api = LineBotApi(channel_access_token)
parser = WebhookParser(channel_secret)


@app.route("/callback", methods=["POST"])
def callback():
    signature = request.headers["X-Line-Signature"]
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # parse webhook body
    try:
        events = parser.parse(body, signature)
    except InvalidSignatureError:
        abort(400)

    # if event is MessageEvent and message is TextMessage, then echo text
    for event in events:
        if not isinstance(event, MessageEvent):
            continue
        if not isinstance(event.message, TextMessage):
            continue

        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text=event.message.text)
        )

    return "OK"


@app.route("/webhook", methods=["POST"])
def webhook_handler():
    signature = request.headers["X-Line-Signature"]
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info(f"Request body: {body}")

    # parse webhook body
    try:
        events = parser.parse(body, signature)
    except InvalidSignatureError:
        abort(400)
    response = False
    # if event is MessageEvent and message is TextMessage, then echo text
    for event in events:
        print(type(event))
        if isinstance(event, PostbackEvent):

            if "intro" in event.postback.data:
                ver = True
                response = machine.intro(event)
            elif "#" in event.postback.data:
                ver = True
                response = machine.select_cinema(event)
            elif "detail" in event.postback.data:
                ver = True
                response = machine.search(event)
            else:
                ver = True
                response = machine.show_time(event)
            # print("herewego")
            break
        if not isinstance(event, MessageEvent):
            continue
        if not isinstance(event.message, TextMessage):
            continue
        if not isinstance(event.message.text, str):
            continue
        print(f"\nFSM STATE: {machine.state}")
        print(f"REQUEST BODY: \n{body}")
        if event.message.text == "我要看電影":
            ver = True
            response = machine.want(event)
        elif event.message.text == "影城據點":
            ver = True
            response = machine.where(event)
        else:
            response = machine.advance(event)
        # if machine.state == "state2":
        #response = machine.search(event)

        # if "時刻表" not in event.message.text:
        if ver == True:
            ver = False
            break
        if response == False:
            response = machine.advance(event)

    return "OK"


@app.route("/show-fsms", methods=["GET"])
def show_fsm():
    machine.get_graph().draw("fsm.png", prog="dot", format="png")
    return send_file("fsm.png", mimetype="image/png")


if __name__ == "__main__":
    port = os.environ.get("PORT", 8000)
    app.run(host="0.0.0.0", port=port, debug=True)
