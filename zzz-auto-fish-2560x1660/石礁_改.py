"""
基于图像识别的绝区零赛博钓鱼脚本
Author:     SmallHappyJerry
Version:    v1.0
Date:       2025-2-20
"""

from queue import Queue
import pygetwindow as gw
import pyautogui
import cv2
import numpy as np
from PIL import Image
import time
import pydirectinput
import threading
from pynput import keyboard
import sys, time, ctypes
from random import random

INTERVAL = 0.01
EXIT_KEY = keyboard.Key.esc
SWITCH_KEY = keyboard.KeyCode.from_char("k")

running = False
xoffset=0
yoffset=0
DEBUG_MODE = False  # 调试模式开关

# 查找窗口
def find_window(window_name):
    windows = gw.getWindowsWithTitle(window_name)
    if windows:
        return windows[0]  # 返回找到的第一个窗口
    else:
        print(f"窗口'{window_name}'未找到")
        return None

# 截取指定区域的截图（减少频繁截图）
def capture_window_area(window, left, top, right, bottom):
    # 获取窗口的屏幕坐标
    window_left, window_top = window.topleft
    # 调整截图区域的坐标
    window_left += xoffset
    window_top += yoffset
    capture_area = (window_left + left, window_top + top,  right - left,  bottom - top)
    
    # 截图
    screenshot = pyautogui.screenshot(region=capture_area)
    return np.array(screenshot)
def save_image(image, file_path):
    image.save(file_path)

# 预加载并缓存模板图像
def load_templates():
    templates = {
        'fish': cv2.cvtColor(cv2.imread('images/yuanhaif.png'), cv2.COLOR_BGR2GRAY),
        'hand': cv2.cvtColor(cv2.imread('images/yuanshou.png'), cv2.COLOR_BGR2GRAY),
        'rightshort': cv2.cvtColor(cv2.imread('images/rightshort1.png'), cv2.COLOR_BGR2GRAY),
        'rightlong': cv2.cvtColor(cv2.imread('images/rightlong1.png'), cv2.COLOR_BGR2GRAY),
        'leftshort': cv2.cvtColor(cv2.imread('images/leftshort1.png'), cv2.COLOR_BGR2GRAY),
        'leftlong': cv2.cvtColor(cv2.imread('images/leftlong1.png'), cv2.COLOR_BGR2GRAY)
    }
    return templates

