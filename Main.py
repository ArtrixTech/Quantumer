import requests
import Detector
import os
import re
import urllib
import queue

url = "https://bbs.meizu.cn/home.php?mod=space&uid=3088580&do=thread&from=space"
con = requests.get(url).text


def get(content):

    head = "<th class=\"scontent\">\n<a href=\""
    tail = "/a>"

    head2 = "target=\"_blank\" >"
    tail2 = "<"

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

detector = Detector.Detector(url)

detector.start(get, do)
