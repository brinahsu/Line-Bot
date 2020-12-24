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
        # text = event.message.text
        return True

    def is_going_to_movie_intro(self, event):
        text = event.message.text
        return "簡介" in text.lower()

    def is_going_to_select_cinema(self, event):
        # text = event.message.text
        return True

    def is_going_to_show_time(self, event):
        # text = event.message.text
        return True

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
            introduction.append(data['href'])
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
                                                    "type": "postback",
                                                    "label": "時刻表",
                                                    "text": name[0]+"時刻表",
                                                    "data": introduction[0]
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
                                                    "type": "message",
                                                    "label": "簡介",
                                                    "text": name[1]+"簡介"
                                                },
                                                "margin": "xs",
                                                "height": "sm",
                                                "style": "primary",
                                                "color": "#ff1493"
                                            },
                                            {
                                                "type": "button",
                                                "action": {
                                                    "type": "postback",
                                                    "label": "時刻表",
                                                    "text": name[1]+"時刻表",
                                                    "data": introduction[1]
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
                                                    "type": "message",
                                                    "label": "簡介",
                                                    "text": name[2]+"簡介"
                                                },
                                                "margin": "xs",
                                                "height": "sm",
                                                "style": "primary",
                                                "color": "#ff1493"
                                            },
                                            {
                                                "type": "button",
                                                "action": {
                                                    "type": "postback",
                                                    "label": "時刻表",
                                                    "text": name[2]+"時刻表",
                                                    "data": introduction[2]
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
                                                    "type": "message",
                                                    "label": "簡介",
                                                    "text": name[3]+"簡介"
                                                },
                                                "margin": "xs",
                                                "height": "sm",
                                                "style": "primary",
                                                "color": "#ff1493"
                                            },
                                            {
                                                "type": "button",
                                                "action": {
                                                    "type": "postback",
                                                    "label": "時刻表",
                                                    "text": name[3]+"時刻表",
                                                    "data": introduction[3]
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
                                                    "type": "message",
                                                    "label": "簡介",
                                                    "text": name[4]+"簡介"
                                                },
                                                "margin": "xs",
                                                "height": "sm",
                                                "style": "primary",
                                                "color": "#ff1493"
                                            },
                                            {
                                                "type": "button",
                                                "action": {
                                                    "type": "postback",
                                                    "label": "時刻表",
                                                    "text": name[4]+"時刻表",
                                                    "data": introduction[4]
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
        r = requests.get(
            "https://www.vscinemas.com.tw/vsweb/film/"+event.postback.data)
        r.encoding = 'utf-8'
        soup = BeautifulSoup(r.text, 'lxml')
        content = []
        net = []
        action = []
        column = []
        place = []
        ref = []
        pic = [
            "https://images.unsplash.com/photo-1536440136628-849c177e76a1?ixid=MXwxMjA3fDB8MHxzZWFyY2h8M3x8bW92aWV8ZW58MHx8MHw%3D&ixlib=rb-1.2.1&auto=format&fit=crop&w=1100&q=60",
            "https://images.unsplash.com/photo-1535016120720-40c646be5580?ixid=MXwxMjA3fDB8MHxzZWFyY2h8Nnx8bW92aWV8ZW58MHx8MHw%3D&ixlib=rb-1.2.1&auto=format&fit=crop&w=1100&q=60",
            "https://images.unsplash.com/photo-1517604931442-7e0c8ed2963c?ixid=MXwxMjA3fDB8MHxzZWFyY2h8MTV8fG1vdmllfGVufDB8fDB8&ixlib=rb-1.2.1&auto=format&fit=crop&w=1100&q=60",
            "https://images.unsplash.com/photo-1533488765986-dfa2a9939acd?ixid=MXwxMjA3fDB8MHxzZWFyY2h8MjR8fG1vdmllfGVufDB8fDB8&ixlib=rb-1.2.1&auto=format&fit=crop&w=1100&q=60"
        ]
        index = 0
        for i, data in enumerate(soup.select('ul.versionList ul')):
            place.append(data.text)
        for i, data in enumerate(soup.select('ul.versionList li ul li p a')):
            ref.append(data['href'])
        k = 0
        con = []
        datas = soup.find_all("a", class_="versionFirst")
        for data in datas:
            # print(title.text)
            pack = ""
            content.append(data.text)
            places = place[index].split('\n')
            for i in places:
                if i == "":
                    continue
                pack += (i+ref[k][0]+ref[k][10:]+"\n")
                k = k+1
            print(pack)
            print(len(pack))
            net.append(data['href'])
            action.append(
                {
                    "type": "button",
                    "action": {
                        "type": "postback",
                        "label": data.text,
                        "text": data.text,
                        "data": pack+event.postback.data[-4:]  # 影城+movie id
                    },
                    "color": "#ffffff",
                    "style": "secondary"
                }
            )
            index = index+1
        a = 0
        for i, data in enumerate(action):
            if i % 3 == 0:

                if (i+3) > len(action):
                    end = len(action)
                else:
                    end = i+3
                con.append(
                    {
                        "type": "bubble",
                        "header": {
                            "type": "box",
                            "layout": "vertical",
                            "contents": [
                                {
                                    "type": "box",
                                    "layout": "vertical",
                                    "contents": [
                                        {
                                            "type": "image",
                                            "url": pic[a],
                                            "size": "full",
                                            "aspectMode": "fit",
                                            "aspectRatio": "150:100",
                                            "gravity": "center",
                                            "flex": 1
                                        }
                                    ]
                                }
                            ],
                            "paddingAll": "0px"
                        },
                        "body": {
                            "type": "box",
                            "layout": "vertical",
                            "contents": [
                                {
                                    "type": "box",
                                    "layout": "vertical",
                                    "contents": [
                                        {
                                            "type": "text",
                                            "contents": [],
                                            "size": "xl",
                                            "text": "請選擇影廳",
                                            "color": "#ffffff",
                                            "weight": "bold",
                                            "gravity": "top"
                                        },
                                        {
                                            "type": "box",
                                            "layout": "baseline",
                                            "contents": [],
                                            "margin": "xl"
                                        },
                                        {
                                            "type": "box",
                                            "layout": "vertical",
                                            "contents": action[i:end],
                                            "spacing": "sm"
                                        }
                                    ]
                                }
                            ],
                            "paddingAll": "20px",
                            "backgroundColor": "#611529"
                        }
                    }
                )
                a = a+1
        bubble_string = {
            "type": "carousel",
            "contents": con
        }
        s1 = json.dumps(bubble_string)
        s2 = json.loads(s1)
        send_flex_message(reply_token, "hello", s2)
        # self.go_back()

    """def on_exit_search_table(self):
        print("Leaving search table")"""

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
            st += "\n\n"
        send_text_message(reply_token, st)
        self.go_back()

    def on_enter_select_cinema(self, event):
        print("I'm entering select cinema")
        reply_token = event.reply_token
        action = []
        datas = []
        content = []
        pic = [
            "https://images.unsplash.com/photo-1489599849927-2ee91cede3ba?ixid=MXwxMjA3fDB8MHxzZWFyY2h8Mnx8Y2luZW1hfGVufDB8fDB8&ixlib=rb-1.2.1&auto=format&fit=crop&w=1100&q=60",
            "https://images.unsplash.com/photo-1585331505473-7586f9cb0854?ixid=MXwxMjA3fDB8MHxzZWFyY2h8MTZ8fGNpbmVtYXxlbnwwfHwwfA%3D%3D&ixlib=rb-1.2.1&auto=format&fit=crop&w=1100&q=60",
            "https://images.unsplash.com/photo-1440404653325-ab127d49abc1?ixid=MXwxMjA3fDB8MHxzZWFyY2h8MTB8fG1vdmllfGVufDB8fDB8&ixlib=rb-1.2.1&auto=format&fit=crop&w=1100&q=60",
            "https://images.unsplash.com/photo-1460881680858-30d872d5b530?ixid=MXwxMjA3fDB8MHxzZWFyY2h8MTd8fG1vdmllfGVufDB8fDB8&ixlib=rb-1.2.1&auto=format&fit=crop&w=1100&q=60",
            "https://images.unsplash.com/photo-1585647347483-22b66260dfff?ixid=MXwxMjA3fDB8MHxzZWFyY2h8M3x8cG9wY29ybnxlbnwwfHwwfA%3D%3D&ixlib=rb-1.2.1&auto=format&fit=crop&w=1100&q=60",
            "https://images.unsplash.com/photo-1485846234645-a62644f84728?ixid=MXwxMjA3fDB8MHxzZWFyY2h8MXx8ZmlsbXxlbnwwfHwwfA%3D%3D&ixlib=rb-1.2.1&auto=format&fit=crop&w=1100&q=60"
        ]
        datas = event.postback.data.split("\n")
        for data in datas[:-1]:
            if data == "":
                continue
            ref = []
            ref = data.split('#')
            action.append(
                {
                    "type": "button",
                    "action": {
                        "type": "postback",
                        "label": ref[0],
                        "text": ref[0],
                        "data": ref[1]+datas[-1]  # movieTime+movie id
                    },
                    "color": "#ffffff",
                    "style": "secondary"
                }
            )
        k = 0
        for i, data in enumerate(action):
            if i % 3 == 0:

                if (i+3) > len(action):
                    end = len(action)
                else:
                    end = i+3
                content.append(
                    {
                        "type": "bubble",
                        "header": {
                            "type": "box",
                            "layout": "vertical",
                            "contents": [
                                {
                                    "type": "box",
                                    "layout": "vertical",
                                    "contents": [
                                        {
                                            "type": "image",
                                            "url": pic[k],
                                            "size": "full",
                                            "aspectMode": "fit",
                                            "aspectRatio": "150:100",
                                            "gravity": "center",
                                            "flex": 1
                                        }
                                    ]
                                }
                            ],
                            "paddingAll": "0px"
                        },
                        "body": {
                            "type": "box",
                            "layout": "vertical",
                            "contents": [
                                {
                                    "type": "box",
                                    "layout": "vertical",
                                    "contents": [
                                        {
                                            "type": "text",
                                            "contents": [],
                                            "size": "xl",
                                            "text": "請選擇影廳",
                                            "color": "#ffffff",
                                            "weight": "bold",
                                            "gravity": "top"
                                        },
                                        {
                                            "type": "box",
                                            "layout": "baseline",
                                            "contents": [],
                                            "margin": "xl"
                                        },
                                        {
                                            "type": "box",
                                            "layout": "vertical",
                                            "contents": action[i:end],
                                            "spacing": "sm"
                                        }
                                    ]
                                }
                            ],
                            "paddingAll": "20px",
                            "backgroundColor": "#611529"
                        }
                    }
                )
                k = k+1
        bubble_string = {
            "type": "carousel",
            "contents": content
        }
        s1 = json.dumps(bubble_string)
        s2 = json.loads(s1)
        send_flex_message(reply_token, "hello", s2)

    def on_enter_show_time(self, event):
        print("I'm entering show time")

        reply_token = event.reply_token
        index = "movieTime"+event.postback.data[:-4]
        url = "https://www.vscinemas.com.tw/vsweb/film/detail.aspx?id=" + \
            event.postback.data[-4:]
        request = req.Request(url, headers={
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"})
        with req.urlopen(request) as response:
            data = response.read().decode("utf-8")
        soup = BeautifulSoup(data, 'lxml')
        content = []
        time = []
        st = ""
        sti = ""
        print(index)
        print(url)
        datas = soup.find("article", id=index)
        data = datas.find_all("h4")
        for i in data:
            st = i.text[7:].replace(" 月 ", "/")
            st = st.replace(" 日", "")
            content.append(st)
        batas = datas.findAll("ul", "bookList")
        for bata in batas:
            time.append(bata.text)
        for i, item in enumerate(data):
            sti = sti+"🍿"+content[i]+"\n     " + \
                time[i].replace("\n", " ")+"\n\n"
        send_text_message(reply_token, "放映時間如下\n\n"+sti)
