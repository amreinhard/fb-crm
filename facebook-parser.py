#!/usr/bin/env python
import re, os
from HTMLParser import HTMLParser
from pprint import pprint

with open('friends.htm', 'r') as f: #closes automatically, handles any exceptions
    reading = f.read()

pyfile = os.path.dirname(os.path.abspath(__file__)) #wherever you go, there you are

class FriendParser(HTMLParser):

    stack = []
    current_head = ""
    data = ""
    header = ['html', 'body', 'div', 'h2']
    expected = ['html', 'body', 'div', 'ul', 'li']
    friends = []

    def handle_starttag(self, tag, attrs):
        self.stack.append(tag)
        if self.stack == self.expected:
            self.data = ""

    def handle_endtag(self, tag):
        if self.stack == self.expected:
            self.friends.append(Friend(self.data, self.current_head))
        self.stack.pop()

    def handle_data(self, data):
        if self.stack == self.expected:
            self.data += data
        if self.stack == self.header:
            self.current_head = data

    def handle_entityref(self, name):
        if self.stack == self.expected:
            self.data += name

    def handle_charref(self, name):
        if self.stack == self.expected:
            self.data += unichr(name) #hexadecimal bug - strip/map?

    #how do I map regex to str and get the groups back? name and date. match regex to str to get matches back

class Friend():

    name = ""
    status = ""
    date = ""

    def __init__(self, name, status):
        self.name, self.date = self._parse_name(name)
        self.status = status

    def _parse_name(self, name):
        #([^\(]+)\(([^)]+)\)
        return (name, "")

    def __str__(self):
        return "Friend(%s, %s)" % (self.name, self.status) #add status later

def message_name():
    """Finds names within message files."""
    idname = {}

    for subdir, dirs, files in os.walk(pyfile + '/messages'):
        for filename in files:
            message_open = open(filename, 'r')
            message_read = message_open.read()
            message_open.close()
            #how do I read from <title> brackets in every file?
            if filename not in idname:
                idname[filename[:-5]] = None

    pprint(idname)
    return idname

def id_association():
    """Associates names to IDs via dictionary."""

parser = FriendParser()
parser.feed(reading)
for friend in parser.friends:
    print friend
message_name()