# 模板匹配
def match_template(screenshot, template):
    # 转为灰度图
    screenshot_gray = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)
    # 使用已经转换为灰度的模板
    result = cv2.matchTemplate(screenshot_gray, template, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    return max_val, max_loc

# 优化的快速连点函数
def rapid_click(key, times, interval_range=(0.06, 0.11)):
    """
    优化的连点函数，使用随机间隔时间
    :param key: 要按下的按键
    :param times: 连点次数
    :param interval_range: 间隔时间范围（秒），默认60-110ms
    """
    for _ in range(times):
        pydirectinput.press(key)
        # 生成60-110ms之间的随机延迟
        random_delay = interval_range[0] + random() * (interval_range[1] - interval_range[0])
        time.sleep(random_delay)

def display_screenshots(screenshot1, screenshot2, screenshot3):
    # 创建一个空白图像用于显示三个截图
    combined_image = np.zeros((max(screenshot1.shape[0], screenshot2.shape[0], screenshot3.shape[0]), 
                               screenshot1.shape[1] + screenshot2.shape[1] + screenshot3.shape[1], 3), dtype=np.uint8)

    # 将三个截图拼接到一起
    combined_image[:screenshot1.shape[0], :screenshot1.shape[1]] = screenshot1
    combined_image[:screenshot2.shape[0], screenshot1.shape[1]:screenshot1.shape[1] + screenshot2.shape[1]] = screenshot2
    combined_image[:screenshot3.shape[0], screenshot1.shape[1] + screenshot2.shape[1]:] = screenshot3

    # 标注名称
    cv2.putText(combined_image, "1", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
    cv2.putText(combined_image, "2", (screenshot1.shape[1] + 10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
    cv2.putText(combined_image, "3", (screenshot1.shape[1] + screenshot2.shape[1] + 10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)

    # 显示拼接后的图像
    cv2.imshow("Combined Screenshot", combined_image)
    cv2.waitKey(1)  # 等待1毫秒，以便窗口刷新

# 主程序
def mainloop(argsQueue):
    window_name = "绝区零"
    window = find_window(window_name)
    
    if window:
        window.activate()
        templates = load_templates()  # 预加载模板
        
        # 设置区域
        regions = {
            'fishing': (2000, 1150, 2250, 1350),
            'right': (1635, 510, 1710, 550),
            'left': (1535, 513, 1611, 555)
        }
        
        
            # 'fishing': (2000, 1150, 2250, 1350),
            # 'right': (1540, 510, 1710, 550),
            # 'left': (1535, 510, 1615, 550)
        num = 0
        f1 = templates['fish']
        pauseFlag = False
        while True:
            if not argsQueue.empty():
                if argsQueue.get() == "switch pause":
                    pauseFlag = not pauseFlag
            if not pauseFlag:
                continue
        
            # 批量截图
            screenshots = {
                'fishing': capture_window_area(window, *regions['fishing']),
                'right': capture_window_area(window, *regions['right']),
                'left': capture_window_area(window, *regions['left'])
            }
            # 显示截图
            display_screenshots(screenshots['fishing'], screenshots['left'], screenshots['right'])
            # 钓鱼判定
            max_val, _ = match_template(screenshots['fishing'], f1)
            
            if max_val > 0.97:
                pydirectinput.press('f')
                time.sleep(0.8)  # 优化延迟时间
                f1 = templates['hand'] if num == 0 else templates['fish']
                num = 1 - num

            # 优化的方向判定
            right_vals = {
                'short': match_template(screenshots['right'], templates['rightshort'])[0],
                'long': match_template(screenshots['right'], templates['rightlong'])[0]
            }
            
            left_vals = {
                'short': match_template(screenshots['left'], templates['leftshort'])[0],
                'long': match_template(screenshots['left'], templates['leftlong'])[0]
            }

            # 处理方向输入
            if right_vals['short'] > 0.6:
                rapid_click('d', 8)  # 使用默认的60-110ms间隔
                pydirectinput.press('space')
            elif right_vals['long'] > 0.6:
                pydirectinput.keyDown('d')
                time.sleep(1.5)  # 优化长按时间
                pydirectinput.keyUp('d')
                pydirectinput.press('space')
            elif left_vals['short'] > 0.4:
                rapid_click('a', 8)  # 使用默认的60-110ms间隔
                pydirectinput.press('space')
            elif left_vals['long'] > 0.4:
                pydirectinput.keyDown('a')
                time.sleep(1.5)
                pydirectinput.keyUp('a')
                pydirectinput.press('space')

            if window.isActive:
                pydirectinput.click(x=window.left + 2000, y=window.top + 900)

            # 仅在调试模式下保存截图
            if DEBUG_MODE:
                for name, screenshot in screenshots.items():
                    screenshot_pil = Image.fromarray(screenshot)
                    save_image(screenshot_pil, f"images/screenshot_{name}.png")

def toggle_running(key,argsQueue):
    
    if key == SWITCH_KEY:
        argsQueue.put("switch pause")

def mymain():
    argsQueue = Queue()
    listener = keyboard.Listener(on_press=lambda key: toggle_running(key, argsQueue))
    listener.start()

    # 启动线程运行主程序
    thread = threading.Thread(target=mainloop,args=(argsQueue,))
    thread.daemon = True
    thread.start()

    print(f"按{SWITCH_KEY}启动或停止钓鱼功能，在其他应用中也可以使用。")
    print(f"按{EXIT_KEY}退出程序。")

    # 保持主线程运行直到按下Esc键
    with keyboard.Listener(on_press=lambda key: key != EXIT_KEY) as esc_listener:
        esc_listener.join()

if __name__ == '__main__':
    # 判断当前进程是否以管理员权限运行
    if ctypes.windll.shell32.IsUserAnAdmin():
        mymain()

    else:
        print('当前不是管理员权限，以管理员权限启动新进程...')
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)
