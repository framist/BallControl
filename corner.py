# opencv支持
import cv2 
import numpy as np 

# 图形处理支持
from imutils.video import VideoStream
from imutils.video import FPS

# 时间支持
import time

import copy

vs = VideoStream(src=0, usePiCamera=True,resolution=(480,368)).start()
time.sleep(1.0)

# 初始化FPS吞吐量估计器
fps = FPS().start()

# 从视频流循环帧
while True:
    # 抓取目前帧
    frame = vs.read()
    (H, W) = frame.shape[:2]

    img = copy.deepcopy(frame)
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

    gray = np.float32(gray)    #将gray转化为float32的输入图像 blocksize=2，ksize=3
    dst = cv2.cornerHarris(gray,20,3,0.04)

    #result is dilated for marking the corners, not important
    dst = cv2.dilate(dst,None)

    # Threshold for an optimal value, it may vary depending on the image　　#将img图像中检测到的角点涂上红色
    img[dst>0.01*dst.max()]=[0,0,255]

    cv2.imshow('cornerHarris',img)

    if cv2.waitKey(0) & 0xff == 27:
        cv2.destroyAllWindows()



    # 更新 FPS
    fps.update()
    fps.stop()
    
    # 初始化我们要显示在帧上的信息集
    info = [
        ("FPS", "{:.2f}".format(fps.fps())),
    ]

    # 遍历信息元组并在帧上绘制它们
    # enumerate函数返回(0, seq[0]), (1, seq[1]), (2, seq[2])...
    for (i, (k, v)) in enumerate(info):
        text = "{}: {}".format(k, v)
        cv2.putText(img, text, (10, H - ((i * 20) + 20)), cv2.FONT_HERSHEY_PLAIN, 1, (255,200,200), 2)


    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


    # 善后处理：
    # 如果我们使用网络摄像头，释放指针
    vs.stop()
    # 关闭所有窗口
    cv2.destroyAllWindows()
