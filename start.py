import subprocess

from PIL import Image
import numpy as np
import time
import re

#adb_path = f"D:/leidian/LDPlayer9/adb.exe"
#emulator_address = '127.0.0.1:5555'

# x = 224, y = 157
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
    result = subprocess.run(f'{adb_path} connect {emulator_address}',shell=True,text=True,capture_output=True)
    if result.returncode != 0:
        print("emulater error")
    
def tap(adb_path, emulator_address, x, y):
    result = subprocess.run(f'{adb_path} -s {emulator_address} shell input tap {x} {y}', shell=True, text=True, capture_output=True)
    if result.returncode != 0:
        print("emulater error")

def tapes(adb_path, emulator_address, x, y):
    tap(adb_path, emulator_address, ES_folders_x[y-1], ES_folders_y[x-1])
    time.sleep(0.5)

def swipe(adb_path, emulator_address, start_x, start_y, end_x, end_y, duration=1000):
    result = subprocess.run(f'{adb_path} -s {emulator_address} shell input swipe {start_x} {start_y} {end_x} {end_y} {duration}', shell=True, text=True, capture_output=True)
    if result.returncode != 0:
        print("emulater error")

def screenshot(adb_path, emulator_address):
    result = subprocess.run(f'{adb_path} -s {emulator_address} shell screencap -p /sdcard/screenshot.png', shell=True, text=True, capture_output=True)
    if result.returncode != 0:
        print("emulater error")
    result = subprocess.run(f'{adb_path} -s {emulator_address} pull /sdcard/screenshot.png screenshot.png', shell=True, text=True, capture_output=True)
    if result.returncode != 0:
        print("emulater error")

def press_home(adb_path, emulator_address):
    result = subprocess.run(f'{adb_path} -s {emulator_address} shell input keyevent 3', shell=True, text=True, capture_output=True)
    if result.returncode != 0:
        print("emulater error")

def press_back(adb_path, emulator_address):
    result = subprocess.run(f'{adb_path} -s {emulator_address} shell input keyevent 4', shell=True, text=True, capture_output=True)
    if result.returncode != 0:
        print("emulater error")

def open_app(adb_path, emulator_address, package_name, activity_name):
    result = subprocess.run(f'{adb_path} -s {emulator_address} shell am start -n {package_name}/{activity_name}', shell=True, text=True, capture_output=True)
    if result.returncode != 0:
        print("emulater error")

def close_app(adb_path, emulator_address, package_name):
    result = subprocess.run(f'{adb_path} -s {emulator_address} shell am force-stop {package_name}', shell=True, text=True, capture_output=True)
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
        if get_color(332, 428) == (113, 213, 44):
            car_statue[i] = 1
        elif get_color(341, 438) == (210, 35, 37):
            car_statue[i] = 2
        else:
            car_statue[i] = 3
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

