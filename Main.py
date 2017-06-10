import requests
import Detector
import os
import re
import urllib
import queue

url = "https://bbs.meizu.cn/home.php?mod=space&uid=3088580&do=thread&from=space"
url2 = "https://bbs.meizu.cn/thread-6616106-1-1.html"
con = requests.get(url).text


def cut_string(input_str, head, tail):
    if isinstance(
        head,
        str) and isinstance(
            tail,
            str) and isinstance(
            input_str,
            str):
        start = input_str.find(head) + len(head)
        end = input_str.find(tail, start)

        rt_str = ""
        for index in range(start, end):
            rt_str += input_str[index]
        return rt_str
    else:
        raise TypeError("Inputs are not string!")


def get(content):

    head = "replyicon_uinfo"
    tail = "readicon_uinfo"

    head2 = "=\"xi1\">"
    tail2 = "<"

    ret_str = cut_string(content, head, tail)
    ret_str = cut_string(ret_str, head2, tail2)

    return ret_str


def do(content):

    def send_message():
        path_file = open("path.cfg", mode="r")
        path = path_file.read()
        path_file.close()
        abs_path = path + r"\aliyun\send.exe"
        abs_path = "start " + abs_path
        os.system(abs_path)

    send_message()


def do2(content):
    print(content)


def judge(new, old):
    if int(new) - int(old) >= 5:
        print("OK!_______________________________")
        return True
    else:
        return False


detector = Detector.Detector(url2, 2)
detector.extract_function = get
detector.function_after_trigger = do2
detector.judging_function = judge
detector.judging_need_old = True
detector.start()
