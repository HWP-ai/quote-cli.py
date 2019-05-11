# -*- coding: utf-8 -*-

import os
import fcntl
import termios
import struct
import random
from codecs import open
from lib0screen import get_width as __get_width

screen_reset = '\033[0m'

code1 = '\033[44m '
code2 = '\033[46m '

def gettitle():
    lines = filter(lambda x: x, open('CSEN', encoding='utf8').readlines())
    x = random.choice(lines)
#    p1 = x.find(u'、') + 1
#    p2 = x.rfind(u'——')
    return u' %s ' % (x.strip())

title = gettitle()
wtitle = sum(__get_width(ord(x)) for x in title)
if wtitle % 2 == 0 :
    title = u' ' + title
    wtitle += 1

def terminal_size():
    th, tw, hp, wp = struct.unpack('HHHH',
        fcntl.ioctl(0, termios.TIOCGWINSZ,
        struct.pack('HHHH', 0, 0, 0, 0)))
    return tw, th

def background():
    tw, th = terminal_size()
    th -= 1
    tw4 = (tw - wtitle) // 4
    if (tw - wtitle) % 4 == 3 :
        tw4 += 1
    midl = (code1 + code2) * tw4 + screen_reset + u'\033[1;41m' \
           + title + ((code2 + code1) * tw4)[:-1] \
           + screen_reset + '\n'
    th4 = (th - 1) // 4
    line1 = (code1 + code2) * (tw4 * 2 + wtitle // 2)\
            + screen_reset + '\n'
    line2 = (code2 + code1) * (tw4 * 2 + wtitle // 2)\
            + screen_reset + '\n'
    print((line1 + line2) * th4
          + midl
          + (line2 + line1) * th4)
    
background()
