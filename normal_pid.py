# -*- coding: utf-8 -*- 
""" 
滚球控制系统
framist
""" 

import RPi.GPIO as GPIO
import serial
# opencv支持
import cv2 
import numpy as np 
# 图形处理支持
from imutils.video import VideoStream
from imutils.video import FPS
# 时间支持
import time
# 线程支持
from threading import Thread
# my
from myPID import PID
from myStepMotor import StepMotor



def GPIO_init():
    GPIO_end()
    # 共阴极接法
    # / 脉冲 方向 / 
    # 使用 11 12 / 15 16 
    GPIO.setmode(GPIO.BOARD)

def GPIO_end():
    GPIO.cleanup()

t = None
def T_control(stepMotor: StepMotor,l:int):
    global t
    if t is not None:
        t.join()
    t = Thread(target=stepMotor.改变电机位置,args=(l,))
    t.start()

def ser_control(ser,xy,l:int):
    # 单次限幅
    # l = l if abs(l) < 100 else l//abs(l)*100
    print(f'{xy},{l}\n'.encode('utf-8'))
    ser.write(f',{xy},{l}\n'.encode('utf-8'))
xPID = None
yPID = None
goal_xy = {'x':250,'y':250}
def on_EVENT_LBUTTONDOWN(event, x, y, flags, param):
    global goal_xy
    global xPID
    global yPID
    if event == cv2.EVENT_LBUTTONDOWN:
        goal_xy['x'] = x
        goal_xy['y'] = y
        xPID.renew(goal_xy['x'])
        yPID.renew(goal_xy['y'])
        print(f'mouse check: {goal_xy}')
        
def main():
    GPIO_init()
    global goal_xy
    global xPID
    global yPID
    ser = serial.Serial("/dev/ttyAMA0", 115200)
    
    # xStepMotor = StepMotor([11,12])

    print("[INFO] starting video stream...")
    # vs = VideoStream(src=0, usePiCamera=True,resolution=(480,368)).start()
    vs = VideoStream(src=0, usePiCamera=True,resolution=(656,496)).start()
    time.sleep(1.0)
    

    # 初始化FPS吞吐量估计器
    fps = FPS().start()

    
    try:
        while not cv2.waitKey(1) & 0xFF == ord('q'):
            # 抓取目前帧
            frame = vs.read()
            cimg = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            # circles = cv2.HoughCircles(cimg, cv2.HOUGH_GRADIENT, 1, 1000, param1=80, param2=13, minRadius=6, maxRadius=10)
            circles = cv2.HoughCircles(cimg, cv2.HOUGH_GRADIENT, 1, 1000, param1=80, param2=13, minRadius=11, maxRadius=15)
            
            if circles is not None:
                circles = np.uint16(np.around(circles.astype(np.double), 3))

                for i in circles[0, :]:
                    # draw the outer circle / the center of the circle
                    cv2.circle(cimg, (i[0], i[1]), i[2], (0, 255, 0), 2)
                    cv2.circle(cimg, (i[0], i[1]), 2, (0, 0, 255), 3)

                # -----------控制---------------
                if xPID is None:
                    # xPID = PID(goal_xy['x'],circles[0][0][0],[1,1,0.01,30])
                    xPID = PID(goal_xy['x'],circles[0][0][0],[0.73,1,0.011,9])
                ser_control(ser,0,int(xPID.control(circles[0][0][0])))
                time.sleep(0.02)
                if yPID is None:
                    # yPID = PID(goal_xy['y'],circles[0][0][1],[1,1,0.01,40])
                    yPID = PID(goal_xy['y'],circles[0][0][1],[1,1,0.011,9])
                ser_control(ser,1,int(yPID.control(circles[0][0][1])))

                # T_control(xStepMotor,int(xPID.control(circles[0][0][1])))
            else:
                pass

            # 更新 FPS
            fps.update()
            fps.stop()

            # 帧上的信息集
            cv2.circle(cimg, (goal_xy['x'], goal_xy['y']), 3, (255, 255, 255), thickness = 1)
            info = [
                ("circle", "---" if circles is None else f"{(circles)}"),
                ("FPS", "{:.2f}".format(fps.fps())),
            ]
            for (i, (k, v)) in enumerate(info):
                text = "{}: {}".format(k, v)
                cv2.putText(cimg, text, (10, cimg.shape[0] - ((i * 20) + 20)),
                            cv2.FONT_HERSHEY_PLAIN, 1, (255, 200, 200), 2)

            cv2.imshow("cimg", cimg)
            cv2.setMouseCallback("cimg", on_EVENT_LBUTTONDOWN)
            
    except  Exception as e:
        print(e)
        
    finally:

        # 善后处理：
        print("==自动停止==")
        ser.write(f',-1,0\n'.encode('utf-8'))
        time.sleep(1)
        # xStepMotor.改变电机位置(0)
        # 如果我们使用网络摄像头，释放指针
        vs.stop()
        # 关闭所有窗口
        cv2.destroyAllWindows()
        ser.close()
        GPIO_end()


if __name__ == '__main__':
    main()


"""
dp - 累加器分辨率与图像分辨率的反比。例如，如果 dp = 1，则累加器具有与输入图像相同的分辨率。如果 dp = 2，则累加器的宽度和高度都是一半。
minDist -检测到的圆的中心之间的最小距离。如果参数太小，除了真正的参数外，可能会错误地检测到多个邻居圈。如果太大，可能会错过一些圈子。
param1:此参数是对应Canny边缘检测的最大阈值，最小阈值是此参数的一半 也就是说像素的值大于param1是会检测为边缘
    在CV_HOUGH_GRADIENT的情况下， 两个传递给Canny（）边缘检测器的阈值较高（较小的两个小于两倍）。
param2:它表示在检测阶段圆心的累加器阈值。它越小的话，就可以检测到更多根本不存在的圆，而它越大的话，能通过检测的圆就更加接近完美的圆形了
minRadius - 最小圆半径。
maxRadius - 最大圆半径。
"""
