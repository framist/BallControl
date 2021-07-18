# _*_ coding:utf-8 _*_

# framist:翻译及增加注释

# 利用cv2跟踪一个物体

# 安装imutils和opencv-contrib-python库

# 命令行使用：
# 摄像头  python track_TLD.py
# 文件    python track_TLD.py --video 目标文件.mp4 --tracker csrt

# 帮助:
# s键选择ROI(region of interest), 再按 SPACE 或 ENTER ; 用 c 键取消选择; q 键退出

# 图形处理支持
from imutils.video import VideoStream
from imutils.video import FPS
import imutils
import cv2

# 命令行支持
import argparse

# 时间支持
import time


# 构造命令行参数解析器并解析参数
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video", type=str,
                help="path to input video file")
ap.add_argument("-t", "--tracker", type=str, default="kcf",
                help="OpenCV object tracker type")
args = vars(ap.parse_args())

# 提取OpenCV版本信息 : 'x.x.x'
# split(".")[:2] : 信息用.分割再取前两个
(major, minor) = cv2.__version__.split(".")[:2]


# 如果 OpenCV 版本 <= 3.2，我们可以使用一个特殊的工厂方法（Factory Function）来创建我们的对象跟踪器
if int(major) == 3 and int(minor) < 3:
    tracker = cv2.Tracker_create(args["tracker"].upper())

# 否则，我们需要明确调用approrpiate对象跟踪构造函数:
else:
    # 初始化一个dict
    # OpenCV对象跟踪器启用
    OPENCV_OBJECT_TRACKERS = {
        "csrt": cv2.TrackerCSRT_create,
        "kcf": cv2.TrackerKCF_create,
        "boosting": cv2.TrackerBoosting_create,
        "mil": cv2.TrackerMIL_create,
        "tld": cv2.TrackerTLD_create,
        "medianflow": cv2.TrackerMedianFlow_create,
        "mosse": cv2.TrackerMOSSE_create
    }

    # 使用OpenCV对象跟踪器对象的dict获取适当的对象跟踪器
    tracker = OPENCV_OBJECT_TRACKERS[args["tracker"]]()



# 如果没有提供视频路径，获取对网络摄像头的引用
if not args.get("video", False):
    print("[INFO] starting video stream...")
    vs = VideoStream(src=0,usePiCamera=True).start()
    time.sleep(1.0)
# 否则，获取对视频文件的引用
else:
    vs = cv2.VideoCapture(args["video"])


# 初始化FPS吞吐量估计器
fps = None
# 初始化要跟踪的对象的边界框坐标
initBB = None


# 从视频流循环帧
while True:
    # 抓取目前帧
    frame = vs.read()
    # 如果是VideoCapture则取frame[1]
    frame = frame[1] if args.get("video", False) else frame

    # 检查是否达到视频尽头 - 循环退出
    if frame is None:
        break

    # 调整帧的大小(这样我们可以更快地处理它)
    frame = imutils.resize(frame, width=500)
    # 并获取帧的尺寸：
    # frame.shape[0]：图像的垂直尺寸（高度）
    # frame.shape[1]：图像的水平尺寸（宽度）
    # frame.shape[2]：图像的通道数。
    (H, W) = frame.shape[:2]

    # 是否正在跟踪一个物体
    if initBB is not None:
        # 获取对象的新边框坐标
        (success, box) = tracker.update(frame)
        # 检查跟踪是否成功
        if success:
            (x, y, w, h) = [int(v) for v in box]
            cv2.rectangle(frame, (x, y), (x + w, y + h),
                          (0, 255, 0), 2)

        # 更新 FPS
        fps.update()
        fps.stop()

        # 初始化我们要显示在帧上的信息集
        info = [
            ("Tracker", args["tracker"]),
            ("Success", "Yes" if success else "No"),
            ("FPS", "{:.2f}".format(fps.fps())),
        ]

        # 遍历信息元组并在帧上绘制它们
        # enumerate函数返回(0, seq[0]), (1, seq[1]), (2, seq[2])...
        for (i, (k, v)) in enumerate(info):
            text = "{}: {}".format(k, v)
            cv2.putText(frame, text, (10, H - ((i * 20) + 20)), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
    
    # imshow函数在指定的窗口中显示图像
    cv2.imshow("Frame", frame)

    # 读入按键，延迟1毫秒
    # 0xFF是一个位掩码，它将左边的24位设置为0。因为ord()在0和255之间返回一个值。
    key = cv2.waitKey(1) & 0xFF

    # 如果按下“s”键，我们将绘制一个包围框去跟踪
    if key == ord("s"):
        # 选择要跟踪的对象的边界框(确保在选择ROI后按ENTER或SPACE)
        initBB = cv2.selectROI("Frame", frame, fromCenter=False, showCrosshair=True)
        # 提供边界框坐标启动OpenCV对象跟踪器，然后启动FPS
        tracker.init(frame, initBB)
        fps = FPS().start()
    
    # q键退出
    elif key == ord("q"):
        break

# 善后处理：
# 如果我们使用网络摄像头，释放指针
if not args.get("video", False):
    vs.stop()
# 否则释放文件指针
else:
    vs.release()
# 关闭所有窗口
cv2.destroyAllWindows()

