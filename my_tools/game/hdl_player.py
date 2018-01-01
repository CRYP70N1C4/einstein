import adb_helper, time, uuid, os
from PIL import Image

base = "E:\\tmp\\smaple\\base.png"
basePIX = None;
features = [(1473, 23), (1513, 288), (1343, 79), (1458, 806), (1600, 917)]


def back(n=1):
    for i in range(n):
        adb_helper.tap_screen(1997, 39,"返回")
        time.sleep(0.5)


def is_fight():
    global basePIX
    if not basePIX:
        print("init")
        basePIX = Image.open(base, "r").load()
    tmp = "E:\\tmp\\adb\\%s.png" % uuid.uuid4().hex
    adb_helper.screenshots(tmp)
    curPIX = Image.open(tmp, "r").load()
    os.remove(tmp)
    for feature in features:
        if not curPIX[feature[0], feature[1]] == basePIX[feature[0], feature[1]]:
            return True
    return False;


# 英雄战场
def yxzc(n=6):
    adb_helper.tap_screen(431, 359,"选择竞技")
    adb_helper.tap_screen(447, 478,"选择对战模式")
    adb_helper.tap_screen(1473, 780,"选择单人匹配")
    for i in range(n):
        adb_helper.tap_screen(1828,996,"开始")
        time.sleep(80)
        while (is_fight()):
            time.sleep(3)
        adb_helper.tap_screen(1305, 1019,"结果确认")
        adb_helper.tap_screen(1288, 1002,"再来一局")
    back(3)


def tz(n):
    for i in range(n):
        adb_helper.tap_screen(1946, 1009,"开战")
        adb_helper.tap_screen(1728, 875,"扫荡")
        adb_helper.tap_screen(1073, 1000,"确认结果")
        adb_helper.tap_screen(1073, 1000,"确认结果")

# 一命通关，活动模式
def ymtghdmc(n=5, m=2, j=2, k=2):
    adb_helper.tap_screen(507, 509,"选择日常")
    adb_helper.tap_screen(350, 746,"选择一命通关")
    tz(n)
    back()
    adb_helper.tap_screen(841, 741,"选择活动模式")

    adb_helper.tap_screen(215, 151,"金币")
    tz(m)
    adb_helper.tap_screen(241, 249,"经验")
    tz(j)
    adb_helper.tap_screen(214, 355,"芯片")
    tz(k)
    back(2)


# 无尽模式
def wjms(n=2):
    adb_helper.tap_screen(1631, 498,"选择挑战")
    adb_helper.tap_screen(627, 809,"选择无尽")
    for i in range(n):
        adb_helper.tap_screen(1611, 1003,"扫荡")
        adb_helper.tap_screen(1524, 514,"普通扫荡")
        adb_helper.tap_screen(1366, 1006,"领取奖励")
        adb_helper.tap_screen(1366, 800,"领取奖励")
        adb_helper.tap_screen(804, 755,"确认")
    back(2)


if __name__ == '__main__':
    # yxzc()
    ymtghdmc()
    wjms()
    # adb_helper.screenshots("aa.png")