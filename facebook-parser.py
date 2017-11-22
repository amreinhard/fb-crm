import re, os
from pprint import pprint

opener = open('friends.html', 'r')
reading = opener.read()
opener.close()
pyfile = os.path.dirname(os.path.abspath(__file__))


def friend_parser():
    """Takes raw HTML, cleans via regex and splits all the names."""

    cleantext = re.sub(r'\[[^)]*\]', '', reading) #cleans dates
    cleantext2 = re.sub(r'\([^)]*\)', '', cleantext) #cleans emails
    splitter = cleantext2.split("</li><li>")
    newlist = [x.strip(' ') for x in splitter]

    pprint(newlist)

    return newlist


def message_name():
    """Finds names within message files."""
    idname = {}

    for subdir, dirs, files in os.walk(pyfile + '/messages'):
        for filename in files:
            message_open = open(filename + '.html', 'r')
            message_read = message_open.read()
            message_open.close()
            #how do I read from <title> brackets in every file?
            if filename not in idname:
                idname[filename[:-5]] = None

    pprint(idname)
    return idname

def id_association():
    """Associates names to IDs via dictionary."""


friend_parser()
message_name()