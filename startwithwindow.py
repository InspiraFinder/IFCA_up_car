import subprocess

from PIL import Image
import numpy as np
import time
import re
import os

import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QTextEdit, QPushButton, QVBoxLayout, QWidget
from PyQt6.QtCore import QThread, pyqtSignal
from io import StringIO
import contextlib

ES_folders_x = [687, 911, 1135, 1359, 1583, 1807]
ES_folders_y = [259, 416, 573, 730, 887, 1044]

build_point = [(559, 533),(471, 771),(860, 913),(1295, 930),(1619, 778),(1594, 508)]
build_area = [(429, 472, 694, 556), (341, 710, 606, 794), (730, 852, 995, 936), (1165, 869, 1430, 953), (1489, 717, 1754, 801), (1464, 447, 1729, 531)]
build_area_a = [(429, 382, 694, 466), (341, 620, 606, 704), (730, 762, 995, 846), (1165, 779, 1430, 863), (1489, 627, 1754, 711), (1464, 357, 1729, 441)]

p = [(773, 315, 830, 373),(773, 565, 830, 623),(773, 815, 830, 873),
     (1091, 315, 1148, 373),(1091, 565, 1148, 623),(1091, 815, 1148, 873),
     (1409, 315, 1466, 373),(1409, 565, 1466, 623),(1409, 815, 1466, 873),
     (1727, 315, 1784, 373),(1727, 565, 1784, 623),(1727, 815, 1784, 873)]

car_point = [(288, 811),(427, 811),(566, 811)]

def connect(adb_path, emulator_address):
    result = subprocess.run(f'{adb_path} connect {emulator_address}',shell=True,text=True,capture_output=True, encoding="utf-8")
    if result.returncode != 0:
        print("emulater error")
    
def tap(adb_path, emulator_address, x, y):
    result = subprocess.run(f'{adb_path} -s {emulator_address} shell input tap {x} {y}', shell=True, text=True, capture_output=True, encoding="utf-8")
    if result.returncode != 0:
        print("emulater error")

def tapes(adb_path, emulator_address, x, y):
    tap(adb_path, emulator_address, ES_folders_x[y-1], ES_folders_y[x-1])
    time.sleep(0.5)

def swipe(adb_path, emulator_address, start_x, start_y, end_x, end_y, duration=1000):
    result = subprocess.run(f'{adb_path} -s {emulator_address} shell input swipe {start_x} {start_y} {end_x} {end_y} {duration}', shell=True, text=True, capture_output=True, encoding="utf-8")
    if result.returncode != 0:
        print("emulater error")

def screenshot(adb_path, emulator_address):
    result = subprocess.run(f'{adb_path} -s {emulator_address} shell screencap -p /sdcard/screenshot.png', shell=True, text=True, capture_output=True, encoding="utf-8")
    if result.returncode != 0:
        print("emulater error")
    result = subprocess.run(f'{adb_path} -s {emulator_address} pull /sdcard/screenshot.png screenshot.png', shell=True, text=True, capture_output=True, encoding="utf-8")
    if result.returncode != 0:
        print("emulater error")

def press_home(adb_path, emulator_address):
    result = subprocess.run(f'{adb_path} -s {emulator_address} shell input keyevent 3', shell=True, text=True, capture_output=True, encoding="utf-8")
    if result.returncode != 0:
        print("emulater error")

def press_back(adb_path, emulator_address):
    result = subprocess.run(f'{adb_path} -s {emulator_address} shell input keyevent 4', shell=True, text=True, capture_output=True, encoding="utf-8")
    if result.returncode != 0:
        print("emulater error")

def open_app(adb_path, emulator_address, package_name, activity_name):
    result = subprocess.run(f'{adb_path} -s {emulator_address} shell am start -n {package_name}/{activity_name}', shell=True, text=True, capture_output=True, encoding="utf-8")
    if result.returncode != 0:
        print("emulater error")

def close_app(adb_path, emulator_address, package_name):
    result = subprocess.run(f'{adb_path} -s {emulator_address} shell am force-stop {package_name}', shell=True, text=True, capture_output=True, encoding="utf-8")
    if result.returncode != 0:
        print("emulater error")

def get_color(x, y):

    image = Image.open("screenshot.png")
    pixel_color = image.getpixel((x, y))
    result = pixel_color[:3]

    return result

