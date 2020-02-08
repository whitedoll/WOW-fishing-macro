import numpy as np
import cv2
import cvui

import win32gui
import win32api
import win32con
import pyautogui
import time
import mss
import math

def callback2(hwnd):
    left, top, x2, y2 = win32gui.GetWindowRect(hwnd)
    # return monitor
    return left + Starting[0], top + 30, area_width[0], area_height[0]


WINDOW_NAME = 'WOW fishing Macro'

state_left = win32api.GetKeyState(0x01)  # Left button down = 0 or 1. Button up = -127 or -128
firstFrame = None

previous_position_y = 10
switch = 0
time_loop = 0
fail_detact = 0
fish_button = 1
success_num = 0
run_button = 1
run_button2 = 1
run_button3 = 0

sensitivity = [2]
start = 0
Starting = [300]
area_width = [300]
area_height = [300]
cap_min = [800]
cap_max = [3000]
previous_www = 0
previous_hhh = 0

program_list = [WINDOW_NAME, WINDOW_NAME]

frame = np.zeros((500, 550, 3), np.uint8)
# frame = np.zeros(imgb.shape, np.uint8)
cvui.init(WINDOW_NAME)
with mss.mss() as sct:

    while True:
        if run_button2 != 0:
            state_switch = win32api.GetKeyState(0x01)
            if state_switch != state_left:  # Button state changed
                state_left = state_switch
                # print(a)
                if state_switch < 0:
                    counttt = 512
                else:
                    hWnd = win32gui.GetForegroundWindow()
                    counttt = 512
                    if win32gui.GetWindowText(hWnd):
                        print(win32gui.GetWindowText(hWnd))
                    program_list.append(win32gui.GetWindowText(hWnd))
                    del program_list[0]
                    print(program_list)

                    left, top, xx, yy = win32gui.GetWindowRect(hWnd)
                    gui_dc = win32gui.GetDC(0)
                    red = win32api.RGB(255, 0, 0)

                    newpen = win32gui.CreatePen(win32con.PS_SOLID, 3, win32api.RGB(255, 0, 0))
                    prevpen = win32gui.SelectObject(gui_dc, newpen)

                    print(left, top, xx, yy)
                    offset = 5

                    win32gui.MoveToEx(gui_dc, left + offset, top)
                    win32gui.LineTo(gui_dc, xx - offset, top)
                    win32gui.LineTo(gui_dc, xx - offset, yy - offset)
                    win32gui.LineTo(gui_dc, left + offset, yy - offset)
                    win32gui.LineTo(gui_dc, left + offset, top)

                    win32gui.ReleaseDC(hWnd, gui_dc)

        frame[:] = (49, 52, 49)
        hwndMain2 = win32gui.FindWindow(None, WINDOW_NAME)

        if run_button == 0:
            run_button2 = 0
            hwndMain = win32gui.FindWindow(None, titlee)
            # hwndMain = win32gui.GetForegroundWindow()
            left2, top2, x22, y22 = win32gui.GetWindowRect(hwndMain)
            if run_button3 == 0:
                # num = 0
                # count = [10]
                Starting = [math.ceil(x22 * (2.6 / 10))]
                area_width = [math.ceil(x22 * (2 / 5))]
                area_height = [math.ceil(y22 * (1 / 3))]
                run_button3 = 1

            if fish_button == 0:
                win32gui.SetForegroundWindow(hwndMain)
                pyautogui.press('1')
                fish_button = 1

            monitor = {"top": int(callback2(hwndMain)[1]), "left": int(callback2(hwndMain)[0]),
                       "width": int(callback2(hwndMain)[2]), "height": int(callback2(hwndMain)[3])}

            printScreen = np.array(sct.grab(monitor))
            www, hhh, iii = printScreen.shape

            size_win = 1
            printScreen2 = cv2.resize(printScreen, None, fx=size_win, fy=size_win)
            printScreen2 = cv2.cvtColor(printScreen2, cv2.COLOR_RGB2GRAY)
            gray = cv2.GaussianBlur(printScreen2, (21, 21), 0)

            if firstFrame is None:
                firstFrame = gray
            if previous_www != www:
                firstFrame = gray
            if previous_hhh != hhh:
                firstFrame = gray
            if start == 0:
                firstFrame = gray
                # continue

            previous_www = www
            previous_hhh = hhh

            frameDelta = cv2.absdiff(firstFrame, gray)
            thresh = cv2.threshold(frameDelta, 30, 255, cv2.THRESH_BINARY)[1]
            kernel = np.ones((8, 8), np.uint8)
            thresh = cv2.dilate(thresh, kernel, iterations=2)
            # print(cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE))
            image, contours, hierarchy = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            # print(contours)
            fail_detact = fail_detact + 1
            # print('fail detact :', fail_detact, ' time_loop :', time_loop)
            if start == 1:
                if fail_detact > 700:
                    # print(fail_detact)
                    time_loop = 0
                    fish_button = 0
                    fail_detact = 0

            for contour in contours:
                rect = cv2.boundingRect(contour)
                area = rect[2] * rect[3]

                cv2.drawContours(printScreen, [contour], 0, (0, 0, 255), 5)

                if cap_max[0] > cv2.contourArea(contour) > cap_min[0]:

                    cv2.drawContours(printScreen, [contour], 0, (0, 255, 0), 2)
                    cv2.drawMarker(printScreen, (contour[0][0][0] + 10, contour[0][0][1] + 15), color=(255, 0, 0),
                                   markerType=cv2.MARKER_CROSS, thickness=2)
                    # print(contour[0][0])

                    current_position_y = contour[0][0][1]
                    diff_position_y = abs(previous_position_y - current_position_y)
                    # print(diff_position_y)
                    previous_position_y = current_position_y

                    thickness = 2
                    fontScale = 1.0
                    org = contour[0][0][0] + 10, contour[0][0][1] + 5
                    org2 = contour[0][0][0] + 10, contour[0][0][1] + 35
                    font = cv2.FONT_HERSHEY_COMPLEX  # hand-writing style font
                    cv2.putText(printScreen, "Y_position:" + str(diff_position_y), org, font, fontScale, (0, 255, 255),
                                thickness, cv2.LINE_AA)
                    cv2.putText(printScreen, "Area:" + str(cv2.contourArea(contour)), org2, font, fontScale,
                                (0, 255, 255),
                                thickness, cv2.LINE_AA)
                    # time.sleep(3)
                    if switch == 0:

                        if 0 <= diff_position_y <= 2:
                            time_loop = time_loop + 1

                            # print(time_loop)
                            if time_loop > 30:
                                switch = 1
                    else:
                        if diff_position_y >= sensitivity[0]:
                            # if diff_position_y >= 3:
                            # print(contour[0][0][0])
                            if start == 1:
                                pyautogui.moveTo(contour[0][0][0] + int(callback2(hwndMain)[0]) + 5,
                                                 contour[0][0][1] + int(callback2(hwndMain)[1]) + 15)
                                pyautogui.click(button='left')

                            switch = 0
                            time.sleep(1.5)
                            if start == 1:
                                pyautogui.moveTo(int(callback2(hwndMain)[0]), int(callback2(hwndMain)[1]))
                            fish_button = 0
                            time_loop = 0
                            fail_detact = 0
                            success_num = success_num + 1
                            print("time_loop", success_num)

            # cvui.text(frame, 10, 15, 'Hello world!')
            if cvui.button(frame, 400, 300, "Start"):
                start = 1
                fish_button = 0
                fail_detact = 0
                # pyautogui.press('1')

            # print('aaaa', start, fish_button, fail_detact)
            if cvui.button(frame, 400, 350, "Stop"):
                start = 0
                fish_button = 1
            # if cvui.button(frame, 300, 80, "&Quit"):
            #     break
            # # cvui.window(frame, 150, 10, 130, 90, str(num))
            #

            printScreen = cv2.resize(printScreen, None, fx=0.7, fy=0.7)
            printScreen = cv2.cvtColor(printScreen, cv2.COLOR_RGB2BGR)
            printScreen = cv2.cvtColor(printScreen, cv2.COLOR_BGR2RGB)
            cvui.image(frame, 20, 20, printScreen)

        if cvui.button(frame, 400, 400, "Select window"):
            if run_button == 0:
                run_button = 1

            if run_button == 1:
                run_button = 0
                titlee = program_list[0]

        if run_button2 == 0:
            cvui.text(frame, 10, 305, "Capture Area")
            cvui.text(frame, 10, 355, "Min Max")

            cvui.text(frame, 100, 285, "Starting")
            cvui.counter(frame, 100, 300, Starting, 10)
            cvui.text(frame, 200, 285, "Width")
            cvui.counter(frame, 200, 300, area_width, 10)
            cvui.text(frame, 300, 285, "Height")
            cvui.counter(frame, 300, 300, area_height, 10)
            cvui.text(frame, 100, 335, "Max")
            cvui.counter(frame, 100, 350, cap_max, 100)
            cvui.text(frame, 200, 335, "Min")
            cvui.counter(frame, 200, 350, cap_min, 100)
            cvui.text(frame, 300, 335, "sensitivity")
            cvui.counter(frame, 300, 350, sensitivity, 1)
            cvui.window(frame, 30, 390, 360, 100, "Log")
            cvui.printf(frame, 50, 420, 0.6, 0xffffff, "Success: %d", success_num)

        # cvui.update()
        # Show window content
        cvui.imshow(WINDOW_NAME, frame)
        visii = win32gui.IsWindowVisible(hwndMain2)
        # print(visii)
        # if cv2.getWindowProperty(WINDOW_NAME, cv2.WND_PROP_AUTOSIZE) is -1:
        #     print(cv2.getWindowProperty(WINDOW_NAME, 1))

        # cv2.waitKey(20)
        if cv2.waitKey(20) == 27 or visii is 0:
            break
            cv2.destroyAllWindows()
            # print("aaa")
        # if visii is 0:
        #     break
        #     cv2.destroyAllWindows()
