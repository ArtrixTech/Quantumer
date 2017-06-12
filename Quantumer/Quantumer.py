from Quantumer.Detector_Class import Detector
import itchat
import threading
import requests
from itchat.content import *

detector_pool = dict()


class ExtractFunction:

    @staticmethod
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

    @staticmethod
    def one(kw):

        ret_str = ExtractFunction.cut_string(
            kw["content"], kw["head"], kw["tail"])

        return ret_str

    @staticmethod
    def two(kw):

        ret_str = ExtractFunction.cut_string(
            kw["content"], kw["head"], kw["tail"])
        ret_str = ExtractFunction.cut_string(ret_str, kw["head2"], kw["tail2"])

        return ret_str


def new_detector(username):
    det = Detector()
    detector_pool[username] = det
    return det


def do(username, new_val):
    itchat.send("changed!NewVal:" + new_val, username)


def first_result_show(username, content):
    itchat.send(content, username)


class Generator:

    step = 0
    url = ""
    interval = ""
    content = ""
    head = ""
    tail = ""
    is_guide = False

    def generate(self):
        html = requests.get(self.url).text

        is_finished = False
        char = 50
        while not is_finished:
            start_place = html.find(self.content) - char
            self.head = html[start_place:start_place + char]

            start_place = html.find(self.content) + len(self.content)
            self.tail = html[start_place:start_place + 1]

            command = "开始监听 url=%s,head1=%s,tail1=%s,interval=%s," % (
                self.url, self.head, self.tail, self.interval)
            if "\n" in command:
                if not char == 0:
                    char -= 1
                else:
                    print("Generate Failed!")
            else:
                is_finished = True
        return "开始监听 url=%s,head1=%s,tail1=%s,interval=%s," % (
            self.url, self.head, self.tail, self.interval)

g = Generator()


@itchat.msg_register(TEXT)
def simple_reply(msg):

    user_name = msg['FromUserName']
    if g.is_guide:
        if g.step == 0:
            g.url = str(msg['Text'])
            g.step = 1
            return "输入每次刷新时间（秒），建议10秒"
        if g.step == 1:
            g.interval = str(msg['Text'])
            g.step = 2
            return "输入要抓取的内容"
        if g.step == 2:
            g.content = str(msg['Text'])
            g.is_guide = False
            g.step = 0
            itchat.send("复制以下内容，发送至本账号即可开始监听:", user_name)
            return g.generate()

    if msg['Type'] == 'Text':
        text = str(msg['Text'])
        if "开始监听" in text:

            command = text.replace("开始监听,", "")
            print("User:" + user_name + "开始新任务")
            exist = False
            try:
                assert isinstance(detector_pool[user_name], Detector)
                exist = True
            except TypeError:
                pass
            except KeyError:
                pass

            if exist:
                itchat.send("开始新任务！旧任务已停止", user_name)
                old_det = detector_pool[user_name]
                assert isinstance(old_det, Detector)
                old_det.stop = True
            else:
                itchat.send("开始新任务", user_name)
            det = new_detector(user_name)

            # Get arguments from the WeChat commands.
            url = ExtractFunction.cut_string(command, "url=", ",")
            head = ExtractFunction.cut_string(command, "head1=", ",")
            tail = ExtractFunction.cut_string(command, "tail1=", ",")
            interval = ExtractFunction.cut_string(command, "interval=", ",")

            if "head2" in command and "tail2" in command:
                head2 = ExtractFunction.cut_string(command, "head2=", ",")
                tail2 = ExtractFunction.cut_string(command, "tail2=", ",")
                det.extract_function = ExtractFunction.two
                det.extract_function_args = {
                    "head": head, "tail": tail, "head2": head2, "tail2": tail2}
            else:
                det.extract_function = ExtractFunction.one
                det.extract_function_args = {"head": head, "tail": tail}

            def send_task_message():
                itchat.send("任务信息：", user_name)
                itchat.send("url：", url)
                itchat.send("间隔Interval：", interval)

            send_task_message()
            det.username = user_name
            det.function_after_trigger = do
            det.start_listening(url, interval)

            return

        elif "停止监听" in text:

            user_name = msg['FromUserName']
            exist = False
            try:
                assert isinstance(detector_pool[user_name], Detector)
                exist = True
            except TypeError:
                pass
            except KeyError:
                pass

            if exist:
                old_det = detector_pool[user_name]
                assert isinstance(old_det, Detector)
                old_det.stop = True
                detector_pool[user_name] = False
            return "任务停止"

        elif "生成命令" in text:
            g.is_guide = True
            return "输入url"
        else:
            return "命令有误，请重新输入"


@itchat.msg_register(FRIENDS)
def add_friend(msg):
    itchat.add_friend(**msg['Text'])  # 该操作会自动将新好友的消息录入，不需要重载通讯录
    itchat.send_msg(
        '你好！请输入“生成命令”来开始一个新的任务。Hello!Please enter "生成命令" to start a new task!',
        msg['RecommendInfo']['UserName'])

itchat.auto_login(hotReload=True, enableCmdQR=1)


def start():
    thread = threading.Thread(
        target=itchat.run,
        name="thread1", )
    thread.start()