if __name__ == "__main__":

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
    new_build = [0,0,0,0,0,0]



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
    statuschange = 1
    for item in range(0, 25):
        if order_list[item] == 'jmp':
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
                time.sleep(1)
                press_back(adb_path, emulator_address)
                time.sleep(1)
                screenshot(adb_path, emulator_address)

        if status == 2:
            car_statue = get_car(adb_path, emulator_address)
            if car_statue == 0:
                car_statue = get_car(adb_path, emulator_address)
            if 3 not in car_statue:
                close_app(adb_path, emulator_address, package_name="com.zeptolab.cats.google")
                time.sleep(1)
                continue
            else:
                status = 4

        if status in [1, 4]:
            if status == 1:
                car_statue = [3, 3, 3]
                tap(adb_path, emulator_address, 1763, 990)  # ENLIST
                time.sleep(2)
                tap(adb_path, emulator_address, 1692, 873)  # START
                time.sleep(2)
                tap(adb_path, emulator_address, 1069, 916)  # LET'S FIGHT
                time.sleep(2)
            order = [char for char in order_list[item]] # 获取车辆属性指令
            if modeexecute == 0:
                screenshot(adb_path, emulator_address)
                modeexecute = 1
                if mode[0] == "auto":
                    for index, c in enumerate(build_area):
                        if pixelsstatic(c, ((175, 191, 209), (178, 195, 213))) > 200 or pixelsstatic(c, ((236, 173, 33), (239, 176, 36))) > 200:
                            car[index] = 'b'
                        elif pixelsstatic(build_area_a[index], ((209, 0, 29), (209, 0, 29))) > 5000:
                            car[index] = 'b'
                        else:
                            car[index] = 's'
            for index, c in enumerate(order):
                if car_statue[index] != 3:
                    continue
                end = 0
                a = 0
                if statuschange == 1:
                    screenshot(adb_path, emulator_address)
                    while a == 0:
                        for i in range(0, 6):
                            if get_color(build_point[i][0],build_point[i][1]) == (94, 106, 131):
                                build[i] = 0
                            elif get_color(build_point[i][0],build_point[i][1]) == (255, 101, 100):
                                build[i] = 2
                            elif get_color(build_point[i][0],build_point[i][1]) == (144, 179, 235):
                                build[i] = 1
                            else:
                                time.sleep(1)
                                screenshot(adb_path, emulator_address)
                                break
                            if i == 5:
                                if all(build[i] == 1 for i in range(len(car)) if car[i] == 'b') == True:
                                    car = ['b' if x == 's' else x for x in car]
                                a = 1
                                break
                    for i in range(0, 6):
                        if build[i] == 1 and car[i] != 'o':
                            continue
                        if car[i] == c or car[i] == 'o':
                            tap(adb_path, emulator_address, build_point[i][0], build_point[i][1])
                            time.sleep(1.5)
                            screenshot(adb_path, emulator_address)
                            while get_color(1188, 327) == (255, 141, 126):
                                time.sleep(1)
                                tap(adb_path, emulator_address, 1210, 447)  # ATTACK
                                time.sleep(1)
                                screenshot(adb_path, emulator_address)
                            if mode[1] == "e":
                                for j in p:
                                    if pixelsstatic(j, ((20, 77, 121),(20, 77, 121))) > 500:
                                        tap(adb_path, emulator_address, j[2], j[3])
                                        time.sleep(1)
                                        break
                            tap(adb_path, emulator_address, 344, 987)  # ATTACK

                            while True:
                                time.sleep(1)
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
                                            tap(adb_path, emulator_address, 1020, 900)
                                            time.sleep(1)
                                            screenshot(adb_path, emulator_address)
                                            while get_color(407, 957) not in ((210, 35, 37),(232, 145, 146)):
                                                tap(adb_path, emulator_address, 1020, 900)
                                                time.sleep(1)
                                                screenshot(adb_path, emulator_address)
                                            end = 1
                                            if get_color(954, 188) == (94, 106, 131):
                                                new_build[i] = 0
                                            elif get_color(954, 188) == (255, 101, 100):
                                                new_build[i] = 2
                                            elif get_color(954, 188) == (144, 179, 235):
                                                new_build[i] = 1
                                            else:
                                                new_build[i] = 3
                                            if build[i] == new_build[i]:
                                                statuschange = 0
                                            else:
                                                statuschange = 1
                                            break
                                        if get_color(407, 957) == (210, 35, 37):
                                            tap(adb_path, emulator_address, 407, 957)
                                            time.sleep(1)
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
                    if mode[1] == "e":
                        for j in p:
                            if pixelsstatic(j, ((20, 77, 121),(20, 77, 121))) > 500:
                                tap(adb_path, emulator_address, j[2], j[3])
                                time.sleep(1)
                                break
                    tap(adb_path, emulator_address, 344, 987)  # ATTACK

                    while True:
                        time.sleep(1)
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
                                    tap(adb_path, emulator_address, 1020, 900)
                                    time.sleep(1)
                                    screenshot(adb_path, emulator_address)
                                    while get_color(407, 957) not in ((210, 35, 37),(232, 145, 146)):
                                        tap(adb_path, emulator_address, 1020, 900)
                                        time.sleep(1)
                                        screenshot(adb_path, emulator_address)
                                    end = 1
                                    if get_color(954, 188) == (94, 106, 131):
                                        new_build[i] = 0
                                    elif get_color(954, 188) == (255, 101, 100):
                                        new_build[i] = 2
                                    elif get_color(954, 188) == (144, 179, 235):
                                        new_build[i] = 1
                                    else:
                                        new_build[i] = 3
                                    if build[i] == new_build[i]:
                                        statuschange = 0
                                    else:
                                        statuschange = 1
                                    break
                                if get_color(407, 957) == (210, 35, 37):
                                    tap(adb_path, emulator_address, 407, 957)
                                    time.sleep(1)
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

                        if end == 2:   
                            break
        close_app(adb_path, emulator_address, package_name="com.zeptolab.cats.google")
        time.sleep(1)




