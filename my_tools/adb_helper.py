import os, time, logging, re, subprocess, sys, io
from PIL import Image


def execute(cmd):
    logging.debug("execute : %s" % cmd)
    print(cmd)
    return os.popen(cmd).read()


def input(text):
    os.system("adb shell input text %s" % text)


def click(x, y, duration=0, msg=""):
    x = int(x)
    y = int(y)
    logging.info(msg)
    if duration > 0:
        execute('adb shell input swipe {} {} {} {} {}'.format(x, y, x, y, duration))
    else:
        execute('adb shell input tap %d %d' % (x, y))


def get_display_size():
    rs = execute("adb shell wm size")
    size = re.search('(\d+)x(\d+)', rs)
    if size:
        return size.group(1), size.group(2)


def screenshots():
    process = subprocess.Popen('adb shell screencap -p', shell=True, stdout=subprocess.PIPE)
    data = process.stdout.read()
    print(type(data))
    if sys.platform == 'win32':
        data = data.replace(b'\r\n', b'\n')
    return Image.open(io.BytesIO(data))


def get_battery_info():
    return execute("adb shell dumpsys battery")
