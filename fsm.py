import requests
import json
from bs4 import BeautifulSoup
from transitions.extensions import GraphMachine

from utils import send_text_message, send_sticker_message, send_flex_message


class TocMachine(GraphMachine):
    def __init__(self, **machine_configs):
        self.machine = GraphMachine(model=self, **machine_configs)

    def is_going_to_state1(self, event):
        text = event.message.text
        return text.lower() == "go to state1"

    def is_going_to_state2(self, event):
        text = event.message.text
        return text.lower() == "go to state2"

    def is_going_to_state3(self, event):
        text = event.message.text
        return text.lower() == "state3"

    def on_enter_state1(self, event):
        print("I'm entering state1")

        reply_token = event.reply_token
        send_sticker_message(reply_token, "1", "2")
        self.go_back()

    def on_exit_state1(self):
        print("Leaving state1")

    def on_enter_state2(self, event):
        print("I'm entering state2")

        reply_token = event.reply_token

        r = requests.get('https://www.vscinemas.com.tw/vsweb/film/index.aspx')
        r.encoding = 'utf-8'
        soup = BeautifulSoup(r.text, 'lxml')
        content = []
        column = []
        name = []
        english = []
        introduction = []
        for i, data in enumerate(soup.select('ul.movieList figure a')):
            if i > 4:
                break
            introduction.append(
                "https://www.vscinemas.com.tw/vsweb/film/"+data['href'])
        for i, data in enumerate(soup.select('ul.movieList figure a img')):
            if i > 4:
                break
            content.append(
                "https://www.vscinemas.com.tw/vsweb" + data['src'][2:])
        for i, data in enumerate(soup.select('section.infoArea a')):
            if i > 4:
                break
            name.append(data.text)
        for i, data in enumerate(soup.select('section.infoArea h3')):
            if i > 4:
                break
            english.append(data.text)

        bubble_string = {
            "type": "carousel",
            "contents": [
                {
                    "type": "bubble",
                    "hero": {
                        "type": "box",
                        "layout": "horizontal",
                        "contents": [
                            {
                                "type": "image",
                                "url": content[0],
                                "size": "full",
                                "aspectRatio": "21:30",
                                "aspectMode": "fit"
                            }
                        ]
                    },
                    "footer": {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                            {
                                "type": "button",
                                "action": {
                                    "type": "uri",
                                    "label": "電影簡介",
                                    "uri": introduction[0]
                                },
                                "color": "#ff005e",
                                "style": "link"
                            },
                            {
                                "type": "button",
                                "action": {
                                    "type": "postback",
                                    "label": "電影時刻表",
                                    "text": name[0]+"時刻表",
                                    "data": introduction[0]
                                },
                                "style": "link"
                            }
                        ],
                        "backgroundColor": "#ffffffe0",
                        "borderColor": "#ffffffe0"
                    }
                },
                {
                    "type": "bubble",
                    "hero": {
                        "type": "box",
                        "layout": "horizontal",
                        "contents": [
                            {
                                "type": "image",
                                "url": content[1],
                                "size": "full",
                                "aspectRatio": "21:30",
                                "aspectMode": "fit"
                            }
                        ]
                    },
                    "footer": {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                            {
                                "type": "button",
                                "action": {
                                    "type": "uri",
                                    "label": "電影簡介",
                                    "uri": introduction[1]
                                },
                                "color": "#ff005e",
                                "style": "link"
                            },
                            {
                                "type": "button",
                                "action": {
                                    "type": "postback",
                                    "label": "電影時刻表",
                                    "text": name[1]+"時刻表",
                                    "data": introduction[1]
                                },
                                "style": "link"
                            }
                        ],
                        "backgroundColor": "#ffffffe0",
                        "borderColor": "#ffffffe0"
                    }
                },
                {
                    "type": "bubble",
                    "hero": {
                        "type": "box",
                        "layout": "horizontal",
                        "contents": [
                            {
                                "type": "image",
                                "url": content[2],
                                "size": "full",
                                "aspectRatio": "21:30",
                                "aspectMode": "fit"
                            }
                        ]
                    },
                    "footer": {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                            {
                                "type": "button",
                                "action": {
                                    "type": "uri",
                                    "label": "電影簡介",
                                    "uri": introduction[2]
                                },
                                "color": "#ff005e",
                                "style": "link"
                            },
                            {
                                "type": "button",
                                "action": {
                                    "type": "postback",
                                    "label": "電影時刻表",
                                    "text": name[2]+"時刻表",
                                    "data": introduction[2]
                                },
                                "style": "link"
                            }
                        ],
                        "backgroundColor": "#ffffffe0",
                        "borderColor": "#ffffffe0"
                    }
                },
                {
                    "type": "bubble",
                    "hero": {
                        "type": "box",
                        "layout": "horizontal",
                        "contents": [
                            {
                                "type": "image",
                                "url": content[3],
                                "size": "full",
                                "aspectRatio": "21:30",
                                "aspectMode": "fit"
                            }
                        ]
                    },
                    "footer": {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                            {
                                "type": "button",
                                "action": {
                                    "type": "uri",
                                    "label": "電影簡介",
                                    "uri": introduction[3]
                                },
                                "color": "#ff005e",
                                "style": "link"
                            },
                            {
                                "type": "button",
                                "action": {
                                    "type": "postback",
                                    "label": "電影時刻表",
                                    "text": name[3]+"時刻表",
                                    "data": introduction[3]
                                },
                                "style": "link"
                            }
                        ],
                        "backgroundColor": "#ffffffe0",
                        "borderColor": "#ffffffe0"
                    }
                },
                {
                    "type": "bubble",
                    "hero": {
                        "type": "box",
                        "layout": "horizontal",
                        "contents": [
                            {
                                "type": "image",
                                "url": content[4],
                                "size": "full",
                                "aspectRatio": "21:30",
                                "aspectMode": "fit"
                            }
                        ]
                    },
                    "footer": {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                            {
                                "type": "button",
                                "action": {
                                    "type": "uri",
                                    "label": "電影簡介",
                                    "uri": introduction[4]
                                },
                                "color": "#ff005e",
                                "style": "link"
                            },
                            {
                                "type": "button",
                                "action": {
                                    "type": "postback",
                                    "label": "電影時刻表",
                                    "text": name[4]+"時刻表",
                                    "data": introduction[4]
                                },
                                "style": "link"
                            }
                        ],
                        "backgroundColor": "#ffffffe0",
                        "borderColor": "#ffffffe0"
                    }
                }
            ]
        }
        s1 = json.dumps(bubble_string)
        s2 = json.loads(s1)

        send_flex_message(reply_token, "hello", s2)
        self.go_back()

    def on_exit_state2(self):
        print("Leaving state2")

    def on_enter_state3(self, event):
        print("I'm entering state3")

        reply_token = event.reply_token
        send_text_message(reply_token, "goto state3")
        self.go_back()

    def on_exit_state3(self):
        print("Leaving state3")
