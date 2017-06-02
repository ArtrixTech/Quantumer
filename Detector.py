import requests
import re
import threading
import time
import urllib
import queue


class Detector:

    def __init__(self, input_url, interval=20):
        # Unit of interval: Second.
        # Ensure the url has a correct syntax
        if "http://" in input_url or "https://" in input_url:
            self.__url = input_url
        else:
            self.__url = "http://" + input_url
        self.__inited = True
        self.__interval = interval
        self.__count = 0

    def start(
            self,
            extract_function,
            function_to_act_if_changed,
            function_args=False):

        thread = threading.Thread(
            target=self.loop_thread,
            name="thread1",
            args=(
                extract_function,
                function_to_act_if_changed,
                function_args,
            ))
        thread.start()
        print("Detect Thread started.")

    def loop_thread(self, extract_function, function, args=False):

        def check(old,init=False):
            if not init:
                content = requests.get(self.__url).text
                now = extract_function(content)
                print("Now the %s check." % str(self.__count + 1))
                self.__count += 1

                if not old == now:
                    if not args:
                        function(now)
                    else:
                        function(now,args)
                    return now
                print("No change.Now result:%s" % now)
                return now
            else:
                # Execute the init check
                content = requests.get(self.__url).text
                now = extract_function(content)
                print("Now the %s check." % str(self.__count + 1))
                self.__count += 1
                print("Now result:%s" % now)
                return now

        if self.__inited:
            old_stamp = time.time()
            old_content = check("Nothing",True)
            while True:
                if time.time() - old_stamp >= self.__interval:
                    old_stamp = time.time()
                    old_content = check(old_content)
                time.sleep(1)
