#!/bin/env python3

from html.parser import HTMLParser

class SummaryParser(HTMLParser):
    def __init__(self, count):
        HTMLParser.__init__(self)
        self.count = count
        self.summary = []
        self.tag_stack = []

    def feed(self, data):
        HTMLParser.feed(self, '<html>%s</html>' % data)

    def handle_startendtag(self, tag, attrs):
        if self.count:
            self.summary.append('<%s/>' % tag)

    def handle_starttag(self, tag, attrs):
        if self.count and tag != 'html':
            self.summary.append('<%s>' % tag)
            self.tag_stack.append(tag)

    def handle_endtag(self, tag):
        if len(self.tag_stack):
            if self.tag_stack[-1] == tag:
                self.summary.append('</%s>' % tag)
                self.tag_stack.pop()

    def handle_data(self, data):
        need = self.count
        if need:
            if len(data) < need:
                need = len(data)
            self.summary.append(data[:need])
            self.count = self.count - need

    def get_summary(self):
        if not self.count:
            self.summary.append('...')
        return ''.join(self.summary)

if __name__ == '__main__':
    sp = SummaryParser(10)
    sp.feed("<p><a href='123'>test测试测试这只是一个测试</li></a></p>")
    print(sp.get_summary())
                

