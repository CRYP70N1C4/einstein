import os
import sys
import subprocess
import time
import random
from my_tools import adb_helper

press_coefficient = 1.6  # 长按的时间系数，请自己根据实际情况调节
piece_base_height_1_2 = 20  # 二分之一的棋子底座高度，可能要调节
piece_body_width = 70  # 棋子的宽度，比截图中量到的稍微大一点比较安全，可能要调节


def jump(distance):
    press_time = distance * press_coefficient
    press_time = max(press_time, 200)
    press_time = int(press_time)++ seed()
    adb_helper.click(random.uniform(400, 900),random.uniform(400, 900), duration=press_time)


def is_piece_pixel(pixel):
    return (50 < pixel[0] < 60) and (53 < pixel[1] < 63) and (95 < pixel[2] < 110);


def find_piece_and_board(im,debug=False):
    w, h = im.size
    im_pixel = im.load()
    data=[]
    for i in range(int(w / 8), int(w * 7 / 8), 20):
        m_count = 0
        c_count = 0
        for j in range(int(h / 3), int(h * 2 / 3), 2):
            if is_piece_pixel(im_pixel[i, j]):
                c_count += 1
            else:
                m_count = max(m_count, c_count)
                c_count = 0
        if m_count > 7:
            data.append(i)
    piece = int(sum(data) / len(data))

    board = 0
    for i in range(int(h / 3), int(h * 2 / 3)):
        last_pixel = im_pixel[0, i]
        if board:
            break
        board_x_sum = 0
        board_x_count = 0

        for j in range(w):
            pixel = im_pixel[j, i]
            if abs(j - piece) < piece_body_width:
                continue
            if abs(pixel[0] - last_pixel[0]) + abs(pixel[1] - last_pixel[1]) + abs(pixel[2] - last_pixel[2]) > 10:
                board_x_sum += j
                board_x_count += 1
        if board_x_sum:
            board = int(board_x_sum / board_x_count)

    if debug:
        for i in range(h):
            for j in range(piece-10,piece+10):
                im_pixel[j,i]=(255,0,0)
            for j in range(board - 10, board + 10):
                    im_pixel[j, i] = (255, 0, 0)
    return piece,board

seeds=[0,0,-1,1,0,-1,1,0,1,-1]
index = 0
def seed():
    global  index
    index+=1
    index=index % 10
    return seeds[index]



def main():
    while True:
        im = adb_helper.screenshots()
        piece, board = find_piece_and_board(im,True)
        ts = int(time.time())
        jump(abs(piece-board))
        im.save("screenshot_backups/{}.png".format(ts))
        time.sleep(random.uniform(1.2, 1.8))  # 为了保证截图的时候应落稳了，多延迟一会儿


if __name__ == '__main__':
    main()