import re

def findUrlAtMail(message):
    return re.findall('(http[s]?\:\/\/[a-zA-Z0-9.$_?\d"=&*%@\/#+-]+[.][a-z]{2,4}[^\s()<>]+)',message)