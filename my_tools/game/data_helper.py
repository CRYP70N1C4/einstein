import os, game.jump as jump

prefix = "E:\\tmp\\adb"
dirs = os.listdir(prefix)
folders = []
for dir in dirs:
    if dir.endswith("0"):
        files = os.listdir(prefix + "\\" + dir)
        if (len(files) == 2):
            folders.append(prefix + "\\" + dir)

for folder in folders:
    try:
        src1 = folder + "\\1.png"
        src2 = folder + "\\2.png"
        bol1 = jump.jump(src1, True)
        bol2 = jump.jump(src2, True)
        dist = bol1.get_distance(bol1.src, bol2.src, 2)
        time = folder.replace("E:\\tmp\\adb\\", "")
        print("%s,%s" % (time, dist))
    except Exception:
        print(folder)
