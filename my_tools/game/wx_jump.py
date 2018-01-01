import adb_helper, uuid, time, os
from PIL import Image
from functools import reduce
import math

# adb_helper.execute("adb shell input keyevent 4")
# tmp = "E:\\tmp\\adb\\%s.png" % uuid.uuid4().hex
# adb_helper.screenshots(tmp)

import game.jump as jump


def generate():
    speed = 300
    for k in range(80):
        n = 1;
        speed += 10
        os.mkdir("E:\\tmp\\adb\\%d" % speed)
        for i in range(2):
            time.sleep(0.3)
            tmp = "E:\\tmp\\adb\\%d\\%d.png" % (speed, n)
            n += 1
            adb_helper.screenshots(tmp)
            adb_helper.keep_tap_screen(100, 100, speed)


base = "E:\\tmp\\adb\\1\\2.png"
basePIX = None;


def fail(curPIX):
    features = [(481, 1681), (393, 1685), (358, 1694)]
    global basePIX
    if not basePIX:
        print("init")
        basePIX = Image.open(base, "r").load()
    i = 0
    for feature in features:
        if not curPIX[feature[0], feature[1]] == basePIX[feature[0], feature[1]]:
            i+=1
    return i < len(features)


def get_time(dist):
    if dist < 300:
        return (int)(dist/ 0.682)
    else:
        return (int)(dist / 0.72)

def run(prefix):
    adb_helper.tap_screen(512, 1700, "再来一局")
    i = 0
    flag = False;
    os.mkdir(prefix)
    while (not flag):
        i += 1;
        tmp = "%s\\%d.png" % (prefix, i)
        adb_helper.screenshots(tmp)
        bol = jump.jump(tmp, True);
        dist = bol.get_length()
        ms = (int)(dist / 0.725)
        print(ms)
        print(dist)
        flag = fail(bol.pixs)
        adb_helper.keep_tap_screen(100, 100, ms)
        time.sleep(1)


for i in range(100):
    run("E:\\tmp\\adb\\training2\\%s" % i)
