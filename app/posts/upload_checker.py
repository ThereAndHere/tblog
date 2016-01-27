#!/bin/env python3

import imghdr
import random, string

class UploadChecker:


    def __init__(self, fs):
        self.accept_type = ['jpeg', 'png']
        self.fs = fs
        self.is_ok = False
        self.message = ""
        self.file_type = ""
        self.check()

    def check(self):
        re = imghdr.what(self.fs.stream)
        print(re)
        if re and re in self.accept_type:
            self.is_ok = True
            self.message = "ok"
            self.file_type = re
        else:
            self.is_ok = False
            self.message = "Not support type"

    def get_result(self):
        return self.is_ok

    def get_msg(self):
        return self.message

    def get_filename(self):
        rstring = string.ascii_letters + string.digits
        fname =  ''.join([rstring[x] for x in random.sample(range(0,len(rstring)),32)]) 
        fname = fname + "." + self.file_type
        return fname




