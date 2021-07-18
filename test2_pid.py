# -*- coding: utf-8 -*- 
""" 
滚球控制系统
framist
""" 
from numbers import Number
import RPi.GPIO as GPIO


# opencv支持
import cv2 
import numpy as np 

# 图形处理支持
from imutils.video import VideoStream
from imutils.video import FPS

# 时间支持
import time

import copy

# 控制方向
电机方向 = [0,0] # 0/1 1:电机位置增加
电机位置 = [0,0] # +-整数
电机GPIO = [[11,12],[15,16]] # 脉冲,方向 

def 改变电机方向(电机, 方向):
    GPIO.output(电机GPIO[电机][1], 方向)
    电机方向[电机] = 方向
    time.sleep(20e-6) # >= 5e-6

def 电机脉冲(电机):
    GPIO.output(电机GPIO[电机][0],1)
    time.sleep(0.3e-3) # >= 1.2e-6
    GPIO.output(电机GPIO[电机][0],0)
    time.sleep(0.3e-3)


def 改变电机位置(电机, 目标位置): # 一路
    d = 1 if 目标位置-电机位置[电机] > 0 else 0
    if d == 电机方向[电机]:
        print("保留方向：",电机方向)
        pass
    else:
        改变电机方向(电机, 1-电机方向[电机])
        print("改变方向：",电机方向)

    for _ in range(abs(电机位置[电机]-目标位置)):
        电机脉冲(电机)
    电机位置[电机]=目标位置
    

def 发送电机脉冲(电机, 脉冲数): # +-
    d = 1 if 脉冲数 > 0 else 0
    if d == 电机方向[电机]:
        print("保留方向：",电机方向)
        pass
    else:
        改变电机方向(电机, 1-电机方向[电机])
        print("改变方向：",电机方向)

    for _ in range(abs(脉冲数)):
        电机脉冲(电机)
    电机位置[电机]=电机位置[电机]+脉冲数
    assert abs(电机位置[电机]) < 2000

pjs = 0
def GPIO_test():
    
    
    time.sleep(0.5)

def GPIO_init():
    GPIO_end()
    # 共阴极接法
    # / 脉冲 方向 / 
    # 使用 11 12 / 15 16 
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup([i for j in 电机GPIO for i in j], GPIO.OUT, initial=0)
    


def GPIO_end():
    GPIO.cleanup()

def PID_control():

    pass


def PID_control_plus(x1: int, x2: int, x3: int, goal: int, KPID: list) -> float:
    last_last_err = x1 - goal
    last_err = x2 - goal
    now_err = x3 - goal
    
    KP, KI, KD = KPID
    change_val = KP * (now_err - last_err) + KI * now_err + KD * (now_err - 2 * last_err + last_last_err)
    print("change_val:",change_val)
    return change_val

x1,x2,x3 = None,None,None
def control_x(x,goal):
    global x1,x2,x3
    x3 = x
    if x1 or x2 is None:
        x1,x2,x3 = goal,goal,x
    else:
        x2 = x3
        x1 = x2
    K=10#用k来调整体比例
    # change_val = PID_control_plus(x1,x2,x3,200,[0.35987*K,0.020534*K,0.2767*K])
    change_val = PID_control_plus(x1,x2,x3,150,[0.35987*K,0*K,0*K])
    发送电机脉冲(0,int(change_val))

def main():
    GPIO_init()
    # GPIO_test()
    print("[INFO] starting video stream...")
    vs = VideoStream(src=0, usePiCamera=True,resolution=(480,368)).start()
    time.sleep(1.0)


    # 初始化FPS吞吐量估计器
    fps = FPS().start()

    
    try:

        # 从视频流循环帧
        while True:
            # 抓取目前帧
            frame = vs.read()

            # 并获取帧的尺寸：
            # frame.shape[0]：图像的垂直尺寸（高度）
            # frame.shape[1]：图像的水平尺寸（宽度）
            # frame.shape[2]：图像的通道数。
            (H, W) = frame.shape[:2]

            
            cimg = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
            """
            dp - 累加器分辨率与图像分辨率的反比。例如，如果 dp = 1，则累加器具有与输入图像相同的分辨率。如果 dp = 2，则累加器的宽度和高度都是一半。
            minDist -检测到的圆的中心之间的最小距离。如果参数太小，除了真正的参数外，可能会错误地检测到多个邻居圈。如果太大，可能会错过一些圈子。
            param1:此参数是对应Canny边缘检测的最大阈值，最小阈值是此参数的一半 也就是说像素的值大于param1是会检测为边缘
                在CV_HOUGH_GRADIENT的情况下， 两个传递给Canny（）边缘检测器的阈值较高（较小的两个小于两倍）。
            param2:它表示在检测阶段圆心的累加器阈值。它越小的话，就可以检测到更多根本不存在的圆，而它越大的话，能通过检测的圆就更加接近完美的圆形了
            minRadius - 最小圆半径。
            maxRadius - 最大圆半径。
            """
            circles = cv2.HoughCircles(cimg, cv2.HOUGH_GRADIENT, 1.5, 1000,param1=80,param2=20,minRadius=5,maxRadius=8)
            # (GrayImage,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,   cv2.THRESH_BINARY,3,5)
            if circles is not None:
                circles = np.uint16(np.around(circles.astype(np.double),3))

                for i in circles[0,:]:
                    # draw the outer circle
                    cv2.circle(cimg,(i[0],i[1]),i[2],(0,255,0),2)
                    # draw the center of the circle
                    cv2.circle(cimg,(i[0],i[1]),2,(0,0,255),3)
                # -----------控制
                control_x(circles[0][0][1])
            else:
                pass  


            # 更新 FPS
            fps.update()
            fps.stop()
            
            # 初始化我们要显示在帧上的信息集
            info = [
                ("circle", "---" if circles is None  else f"{(circles)}"),
                ("FPS", "{:.2f}".format(fps.fps())),
            ]

            # 遍历信息元组并在帧上绘制它们
            # enumerate函数返回(0, seq[0]), (1, seq[1]), (2, seq[2])...
            for (i, (k, v)) in enumerate(info):
                text = "{}: {}".format(k, v)
                cv2.putText(cimg, text, (10, H - ((i * 20) + 20)), cv2.FONT_HERSHEY_PLAIN, 1, (255,200,200), 2)
            

            cv2.imshow("Frame", cimg)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

            # GPIO_test()
    except:
        pass
    finally:

        # 善后处理：
        print("==自动停止==")
        time.sleep(3)
        改变电机位置(0, 0)
        # 如果我们使用网络摄像头，释放指针
        vs.stop()
        # 关闭所有窗口
        cv2.destroyAllWindows()

        GPIO_end()


if __name__ == '__main__':
    main()