def pixelsstatic(area, color):
    image = Image.open("screenshot.png")
    cropped_image = image.crop(area)
    image_np = np.array(cropped_image)
    count = 0
    for i in range(image_np.shape[0]):
        for j in range(image_np.shape[1]):
            pixel = image_np[i, j]
            if all(color[0][k] <= pixel[k] <= color[1][k] for k in range(3)):
                    count += 1
    return count

 
def get_car(adb_path, emulator_address):
    car_statue = [0, 0, 0]  # 1 = defend, 2 = fix, 3 = ready
    car_statue_check = [0, 0, 0]
    while True:
        screenshot(adb_path, emulator_address)
        if get_color(29, 607) == (85, 116, 206):
            tap(adb_path, emulator_address, 29, 607)
            time.sleep(3)
            screenshot(adb_path, emulator_address)
        if get_color(458, 607) == (85, 116, 206):
            time.sleep(1)
            break
        if get_color(1126, 128) != (145, 167, 192):
            while get_color(1775, 662) not in ((53, 79, 127), (52, 78, 126)):
                time.sleep(1)
                press_back(adb_path, emulator_address)
                time.sleep(1)
                screenshot(adb_path, emulator_address)
            tap(adb_path, emulator_address, 1720, 61)  # CITY KINGS
            time.sleep(2)
    while True:
        screenshot(adb_path, emulator_address)
        if get_color(131, 793) == (255, 255, 255):
            i = 0
        elif get_color(248, 793) == (255, 255, 255):
            i = 1
        elif get_color(365, 793) == (255, 255, 255):
            i = 2
        else:
            return 0
        car_statue_check[i] = 1
        if get_color(115, 428) == (113, 213, 44):
            car_statue[i] = 1
        elif get_color(341, 438) == (210, 35, 37):
            car_statue[i] = 2
        elif get_color(392, 576) != (255, 255, 255) and get_color(100, 400) == (114, 149, 224):
            car_statue[i] = 3
        else:
            car_statue[i] = 4
        car_cor = get_car_color(adb_path, emulator_address)
        if car_statue_check[0] == 0:
            nextx = 131
        elif car_statue_check[1] == 0:
            nextx = 248
        elif car_statue_check[2] == 0:
            nextx = 365
        else:
            while True:
                screenshot(adb_path, emulator_address)
                if get_color(458, 607) == (85, 116, 206):
                    tap(adb_path, emulator_address, 458, 607)
                    time.sleep(3)
                    screenshot(adb_path, emulator_address)
                if get_color(29, 607) == (85, 116, 206):
                    time.sleep(1)
                    break
                if get_color(1126, 128) != (145, 167, 192):
                    while get_color(1775, 662) not in ((53, 79, 127), (52, 78, 126)):
                        time.sleep(1)
                        press_back(adb_path, emulator_address)
                        time.sleep(1)
                        screenshot(adb_path, emulator_address)
                    tap(adb_path, emulator_address, 1720, 61)  # CITY KINGS
                    time.sleep(2)
            return car_statue
        while True:
            tap(adb_path, emulator_address, nextx, 793)
            time.sleep(3)
            car_ncor = get_car_color(adb_path, emulator_address)
            if car_ncor != car_cor:
                break
        
def get_car_color(adb_path, emulator_address):
    screenshot(adb_path, emulator_address)
    car_color = []
    car_color.extend(get_color(230, 530))
    car_color.extend(get_color(190, 595))
    car_color.extend(get_color(285, 595))
    return car_color

