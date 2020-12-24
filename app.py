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
    states=["user", "state1", "state2",
            "state3", "search_table", "movie_intro", "select_cinema", "show_time"],
    transitions=[
        {
            "trigger": "advance",
            "source": "user",
            "dest": "state1",
            "conditions": "is_going_to_state1",
        },
        {
            "trigger": "advance",
            "source": "user",
            "dest": "state2",
            "conditions": "is_going_to_state2",
        },
        {
            "trigger": "advance",
            "source": "user",
            "dest": "state3",
            "conditions": "is_going_to_state3",
        },
        {
            "trigger": "intro",
            "source": ["user", "state1", "state2", "state3", "search_table", "select_cinema"],
            "dest": "movie_intro",
            "conditions": "is_going_to_movie_intro",
        },
        {
            "trigger": "search",
            "source": ["user", "state1", "state2", "state3", "movie_intro", "select_cinema"],
            "dest": "search_table",
            "conditions": "is_going_to_search_table",
        },
        {
            "trigger": "select_cinema",
            "source": ["search_table"],
            "dest": "select_cinema",
            "conditions": "is_going_to_select_cinema",
        },
        {
            "trigger": "time",
            "source": ["select_ciema"],
            "dest": "show_time",
            "conditions": "is_going_to_show_time",
        },
        {
            "trigger": "go_back",
            "source": ["state1", "state2", "state3", "search_table", "movie_intro", "select_cinema", "show_time"],
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

    # if event is MessageEvent and message is TextMessage, then echo text
    for event in events:
        print(type(event))
        if isinstance(event, PostbackEvent):
            if "detail" in event.postback.data:
                response = machine.search(event)
            elif "#" in event.postback.data:
                response = machine.select_cinema(event)
            else:
                response = machine.time(event)
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
        if machine.state == "user":
            response = machine.advance(event)
        # if machine.state == "state2":
        #response = machine.search(event)
        response = machine.intro(event)
        # if "時刻表" not in event.message.text:

    # if response == False:
    #    send_text_message(event.reply_token, "Not Entering any State")

    return "OK"


@app.route("/show-fsm", methods=["GET"])
def show_fsm():
    machine.get_graph().draw("fsm.png", prog="dot", format="png")
    return send_file("fsm.png", mimetype="image/png")


if __name__ == "__main__":
    port = os.environ.get("PORT", 8000)
    app.run(host="0.0.0.0", port=port, debug=True)
