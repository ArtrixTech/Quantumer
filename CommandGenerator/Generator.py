import requests


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

print("Input the Url(With out the http or https):")
url = "http://" + input()

print("Input the content to Grab:")
content = input()

print("Input the interval:")
interval = input()

html = requests.get(url).text

is_finished = False
char = 50
head,tail="",""
while not is_finished:
    start_place = html.find(content) - char
    head = html[start_place:start_place + char]

    start_place = html.find(content) + len(content)
    tail = html[start_place:start_place + 1]

    command = "开始监听 url=%s,head1=%s,tail1=%s,interval=%s," % (
        url, head, tail, interval)
    if "\n" in command:
        if not char == 0:
            char -= 1
        else:
            print("Generate Failed!")
    else:
        is_finished = True

print(head)
print(tail)
print(cut_string(html, head, tail))
if cut_string(html, head, tail) == content:
    print("----------------------------------------------------------------------------------------------")
    print("Grab Result:"+cut_string(html, head, tail))
    print("Generated Command:")
    print("")
    print(
        "开始监听 url=%s,head1=%s,tail1=%s,interval=%s," %
        (url, head, tail, interval))
    print("-----------Just copy it into your WeChat dialog and send to the WeChar bot account.-----------")
