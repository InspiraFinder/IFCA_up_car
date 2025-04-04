import subprocess

from PIL import Image
import time
import re

#adb_path = f"D:/leidian/LDPlayer9/adb.exe"
#emulator_address = '127.0.0.1:5555'

# x = 224, y = 157
ES_folders_x = [687, 911, 1135, 1359, 1583, 1807]
ES_folders_y = [259, 416, 573, 730, 887, 1044]

build_point = [(559, 533),(471, 771),(860, 913),(1295, 930),(1619, 778),(1594, 508)]
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
    tap(adb_path, emulator_address, ES_folders_x[x-1], ES_folders_y[y-1])
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

if __name__ == "__main__":

    # 读取配置文件
    with open('config.txt', 'r', encoding='utf-8') as file:
        lines = file.readlines()

    adb_path = lines[0].strip()
    emulator_address = lines[1].strip()
    folder_input = lines[2].strip()
    folder = [int(num) for num in folder_input.strip('[]').split(',')]
    lines_to_process = lines[3:8]
    order_list = []
    for line in lines_to_process:
        elements = line.strip('[]\n').split(',')
        order_list.extend([element.strip() for element in elements])
    car_input = lines[8].strip()
    car = [char for char in car_input.strip('[]').split(',')]
    build = [0,0,0,0,0,0]



    connect(adb_path, emulator_address)
    open_app(adb_path, emulator_address, package_name="com.estrongs.android.pop", activity_name=".app.openscreenad.NewSplashActivity")
    time.sleep(5)
    tap(adb_path, emulator_address, 144, 766)  # 主目录
    time.sleep(0.5)
    tapes(adb_path, emulator_address, 1, 2)  # 选择你的主文件夹，第一排第二个
    tapes(adb_path, emulator_address, folder[0], folder[1])  # 选择你的次文件夹
    for item in range(0, 25):
        open_app(adb_path, emulator_address, package_name="com.estrongs.android.pop", activity_name=".app.openscreenad.NewSplashActivity")
        x = item % 6 + 1
        y = item // 6 + 1
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
        while get_color(1775, 662) != (53, 79, 127):
            time.sleep(1)
            press_back(adb_path, emulator_address)
            time.sleep(1)
            screenshot(adb_path, emulator_address)

        status = 1
        while True:
            tap(adb_path, emulator_address, 1720, 61)  # CITY KINGS
            time.sleep(2)
            if get_color(1126, 128) == (145, 167, 192):
                status = 2
                break
            if get_color(1126, 128) == (255, 255, 255):
                break
            while get_color(1775, 662) != (53, 79, 127):
                time.sleep(1)
                press_back(adb_path, emulator_address)
                time.sleep(1)
                screenshot(adb_path, emulator_address)

        if status == 2:
            close_app(adb_path, emulator_address, package_name="com.zeptolab.cats.google")
            time.sleep(1)
            continue

        if status == 1:
            tap(adb_path, emulator_address, 1763, 990)  # ENLIST
            time.sleep(2)
            tap(adb_path, emulator_address, 1692, 873)  # START
            time.sleep(2)
            tap(adb_path, emulator_address, 1069, 916)  # LET'S FIGHT
            time.sleep(2)
            order = [char for char in order_list[item]] # 获取车辆属性指令
            screenshot(adb_path, emulator_address)
            for i in range(0, 6):
                if get_color(build_point[i][0],build_point[i][1]) == (144, 179, 235):
                    build[i] = 1
                elif get_color(build_point[i][0],build_point[i][1]) == (255, 101, 100):
                    build[i] = 2
            for c in order:
                for i in range(0, 6):
                    if build[i] == 0:
                        continue
                    if car[i] == c:
                        tap(adb_path, emulator_address, build_point[i][0], build_point[i][1])
                        time.sleep(1.5)
                        screenshot(adb_path, emulator_address)
                        while get_color(1188, 327) == (255, 141, 126):
                            time.sleep(1)
                            tap(adb_path, emulator_address, 1210, 447)  # ATTACK
                            time.sleep(1)
                            screenshot(adb_path, emulator_address)
                        tap(adb_path, emulator_address, 344, 987)  # ATTACK
                        time.sleep(1)
                        screenshot(adb_path, emulator_address)
                        while get_color(149, 657) == (115, 69, 55):
                            time.sleep(1)
                            tap(adb_path, emulator_address, car_point[c][0], car_point[c][1])
                            time.sleep(1)
                            tap(adb_path, emulator_address, 960, 540)  # ATTACK

        close_app(adb_path, emulator_address, package_name="com.zeptolab.cats.google")
        time.sleep(1)




