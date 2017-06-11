from Quantumer import Quantumer




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

quantumer = Quantumer()
det=quantumer.new_detector()
det.extract_function = get
det.function_after_trigger = do2
det.judging_function = judge
det.judging_need_old = True
det.start_listening(url2, 2)
