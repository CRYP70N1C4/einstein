import math,uuid
from PIL import Image
from functools import reduce


class jump:
    def __init__(self, path, debug=False):
        self.path = path
        self.debug = debug
        img = Image.open(path, "r");
        self.width, self.height = img.size;
        self.pixs = img.load()
        self.img = img
        self.src = self.get_cur_position()
        self.dest = self.get_dest()

    @staticmethod
    def get_distance(c1, c2, n=3):
        sum = 0
        for i in range(n):
            sum += (c1[i] - c2[i]) * (c1[i] - c2[i])
        return math.sqrt(sum)

    def get_bg_color(self):
        features = []
        for i in range(self.width - 2):
            features.append(self.pixs[i + 1, 1])
            features.append(self.pixs[i + 1, self.height - 1])

        for i in range(self.height - 2):
            features.append(self.pixs[1, i + 1])
            features.append(self.pixs[self.width - 1, i + 1])
        size = len(features)
        x, y, z = reduce(lambda x, y: (x[0] + y[0], x[1] + y[1], x[2] + y[2]), features)
        bg_color = (int)(x / size), (int)(y / size), (int)(z / size)
        return bg_color;

    def get_dest(self):
        bg_color = self.get_bg_color()
        m, n = -1, -1;
        flag = False
        for j in range(800, 1500):
            if flag: break
            for i in range(self.width):
                if self.get_distance(bg_color, self.pixs[i, j]) > 25:
                    m, n = i, j + 100
                    flag = True
                    break
        if self.debug:
            for i in range(m - 20, m + 20):
                for j in range(n - 20, n + 20):
                    self.pixs[i, j] = (255, 0, 0)
        return m, n;

    def get_cur_position(self):
        bg_color = (59, 56, 82)
        m, n = -1, -1;
        for j in range(900, 1500):
            for i in range(self.width):
                if self.get_distance(bg_color, self.pixs[i, j]) < 25:
                    m, n = i, j
        if self.debug:
            for i in range(m - 20, m + 20):
                for j in range(n - 20, n + 20):
                    self.pixs[i, j] = (255, 0, 0)
        return m, n;

    def get_length(self):
        if self.debug:
            self.img.save("E:\\tmp\\adb\\test\\%s.png" % uuid.uuid4().hex)
        return self.get_distance(self.src, self.dest, 2)

    def show(self):
        self.img.show()
