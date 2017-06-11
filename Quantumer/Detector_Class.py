import requests
import re
import threading
import time
from types import FunctionType
import urllib
import queue


class Detector:

    __init = False
    __function_after_trigger = False
    __extract_function = False
    __judging_function = False
    username = False
    extract_function_args = False
    stop = False

    @property
    def function_after_trigger(self):
        return self.__function_after_trigger

    @function_after_trigger.setter
    def function_after_trigger(self, value):
        assert isinstance(value, FunctionType)
        self.__function_after_trigger = value

        # check if is all the required function bound.
        if self.extract_function:
            self.__init = True

    @property
    def extract_function(self):
        return self.__extract_function

    @extract_function.setter
    def extract_function(self, value):
        assert isinstance(value, FunctionType)
        self.__extract_function = value

        # check if is all the required function bound.
        if self.function_after_trigger:
            self.__init = True

    @property
    def judging_function(self):
        return self.__judging_function

    @judging_function.setter
    def judging_function(self, value):
        assert isinstance(value, FunctionType)
        self.__init = True
        self.__judging_function = value

    # def __init__(self, input_url, interval=20):

    def start_listening(self, input_url, interval=20):

        # Unit of interval: Second.
        # Ensure the url has a correct syntax
        if "http://" in input_url or "https://" in input_url:
            self.__url = input_url
        else:
            self.__url = "http://" + input_url
        self.__interval = interval
        self.__count = 0
        self.trigger_need_old = False
        self.judging_need_old = False
        self.__old_change = ""

        assert self.__init
        thread = threading.Thread(
            target=self.loop_thread,
            name="thread1",)
        thread.start()
        print("Detect Thread started.")

    def loop_thread(self):

        def check(old, init=False):
            if not init:

                content = requests.get(self.__url).text
                self.extract_function_args["content"] = content
                now = self.extract_function(self.extract_function_args)
                print("Now the %s check." % str(self.__count + 1))
                self.__count += 1

                # trigger the function
                def trigger():

                    print("Triggered.New Val:" + now)
                    if self.trigger_need_old:
                        # if it is the first change:
                        if self.__old_change:
                            self.function_after_trigger(
                                self.username, now, self.__old_change)
                        else:
                            self.function_after_trigger(
                                self.username, now, now)
                    else:
                        self.function_after_trigger(self.username, now)

                    self.__old_change = now

                # if need the judge function
                if self.judging_function:
                    if self.judging_need_old:
                        if self.__old_change:
                            if self.judging_function(now, self.__old_change):
                                trigger()
                                return now
                        else:
                            if self.judging_function(now, now):
                                trigger()
                                return now
                    else:
                        if self.judging_function(now):
                            trigger()
                            return now
                    print("No change.Now result:%s" % now)
                    return now

                # if the judge function has not been required
                elif not old == now:
                    trigger()
                    return now
                print("No change.Now result:%s" % now)
                return now

            else:
                # Execute the init check
                content = requests.get(self.__url).text
                self.extract_function_args["content"] = content
                now = self.extract_function(self.extract_function_args)
                print("Now the %s check." % str(self.__count + 1))
                self.__count += 1
                self.__old_change = now
                print("Now result:%s" % now)
                return now

        old_stamp = time.time()
        old_content = check("Nothing", True)
        while True:
            if time.time() - old_stamp >= int(self.__interval):
                old_stamp = time.time()
                old_content = check(old_content)
            time.sleep(1)
            if self.stop:
                break
