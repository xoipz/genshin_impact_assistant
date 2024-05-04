import io
import time

import cv2
import numpy as np
import subprocess
import locale
import pygetwindow as gw
from PIL import ImageGrab


def screenshot_size(left, top, right, bottom):
    # 使用PIL的ImageGrab.grab捕获指定区域的截图
    screenshota = ImageGrab.grab(bbox=(left, top, right, bottom))
    # PIL.Image
    # 将PIL.Image对象转换为NumPy数组
    screenshota_np = np.array(screenshota)
    # PIL.Image返回的是RGB格式，转换为OpenCV使用的BGR格式
    screenshota_np = cv2.cvtColor(screenshota_np, cv2.COLOR_RGB2BGR)
    return screenshota_np


def screenshot_specific_window(window_title):
    try:
        # 查找对应标题的窗口
        window = gw.getWindowsWithTitle(window_title)[0]
        if window:
            # window.activate()
            # time.sleep(0.5)
            # 获取窗口的边界
            left, top, right, bottom = window.left, window.top, window.right, window.bottom
            # 使用PIL的ImageGrab.grab捕获指定区域的截图
            screenshota = ImageGrab.grab(bbox=(left, top, right, bottom))
            # PIL.Image

            # 将PIL.Image对象转换为NumPy数组
            screenshota_np = np.array(screenshota)
            # PIL.Image返回的是RGB格式，转换为OpenCV使用的BGR格式
            screenshota_np = cv2.cvtColor(screenshota_np, cv2.COLOR_RGB2BGR)
            return screenshota_np
    except Exception as e:
        # print(f"截图失败: {e}")
        return None


def get_window_size(window_title):
    # 查找对应标题的窗口
    window = gw.getWindowsWithTitle(window_title)[0]
    left, top, right, bottom = window.left, window.top, window.right, window.bottom
    return [left, top]


# 使用示例
# screenshot_specific_window("Notepad")


def is_program_running(program_name):
    try:
        tasklist_output = subprocess.check_output(['tasklist'], shell=True).decode(locale.getpreferredencoding(False))
    except UnicodeDecodeError as e:
        print(f"Error decoding tasklist output: {e}")
        return False

    return program_name in tasklist_output


def focus_on_program(window_title):
    """
    根据窗口标题将焦点设置到该程序。

    Args:
        window_title (str): 目标窗口的标题。

    Returns:
        bool: 如果成功设置焦点返回True，否则返回False。
    """
    try:
        win = gw.getWindowsWithTitle(window_title)[0]  # 获取第一个匹配标题的窗口
        if win is not None:
            win.activate()  # 将焦点设置到窗口
            time.sleep(0.5)
            return True
    except IndexError:
        # 没有找到窗口
        print(f"No window with title '{window_title}' found.")
    except Exception as e:
        # 处理其他可能的错误
        print(f"Error focusing on the program: {e}")

    return False


def wait_for_program(program_name):
    program = False
    while not program:
        time.sleep(2)
        program = is_program_running(program_name)


def is_program_focused(window_title):
    """
    检查具有指定标题的程序是否处于焦点。

    Args:
        window_title (str): 目标窗口的标题。

    Returns:
        bool: 如果目标程序处于焦点，返回True；否则返回False。
    """
    try:
        # 获取当前活动的窗口
        active_win = gw.getActiveWindow()
        # 检查当前活动窗口的标题是否包含目标窗口标题
        if active_win and window_title in active_win.title:
            return True
    except Exception as e:
        # 出现异常时打印错误信息
        print(f"Error checking program focus: {e}")

    return False
