from Quantumer.Detector_Class import Detector
import itchat
import threading
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


@itchat.msg_register(TEXT)
def simple_reply(msg):
    if msg['Type'] == 'Text':
        text = str(msg['Text'])
        if "开始监听" in text:

            command = text.replace("开始监听,", "")
            user_name = msg['FromUserName']
            print("User:" + user_name + "开始新任务")
            exist=False
            try:
                assert isinstance(detector_pool[user_name], Detector)
                exist=True
            except:pass

            if exist:
                itchat.send("开始新任务！旧任务已停止",user_name)
                old_det = detector_pool[user_name]
                assert isinstance(old_det, Detector)
                old_det.stop = True
            det = new_detector(user_name)

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
            except:pass

            if exist:
                old_det = detector_pool[user_name]
                assert isinstance(old_det, Detector)
                old_det.stop = True
            return "任务停止"

        else:
            return "命令有误，请重新输入"


@itchat.msg_register(FRIENDS)
def add_friend(msg):
    itchat.add_friend(**msg['Text'])  # 该操作会自动将新好友的消息录入，不需要重载通讯录
    itchat.send_msg(
        '你好！信息格式：开始监听,url=%your_url%,head1=%your_url%,tail1=%your_url%,head2=%your_url%,tail2=%your_url%,interval=%second%',
        msg['RecommendInfo']['UserName'])

itchat.auto_login(hotReload=True, enableCmdQR=1)


def start():
    thread = threading.Thread(
        target=itchat.run,
        name="thread1", )
    thread.start()
