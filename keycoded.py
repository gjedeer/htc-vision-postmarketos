#!/usr/bin/python
import struct
import time
import sys
import os

infile_path = "/dev/input/event" + (sys.argv[1] if len(sys.argv) > 1 else "3")

#long int, long int, unsigned short, unsigned short, unsigned int
FORMAT = 'llHHI'
EVENT_SIZE = struct.calcsize(FORMAT)

framebuffer = int(os.getenv('FRAMEBUFFER', 0))

#open file in binary mode
in_file = open(infile_path, "rb")

buf = ""

POWER_BUTTON = 116
KEYUP = 0
KEYDOWN = 1

FB_BLANK_PATH = '/sys/class/graphics/fb%d/blank' % framebuffer

fb_blank = 0

power_key_down = None

def is_blank():
    return fb_blank

def toggle_blank():
    global fb_blank
    blank = is_blank()
    print "Blank: %d" % fb_blank
    with open(FB_BLANK_PATH, 'w') as f:
        f.write("%d" % int(not blank))

    fb_blank = int(not blank)
    print "Blank: %d" % fb_blank

while True:
    buf += in_file.read(1)

    if len(buf) >= EVENT_SIZE:
        event = buf[:EVENT_SIZE]
        buf = buf[EVENT_SIZE:]


        (tv_sec, tv_usec, type, code, value) = struct.unpack(FORMAT, event)

        if type != 0 or code != 0 or value != 0:
            print("Event type %u, code %u, value %u at %d.%d" % \
                (type, code, value, tv_sec, tv_usec))
            if type == 1:
                if code == POWER_BUTTON:
                    if value == KEYUP:
                        power_key_up = tv_sec + 0.000001 * tv_usec

                        if power_key_down and power_key_up - power_key_down > 5:
                            print "SHUTDOWN"
                            os.system("poweroff")
                        else:
                            toggle_blank()
                        power_key_down = None
                    elif value == KEYDOWN:
                        power_key_down = tv_sec + 0.000001 * tv_usec

        else:
            # Events with code, type and value == 0 are "separator" events
            print("===========================================")


in_file.close()