def main():
# 读取配置文件
    with open('config.txt', 'r', encoding='utf-8') as file:
        lines = file.readlines()

    adb_path = lines[0].strip()
    print(f"adb_path: {adb_path}")
    emulator_address = lines[1].strip()
    print(f"emulator_address: {emulator_address}")
    folder_input = lines[2].strip()
    folder = [int(num) for num in folder_input.strip('[]').split(',')]
    print(f"folder: {folder}")
    lines_to_process = lines[3:8]
    order_list = []
    for line in lines_to_process:
        elements = line.strip('[]\n').split(',')
        order_list.extend([element.strip() for element in elements])
    print(f"order_list: {order_list}")
    car_input = lines[8].strip()
    car = [char for char in car_input.strip('[]').split(',')]
    print(f"car: {car}")
    mode_input = lines[9].strip()
    mode = [string for string in mode_input.strip('[]').split(',')]
    print(f"mode: {mode}")
    build = [0,0,0,0,0,0]
    bbuild = [0,0,0,0,0,0]
    sbuild = [0,0,0,0,0,0]
    new_build = [0,0,0,0,0,0]
    blp = [0,0,0,0,0,0]



    connect(adb_path, emulator_address)
    close_app(adb_path, emulator_address, package_name="com.zeptolab.cats.google")
    close_app(adb_path, emulator_address, package_name="com.estrongs.android.pop")
    open_app(adb_path, emulator_address, package_name="com.estrongs.android.pop", activity_name=".app.openscreenad.NewSplashActivity")
    time.sleep(5)
    tap(adb_path, emulator_address, 144, 766)  # 主目录
    time.sleep(0.5)
    tapes(adb_path, emulator_address, 1, 2)  # 选择你的主文件夹，第一排第二个
    tapes(adb_path, emulator_address, folder[0], folder[1])  # 选择你的次文件夹
    modeexecute = 0
    for item in range(0, 25):
        if mode[1] == "firstline":
            if item >= 5:
                break
        print(f"Processing item {item + 1}")
        if order_list[item] == 'jmp':
            print(f"Item {item + 1} will be jumped")
            continue
        open_app(adb_path, emulator_address, package_name="com.estrongs.android.pop", activity_name=".app.openscreenad.NewSplashActivity")
        y = item % 6 + 1
        x = item // 6 + 1
        tapes(adb_path, emulator_address, x, y)
        while True:
            screenshot(adb_path, emulator_address)
            if get_color(898, 689) == (215, 215, 215):
                time.sleep(0.5)
                tap(adb_path, emulator_address, 898, 689)
                break
        time.sleep(1)
        press_home(adb_path, emulator_address)
        open_app(adb_path, emulator_address, package_name="com.zeptolab.cats.google", activity_name="com.zeptolab.cats.CATSActivity")
        time.sleep(35)
        screenshot(adb_path, emulator_address)

        status = 0
        while get_color(1775, 662) not in ((53, 79, 127), (52, 78, 126)):
            if get_color(384, 722) == (236, 224, 210):
                swipe(adb_path, emulator_address, 1313, 372, 13, 372)
            time.sleep(1)
            press_back(adb_path, emulator_address)
            time.sleep(1)
            screenshot(adb_path, emulator_address)

        status = 1
        while True:
            tap(adb_path, emulator_address, 1720, 61)  # CITY KINGS
            time.sleep(2)
            screenshot(adb_path, emulator_address)
            if get_color(1126, 128) == (145, 167, 192):
                status = 2
                break
            if get_color(1126, 128) == (255, 255, 255):
                break
            while get_color(1775, 662) not in ((53, 79, 127), (52, 78, 126)):
                if get_color(384, 722) == (236, 224, 210):
                    swipe(adb_path, emulator_address, 1313, 372, 13, 372)
                time.sleep(1)
                press_back(adb_path, emulator_address)
                time.sleep(1)
                screenshot(adb_path, emulator_address)

        if status == 2:
            car_statue = get_car(adb_path, emulator_address)
            if car_statue == 0:
                car_statue = get_car(adb_path, emulator_address)
            print(f"car_statue: {car_statue}")
            if 3 not in car_statue:
                close_app(adb_path, emulator_address, package_name="com.zeptolab.cats.google")
                if not os.path.exists("report.txt"):
                    with open("report.txt", "w", encoding="utf-8") as file:
                        pass
                with open("report.txt", "a", encoding="utf-8") as file:
                    formatedoutput = f"Item {item + 1}: "
                    file.write(formatedoutput)
                    formatedoutput = f"{car_statue}\n"
                    file.write(formatedoutput)
                print(f"Item {item + 1} processed")
                time.sleep(1)
                continue
            else:
                status = 4

        if status in [1, 4]:
            if status == 1:
                car_statue = [3, 3, 3]
                print(f"car_statue: {car_statue}")
                tap(adb_path, emulator_address, 1763, 990)  # ENLIST
                time.sleep(2)
                tap(adb_path, emulator_address, 1692, 873)  # START
                time.sleep(2)
                tap(adb_path, emulator_address, 1069, 916)  # LET'S FIGHT
                time.sleep(2)
            statuschange = 1
            order = [char for char in order_list[item]]  # 获取车辆属性指令
            order.append('u') 
            if modeexecute == 0:
                screenshot(adb_path, emulator_address)
                modeexecute = 1
                if mode[0] == "auto":
                    for index, c in enumerate(build_area):
                        if pixelsstatic(build_area_a[index], ((209, 0, 29), (209, 0, 29))) > 5000:
                            build[index] = 6
                        elif pixelsstatic(c, ((175, 191, 209), (178, 195, 213))) > 200 or pixelsstatic(c, ((236, 173, 33), (239, 176, 36))) > 200:
                            car[index] = 'b'
                        else:
                            car[index] = 's'
                elif mode[0] == "autoultra":
                    for index, c in enumerate(build_area):
                        if pixelsstatic(build_area_a[index], ((209, 0, 29), (209, 0, 29))) > 5000:
                            build[index] = 6
                        elif pixelsstatic(c, ((175, 191, 209), (178, 195, 213))) > 200 or pixelsstatic(c, ((236, 173, 33), (239, 176, 36))) > 200:
                            car[index] = 'o'
                        else:
                            car[index] = 's'
            for index, c in enumerate(order):
                if index == 3:
                    continue
                if car_statue[index] != 3:
                    continue
                end = 0
                a = 0
                final = 0
                if statuschange == 1:
                    screenshot(adb_path, emulator_address)
                    while a == 0:
                        for i in range(0, 6):
                            blue = pixelsstatic(build_area[i], ((144, 179, 235), (144, 179, 235)))
                            red = pixelsstatic(build_area[i], ((255, 101, 100), (255, 101, 100)))
                            grey = pixelsstatic(build_area[i], ((94, 106, 131), (94, 106, 131)))
                            sum = blue + red + grey
                            blp[i] = blue / sum
                            if car[i] in ['a','b','o'] and blp[i] <= 0.5 and build[i] == 6:
                                bbuild[i] = 3
                            elif car[i] in ['a','b','o'] and blp[i] <= 0.5:
                                bbuild[i] = 2
                            elif car[i] == 'o':
                                bbuild[i] = 1
                            else:
                                bbuild[i] = 0
                            if car[i] in ['a','s'] and blp[i] <= 0.5 and build[i] == 6:
                                sbuild[i] = 3
                            elif car[i] in ['a','s'] and blp[i] <= 0.5:
                                sbuild[i] = 2
                            elif car[i] == 'o' and blp[i] >= 0.7:
                                sbuild[i] = 1
                            else:
                                sbuild[i] = 0
                            if build[i] == 6 and blp[i] <= 0.5 and car[i] != 'n':
                                build[i] = 6
                            elif blp[i] <= 0.5 and car[i] != 'n':
                                build[i] = 5
                            elif blp[i] >= 0.5 and car[i] == 'o':
                                build[i] = 1
                            else:
                                build[i] = 0
                            if blp[i] >= 0.99:
                                build[i] = 0
                                bbuild[i] = 0
                                sbuild[i] = 0
                            if sum <= 100:
                                time.sleep(1)
                                screenshot(adb_path, emulator_address)
                                break
                            if i == 5:
                                if 6 not in build and 5 not in build and 1 in build:
                                    indices = [i for i, value in enumerate(build) if value == 1]
                                    sorted_indices = sorted(indices, key=lambda i: blp[i], reverse=True)
                                    value = 5
                                    for indexx in sorted_indices:
                                        build[indexx] = value
                                        value -= 1
                                if 3 not in bbuild and 2 not in bbuild and 1 in bbuild:
                                    indices = [i for i, value in enumerate(bbuild) if value == 1]
                                    sorted_indices = sorted(indices, key=lambda i: blp[i], reverse=True)
                                    value = 5
                                    for indexx in sorted_indices:
                                        bbuild[indexx] = value
                                        value -= 1
                                if 3 not in sbuild and 2 not in sbuild and 1 in sbuild:
                                    indices = [i for i, value in enumerate(sbuild) if value == 1]
                                    sorted_indices = sorted(indices, key=lambda i: blp[i], reverse=True)
                                    value = 5
                                    for indexx in sorted_indices:
                                        sbuild[indexx] = value
                                        value -= 1
                                max_value = max(build)
                                bmax_value = max(bbuild)
                                smax_value = max(sbuild)
                                build = [1 if x == max_value else 0 for x in build]
                                bbuild = [1 if x == bmax_value else 0 for x in bbuild]
                                sbuild = [1 if x == smax_value else 0 for x in sbuild]
                                if all(bbuild[i] == 0 for i in range(len(car)) if car[i] in ('b', 'o', 'a')) == True:
                                    car = ['a' if x == 's' else x for x in car]
                                a = 1
                                break
                    for i in range(0, 6):
                        if build[i] == 0:
                            continue
                        if (car[i] in ('o', 'a') or car[i] == c) and build[i] == 1:
                            tap(adb_path, emulator_address, build_point[i][0], build_point[i][1])
                            time.sleep(1.5)
                            screenshot(adb_path, emulator_address)
                            while get_color(1188, 327) != (255, 141, 126):
                                time.sleep(0.5)
                                screenshot(adb_path, emulator_address)
                            while get_color(1188, 327) == (255, 141, 126):
                                time.sleep(1)
                                tap(adb_path, emulator_address, 1210, 447)  # ATTACK
                                time.sleep(1)
                                screenshot(adb_path, emulator_address)
                            if mode[2] == "e":
                                for j in p:
                                    if pixelsstatic(j, ((20, 77, 121),(20, 77, 121))) > 500:
                                        tap(adb_path, emulator_address, j[2], j[3])
                                        time.sleep(1)
                                        break
                            
                            tap(adb_path, emulator_address, 344, 987)  # ATTACK

                            while True:
                                time.sleep(1)
                                screenshot(adb_path, emulator_address)
                                if get_color(407, 957) in ((210, 35, 37), (232, 145, 146)) and end == 0:
                                    tap(adb_path, emulator_address, 344, 987)  # ATTACK
                                    screenshot(adb_path, emulator_address)
                                if get_color(149, 657) in ((115, 69, 55), (115, 70, 56)):
                                    time.sleep(1)
                                    tap(adb_path, emulator_address, car_point[index][0], car_point[index][1])
                                    time.sleep(1)
                                    tap(adb_path, emulator_address, 960, 540)  # ATTACK
                                    time.sleep(10)
                                    while True:
                                        screenshot(adb_path, emulator_address)
                                        if get_color(1217, 225) in ((193, 40, 41), (120, 44, 20)):
                                            if get_color(1217, 225) == (193, 40, 41):
                                                final = 1
                                            if get_color(1217, 225) == (120, 44, 20):
                                                final = 2
                                            tap(adb_path, emulator_address, 1020, 900)
                                            time.sleep(1)
                                            screenshot(adb_path, emulator_address)
                                            while get_color(407, 957) not in ((210, 35, 37), (232, 145, 146)):
                                                tap(adb_path, emulator_address, 1020, 900)
                                                time.sleep(1)
                                                screenshot(adb_path, emulator_address)
                                            end = 1
                                            if get_color(954, 188) == (144, 179, 235):
                                                new_build[i] = 0
                                            else:
                                                new_build[i] = 1
                                            if (new_build[i] == 1 and (order[index] == order[index + 1] or (car[i] == 'a' and order[index + 1] != 'n'))) or car[i] == 'o':
                                                statuschange = 0
                                            else:
                                                statuschange = 1
                                            break
                                
                                if end == 1:
                                    if statuschange == 1:
                                        while True:
                                            screenshot(adb_path, emulator_address)
                                            if get_color(1126, 128) == (145, 167, 192):
                                                end = 2
                                                break
                                            else:
                                                press_back(adb_path, emulator_address)
                                                time.sleep(1)   
                                    else:
                                        end = 2
                                        break   

                                if end == 2:   
                                    break

                            if end == 2:
                                break
                else:
                    while True:
                        screenshot(adb_path, emulator_address)
                        if get_color(458, 607) == (85, 116, 206):
                            tap(adb_path, emulator_address, 458, 607)
                            time.sleep(3)
                            screenshot(adb_path, emulator_address)
                        if get_color(29, 607) == (85, 116, 206):
                            time.sleep(1)
                            break
                    if mode[2] == "e":
                        for j in p:
                            if pixelsstatic(j, ((20, 77, 121),(20, 77, 121))) > 500:
                                tap(adb_path, emulator_address, j[2], j[3])
                                time.sleep(1)
                                break
                    tap(adb_path, emulator_address, 344, 987)  # ATTACK

                    while True:
                        time.sleep(1)
                        screenshot(adb_path, emulator_address)
                        if get_color(407, 957) in ((210, 35, 37), (232, 145, 146)) and end == 0:
                            tap(adb_path, emulator_address, 344, 987)  # ATTACK
                            screenshot(adb_path, emulator_address)
                        if get_color(149, 657) in ((115, 69, 55), (115, 70, 56)):
                            time.sleep(1)
                            tap(adb_path, emulator_address, car_point[index][0], car_point[index][1])
                            time.sleep(1)
                            tap(adb_path, emulator_address, 960, 540)  # ATTACK
                            time.sleep(10)
                            while True:
                                screenshot(adb_path, emulator_address)
                                if get_color(1217, 225) in ((193, 40, 41), (120, 44, 20)):
                                    if get_color(1217, 225) == (193, 40, 41):
                                        final = 1
                                    if get_color(1217, 225) == (120, 44, 20):
                                        final = 2
                                    tap(adb_path, emulator_address, 1020, 900)
                                    time.sleep(1)
                                    screenshot(adb_path, emulator_address)
                                    while get_color(407, 957) not in ((210, 35, 37), (232, 145, 146), (255, 96, 90)):
                                        tap(adb_path, emulator_address, 1020, 900)
                                        time.sleep(1)
                                        screenshot(adb_path, emulator_address)
                                    end = 1
                                    if get_color(954, 188) == (144, 179, 235):
                                        new_build[i] = 0
                                    else:
                                        new_build[i] = 1
                                    if (new_build[i] == 1 and (order[index] == order[index + 1] or (car[i] == 'a' and order[index + 1] != 'n'))) or car[i] == 'o':
                                        statuschange = 0
                                    else:
                                        statuschange = 1
                                    break

                        if end == 1:
                            if statuschange == 1:
                                while True:
                                    screenshot(adb_path, emulator_address)
                                    if get_color(1126, 128) == (145, 167, 192):
                                        end = 2
                                        break
                                    else:
                                        press_back(adb_path, emulator_address)
                                        time.sleep(1)  
                            else:
                                end == 2
                                break    

                        if end == 2:   
                            break
                if final == 1:
                    car_statue[index] = 1
                if final == 2:
                    car_statue[index] = 2

        close_app(adb_path, emulator_address, package_name="com.zeptolab.cats.google")
        if not os.path.exists("report.txt"):
            with open("report.txt", "w", encoding="utf-8") as file:
                pass
        with open("report.txt", "a", encoding="utf-8") as file:
            formatedoutput = f"Item {item + 1}: "
            file.write(formatedoutput)
            formatedoutput = f"{car_statue}\n"
            file.write(formatedoutput)
        print(f"Item {item + 1} processed")
        time.sleep(1)

