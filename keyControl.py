""" 
滚球控制系统-键盘
framist
"""
from typing import NoReturn
import RPi.GPIO as GPIO
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
from multiprocessing import Process
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
def T_test(stepMotor: StepMotor):
    global t
    if t is not None:
        t.join()
    t = Thread(target=stepMotor.发送电机脉冲系列,args=(-500,))
    t.start()
    t.join()
    t = Thread(target=stepMotor.发送电机脉冲系列,args=(500,))
    t.start()

def _test(stepMotor: StepMotor):
    while 1:
        stepMotor.发送电机脉冲系列(+500)
        stepMotor.发送电机脉冲系列(-500)

def control(stepMotor: StepMotor):
    global t
    k = cv2.waitKey(1) & 0xFF
    # stepMotor.发送电机脉冲系列(+500)
    # stepMotor.发送电机脉冲系列(-500)
    if t is not None:
        t.join()
    if k == ord('d'):
        t = Thread(target=stepMotor.发送电机脉冲系列,args=(-30,))
    elif k == ord('e'):
        t = Thread(target=stepMotor.发送电机脉冲系列,args=(+30,))
    elif k == ord('c'):
        # stepMotor.发送电机脉冲系列(-500)
        t = Thread(target=stepMotor.发送电机脉冲系列,args=(-500,))
    elif k == ord('3'):
        # stepMotor.发送电机脉冲系列(+500)
        t = Thread(target=stepMotor.发送电机脉冲系列,args=(+500,))
    else:
        return
    t.start()

def main():
    GPIO_init()
    xStepMotor = StepMotor([11, 12])

    # p = Thread(target=_test,args=(xStepMotor,))
    # p.start()    
    # time.sleep(1)
    
    print("[INFO] starting video stream...")
    vs = VideoStream(src=0, usePiCamera=True, resolution=(480, 368)).start()
    time.sleep(1.0)

    # 初始化FPS吞吐量估计器
    fps = FPS().start()

    try:
        while not cv2.waitKey(1) & 0xFF == ord('q'):
            # time.sleep(0.05)
            # 抓取目前帧
            frame = vs.read()
            cimg = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            circles = cv2.HoughCircles(cimg, cv2.HOUGH_GRADIENT, 1.5, 1000, param1=80, param2=20, minRadius=5, maxRadius=9)
            
            if circles is not None:
                circles = np.uint16(np.around(circles.astype(np.double), 3))

                for i in circles[0, :]:
                    # draw the outer circle / the center of the circle
                    cv2.circle(cimg, (i[0], i[1]), i[2], (0, 255, 0), 2)
                    cv2.circle(cimg, (i[0], i[1]), 2, (0, 0, 255), 3)
                # -----------控制---------------
                
            else:
                pass
            
            control(xStepMotor)
            # T_test(xStepMotor)
            # 更新 FPS
            fps.update()
            fps.stop()

            # 帧上的信息集
            info = [
                ("circle", "---" if circles is None else f"{(circles)}"),
                ("FPS", "{:.2f}".format(fps.fps())),
            ]
            for (i, (k, v)) in enumerate(info):
                text = "{}: {}".format(k, v)
                cv2.putText(cimg, text, (10, cimg.shape[0] - ((i * 20) + 20)),
                            cv2.FONT_HERSHEY_PLAIN, 1, (255, 200, 200), 2)

            cv2.imshow("cimg", cimg)

    except Exception as e:
        print(e)

    finally:
        # 善后处理：
        # p.kill()
    
        print("\n======停止======")
        time.sleep(3)
        xStepMotor.改变电机位置(0)
        # 如果我们使用网络摄像头，释放指针
        vs.stop()
        # 关闭所有窗口
        cv2.destroyAllWindows()

        GPIO_end()



if __name__ == '__main__':
    main()
