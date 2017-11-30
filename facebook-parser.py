#!/usr/bin/env python
import re, os
from HTMLParser import HTMLParser
from pprint import pprint
from pythonds.basic.stack import Stack

with open('friends.htm', 'r') as f: #closes automatically, handles any exceptions
    reading = f.read()

pyfile = os.path.dirname(os.path.abspath(__file__)) #wherever you go, there you are

class FriendParser(HTMLParser):

    s = Stack()
    friends = []
    current_head = ""
    data = ""
    header = ['html', 'body', 'div', 'h2']
    expected = ['html', 'body', 'div', 'ul', 'li']

    def handle_starttag(self, tag, attrs):
        self.s.push(tag)
        if self.s == self.expected:
            self.data = ""

    def handle_endtag(self, tag):
        if self.s == self.expected:
            self.friends.append(Friend(self.data, self.current_head))
        self.s.pop()

    def handle_data(self, data):
        if self.s == self.expected:
            self.data += data
        if self.s == self.header:
            self.current_head = data

    def handle_entityref(self, name):
        if self.s == self.expected:
            self.data += name

    def handle_charref(self, name):
        if self.s == self.expected:
            self.data += name #hexadecimal bug - unichr/chr? - strip/map?


class Friend():

    name = ""
    status = ""
    date = ""
    parens = r"([^\(]+)\(([^)]+)\)"

    def __init__(self, name, status):
        self.name, self.date = self._parse_name(name)
        self.status = status

    def _parse_name(self, name):
        clean = re.findall(self.parens)
        print name, clean
        return (name, clean)

    def __str__(self):
        return "Friend(%s, %s)" % (self.name, self.status)  # add status later


parser = FriendParser()
parser.feed(reading)
for friend in parser.friends:
    print friend