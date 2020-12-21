import requests
import json
import urllib.request as req
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

    def is_going_to_search_table(self, event):
        text = event.message.text
        return "時刻表" in text.lower()

    def is_going_to_movie_intro(self, event):
        print(type(event))
        text = event.message.text
        return "簡介" in text.lower()

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
        url = "https://www.vscinemas.com.tw/vsweb/film/index.aspx"
        request = req.Request(url, headers={
                              "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"})
        with req.urlopen(request) as response:
            data = response.read().decode("utf-8")
        soup = BeautifulSoup(data, 'lxml')
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
                    "body": {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                            {
                                "type": "image",
                                "size": "full",
                                "aspectMode": "cover",
                                "aspectRatio": "2:3",
                                "gravity": "top",
                                "url": content[0]
                            },
                            {
                                "type": "box",
                                "layout": "vertical",
                                "contents": [
                                    {
                                        "type": "box",
                                        "layout": "vertical",
                                        "contents": [
                                            {
                                                "type": "text",
                                                "text": name[0],
                                                "size": "xl",
                                                "color": "#000000",
                                                "weight": "bold"
                                            }
                                        ]
                                    },
                                    {
                                        "type": "box",
                                        "layout": "baseline",
                                        "contents": [
                                            {
                                                "type": "text",
                                                "color": "#000000",
                                                "size": "sm",
                                                "flex": 0,
                                                "text": english[0]
                                            }
                                        ],
                                        "spacing": "lg"
                                    },
                                    {
                                        "type": "box",
                                        "layout": "horizontal",
                                        "contents": [
                                            {
                                                "type": "button",
                                                "action": {
                                                    "type": "message",
                                                    "label": "簡介",
                                                    "text": name[0]+"簡介"
                                                },
                                                "margin": "xs",
                                                "height": "sm",
                                                "style": "primary",
                                                "color": "#ff1493"
                                            },
                                            {
                                                "type": "button",
                                                "action": {
                                                    "type": "message",
                                                    "label": "時刻表",
                                                    "text": name[0]+"時刻表",
                                                },
                                                "height": "sm",
                                                "style": "primary",
                                                "color": "#1e90ff"
                                            }
                                        ],
                                        "borderWidth": "none",
                                        "cornerRadius": "4px",
                                        "spacing": "lg",
                                        "borderColor": "#000000",
                                        "margin": "md"
                                    }
                                ],
                                "position": "absolute",
                                "offsetBottom": "0px",
                                "offsetStart": "0px",
                                "offsetEnd": "0px",
                                "backgroundColor": "#ffffffcc",
                                "paddingAll": "20px",
                                "paddingTop": "18px",
                                "height": "130px"
                            },
                            {
                                "type": "box",
                                "layout": "vertical",
                                "contents": [
                                    {
                                        "type": "text",
                                        "text": "熱映中",
                                        "color": "#ffffff",
                                        "align": "center",
                                        "size": "xs",
                                        "offsetTop": "3px"
                                    }
                                ],
                                "position": "absolute",
                                "cornerRadius": "20px",
                                "offsetTop": "18px",
                                "backgroundColor": "#ff334b",
                                "offsetStart": "18px",
                                "height": "25px",
                                "width": "53px"
                            }
                        ],
                        "paddingAll": "0px"
                    }
                },
                {
                    "type": "bubble",
                    "body": {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                            {
                                "type": "image",
                                "size": "full",
                                "aspectMode": "cover",
                                "aspectRatio": "2:3",
                                "gravity": "top",
                                "url": content[1]
                            },
                            {
                                "type": "box",
                                "layout": "vertical",
                                "contents": [
                                    {
                                        "type": "box",
                                        "layout": "vertical",
                                        "contents": [
                                            {
                                                "type": "text",
                                                "text": name[1],
                                                "size": "xl",
                                                "color": "#000000",
                                                "weight": "bold"
                                            }
                                        ]
                                    },
                                    {
                                        "type": "box",
                                        "layout": "baseline",
                                        "contents": [
                                            {
                                                "type": "text",
                                                "color": "#000000",
                                                "size": "sm",
                                                "flex": 0,
                                                "text": english[1]
                                            }
                                        ],
                                        "spacing": "lg"
                                    },
                                    {
                                        "type": "box",
                                        "layout": "horizontal",
                                        "contents": [
                                            {
                                                "type": "button",
                                                "action": {
                                                    "type": "uri",
                                                    "uri": introduction[1],
                                                    "label": "簡介"
                                                },
                                                "margin": "xs",
                                                "height": "sm",
                                                "style": "primary",
                                                "color": "#ff1493"
                                            },
                                            {
                                                "type": "button",
                                                "action": {
                                                    "type": "message",
                                                    "label": "時刻表",
                                                    "text": name[1]+"時刻表",
                                                },
                                                "height": "sm",
                                                "style": "primary",
                                                "color": "#1e90ff"
                                            }
                                        ],
                                        "borderWidth": "none",
                                        "cornerRadius": "4px",
                                        "spacing": "lg",
                                        "borderColor": "#000000",
                                        "margin": "md"
                                    }
                                ],
                                "position": "absolute",
                                "offsetBottom": "0px",
                                "offsetStart": "0px",
                                "offsetEnd": "0px",
                                "backgroundColor": "#ffffffcc",
                                "paddingAll": "20px",
                                "paddingTop": "18px",
                                "height": "130px"
                            },
                            {
                                "type": "box",
                                "layout": "vertical",
                                "contents": [
                                    {
                                        "type": "text",
                                        "text": "熱映中",
                                        "color": "#ffffff",
                                        "align": "center",
                                        "size": "xs",
                                        "offsetTop": "3px"
                                    }
                                ],
                                "position": "absolute",
                                "cornerRadius": "20px",
                                "offsetTop": "18px",
                                "backgroundColor": "#ff334b",
                                "offsetStart": "18px",
                                "height": "25px",
                                "width": "53px"
                            }
                        ],
                        "paddingAll": "0px"
                    }
                },
                {
                    "type": "bubble",
                    "body": {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                            {
                                "type": "image",
                                "size": "full",
                                "aspectMode": "cover",
                                "aspectRatio": "2:3",
                                "gravity": "top",
                                "url": content[2]
                            },
                            {
                                "type": "box",
                                "layout": "vertical",
                                "contents": [
                                    {
                                        "type": "box",
                                        "layout": "vertical",
                                        "contents": [
                                            {
                                                "type": "text",
                                                "text": name[2],
                                                "size": "xl",
                                                "color": "#000000",
                                                "weight": "bold"
                                            }
                                        ]
                                    },
                                    {
                                        "type": "box",
                                        "layout": "baseline",
                                        "contents": [
                                            {
                                                "type": "text",
                                                "color": "#000000",
                                                "size": "sm",
                                                "flex": 0,
                                                "text": english[2]
                                            }
                                        ],
                                        "spacing": "lg"
                                    },
                                    {
                                        "type": "box",
                                        "layout": "horizontal",
                                        "contents": [
                                            {
                                                "type": "button",
                                                "action": {
                                                    "type": "uri",
                                                    "uri": introduction[2],
                                                    "label": "簡介"
                                                },
                                                "margin": "xs",
                                                "height": "sm",
                                                "style": "primary",
                                                "color": "#ff1493"
                                            },
                                            {
                                                "type": "button",
                                                "action": {
                                                    "type": "message",
                                                    "label": "時刻表",
                                                    "text": name[2]+"時刻表",
                                                },
                                                "height": "sm",
                                                "style": "primary",
                                                "color": "#1e90ff"
                                            }
                                        ],
                                        "borderWidth": "none",
                                        "cornerRadius": "4px",
                                        "spacing": "lg",
                                        "borderColor": "#000000",
                                        "margin": "md"
                                    }
                                ],
                                "position": "absolute",
                                "offsetBottom": "0px",
                                "offsetStart": "0px",
                                "offsetEnd": "0px",
                                "backgroundColor": "#ffffffcc",
                                "paddingAll": "20px",
                                "paddingTop": "18px",
                                "height": "130px"
                            },
                            {
                                "type": "box",
                                "layout": "vertical",
                                "contents": [
                                    {
                                        "type": "text",
                                        "text": "熱映中",
                                        "color": "#ffffff",
                                        "align": "center",
                                        "size": "xs",
                                        "offsetTop": "3px"
                                    }
                                ],
                                "position": "absolute",
                                "cornerRadius": "20px",
                                "offsetTop": "18px",
                                "backgroundColor": "#ff334b",
                                "offsetStart": "18px",
                                "height": "25px",
                                "width": "53px"
                            }
                        ],
                        "paddingAll": "0px"
                    }
                },
                {
                    "type": "bubble",
                    "body": {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                            {
                                "type": "image",
                                "size": "full",
                                "aspectMode": "cover",
                                "aspectRatio": "2:3",
                                "gravity": "top",
                                "url": content[3]
                            },
                            {
                                "type": "box",
                                "layout": "vertical",
                                "contents": [
                                    {
                                        "type": "box",
                                        "layout": "vertical",
                                        "contents": [
                                            {
                                                "type": "text",
                                                "text": name[3],
                                                "size": "xl",
                                                "color": "#000000",
                                                "weight": "bold"
                                            }
                                        ]
                                    },
                                    {
                                        "type": "box",
                                        "layout": "baseline",
                                        "contents": [
                                            {
                                                "type": "text",
                                                "color": "#000000",
                                                "size": "sm",
                                                "flex": 0,
                                                "text": english[3]
                                            }
                                        ],
                                        "spacing": "lg"
                                    },
                                    {
                                        "type": "box",
                                        "layout": "horizontal",
                                        "contents": [
                                            {
                                                "type": "button",
                                                "action": {
                                                    "type": "uri",
                                                    "uri": introduction[3],
                                                    "label": "簡介"
                                                },
                                                "margin": "xs",
                                                "height": "sm",
                                                "style": "primary",
                                                "color": "#ff1493"
                                            },
                                            {
                                                "type": "button",
                                                "action": {
                                                    "type": "message",
                                                    "label": "時刻表",
                                                    "text": name[3]+"時刻表",
                                                },
                                                "height": "sm",
                                                "style": "primary",
                                                "color": "#1e90ff"
                                            }
                                        ],
                                        "borderWidth": "none",
                                        "cornerRadius": "4px",
                                        "spacing": "lg",
                                        "borderColor": "#000000",
                                        "margin": "md"
                                    }
                                ],
                                "position": "absolute",
                                "offsetBottom": "0px",
                                "offsetStart": "0px",
                                "offsetEnd": "0px",
                                "backgroundColor": "#ffffffcc",
                                "paddingAll": "20px",
                                "paddingTop": "18px",
                                "height": "130px"
                            },
                            {
                                "type": "box",
                                "layout": "vertical",
                                "contents": [
                                    {
                                        "type": "text",
                                        "text": "熱映中",
                                        "color": "#ffffff",
                                        "align": "center",
                                        "size": "xs",
                                        "offsetTop": "3px"
                                    }
                                ],
                                "position": "absolute",
                                "cornerRadius": "20px",
                                "offsetTop": "18px",
                                "backgroundColor": "#ff334b",
                                "offsetStart": "18px",
                                "height": "25px",
                                "width": "53px"
                            }
                        ],
                        "paddingAll": "0px"
                    }
                },
                {
                    "type": "bubble",
                    "body": {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                            {
                                "type": "image",
                                "size": "full",
                                "aspectMode": "cover",
                                "aspectRatio": "2:3",
                                "gravity": "top",
                                "url": content[4]
                            },
                            {
                                "type": "box",
                                "layout": "vertical",
                                "contents": [
                                    {
                                        "type": "box",
                                        "layout": "vertical",
                                        "contents": [
                                            {
                                                "type": "text",
                                                "text": name[4],
                                                "size": "xl",
                                                "color": "#000000",
                                                "weight": "bold"
                                            }
                                        ]
                                    },
                                    {
                                        "type": "box",
                                        "layout": "baseline",
                                        "contents": [
                                            {
                                                "type": "text",
                                                "color": "#000000",
                                                "size": "sm",
                                                "flex": 0,
                                                "text": english[4]
                                            }
                                        ],
                                        "spacing": "lg"
                                    },
                                    {
                                        "type": "box",
                                        "layout": "horizontal",
                                        "contents": [
                                            {
                                                "type": "button",
                                                "action": {
                                                    "type": "uri",
                                                    "uri": introduction[4],
                                                    "label": "簡介"
                                                },
                                                "margin": "xs",
                                                "height": "sm",
                                                "style": "primary",
                                                "color": "#ff1493"
                                            },
                                            {
                                                "type": "button",
                                                "action": {
                                                    "type": "message",
                                                    "label": "時刻表",
                                                    "text": name[4]+"時刻表",
                                                },
                                                "height": "sm",
                                                "style": "primary",
                                                "color": "#1e90ff"
                                            }
                                        ],
                                        "borderWidth": "none",
                                        "cornerRadius": "4px",
                                        "spacing": "lg",
                                        "borderColor": "#000000",
                                        "margin": "md"
                                    }
                                ],
                                "position": "absolute",
                                "offsetBottom": "0px",
                                "offsetStart": "0px",
                                "offsetEnd": "0px",
                                "backgroundColor": "#ffffffcc",
                                "paddingAll": "20px",
                                "paddingTop": "18px",
                                "height": "130px"
                            },
                            {
                                "type": "box",
                                "layout": "vertical",
                                "contents": [
                                    {
                                        "type": "text",
                                        "text": "熱映中",
                                        "color": "#ffffff",
                                        "align": "center",
                                        "size": "xs",
                                        "offsetTop": "3px"
                                    }
                                ],
                                "position": "absolute",
                                "cornerRadius": "20px",
                                "offsetTop": "18px",
                                "backgroundColor": "#ff334b",
                                "offsetStart": "18px",
                                "height": "25px",
                                "width": "53px"
                            }
                        ],
                        "paddingAll": "0px"
                    }
                }

            ]
        }
        s1 = json.dumps(bubble_string)
        s2 = json.loads(s1)

        send_flex_message(reply_token, "hello", s2)
        # self.go_back()

    """def on_exit_state2(self):
        print("Leaving state2")"""

    def on_enter_state3(self, event):
        print("I'm entering state3")

        reply_token = event.reply_token
        send_text_message(reply_token, "goto state3")
        self.go_back()

    def on_exit_state3(self):
        print("Leaving state3")

    def on_enter_search_table(self, event):
        print("I'm entering search table")

        reply_token = event.reply_token
        send_text_message(reply_token, "goto search table")
        self.go_back()

    def on_exit_search_table(self):
        print("Leaving search table")

    def on_enter_movie_intro(self, event):
        print("I'm entering movie intro")

        reply_token = event.reply_token
        url = "https://www.vscinemas.com.tw/vsweb/film/detail.aspx?id=4918"
        request = req.Request(url, headers={
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"})
        with req.urlopen(request) as response:
            data = response.read().decode("utf-8")
        soup = BeautifulSoup(data, 'lxml')
        st = ""
        for i, data in enumerate(soup.select('div.bbsArticle p')):
            st += data.text
            st += "\n"
            print(data.text)
        send_text_message(reply_token, st)
        self.go_back()