class RedirectedIO(StringIO):
    def __init__(self, signal):
        super().__init__()
        self.signal = signal
        self.last_emit_time = time.time()  

    def write(self, message):
        super().write(message)
        current_time = time.time()
        if current_time - self.last_emit_time >= 1:  
            self.flush()
            output = self.getvalue().strip()
            if output: 
                self.signal.emit(output)
                self.truncate(0)
                self.seek(0)
            self.last_emit_time = current_time

class WorkerThread(QThread):
    output_signal = pyqtSignal(str)

    @contextlib.contextmanager
    def redirect_stdout(self, new_stdout):
        old_stdout = sys.stdout
        sys.stdout = new_stdout
        try:
            yield
        finally:
            sys.stdout = old_stdout

    def run(self):
        with self.redirect_stdout(RedirectedIO(self.output_signal)):
            main()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("IFCA-UP-UP-CAR-🚗")

        self.resize(320, 240)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout(self.central_widget)

        self.output_box = QTextEdit(self)
        self.output_box.setReadOnly(True)
        self.layout.addWidget(self.output_box)

        self.start_button = QPushButton("START", self)
        self.start_button.clicked.connect(self.on_start_clicked)
        self.layout.addWidget(self.start_button)

        self.worker_thread = None

    def on_start_clicked(self):
        if self.worker_thread is None or not self.worker_thread.isRunning():
            self.start_button.setEnabled(False)
            self.start_button.setText("Processing...")

            self.worker_thread = WorkerThread()
            self.worker_thread.output_signal.connect(self.update_output_box)
            self.worker_thread.finished.connect(self.on_task_finished)
            self.worker_thread.start()

    def update_output_box(self, output):
        self.output_box.append(output)

    def on_task_finished(self):
        self.start_button.setEnabled(True)
        self.start_button.setText("START")
        self.worker_thread = None

if __name__ == "__main__":
    app = QApplication(sys.argv)

    main_window = MainWindow()
    main_window.show()

    sys.exit(app.exec())



