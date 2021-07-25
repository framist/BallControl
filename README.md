# 滚球控制系统

主要使用PID控制方法，基于python、opencv，采用树莓派4B、树莓派pico实现的滚球控制系统（2017年电赛B题）

仅个人习作项目，不具参考意义

---

以下是队友简单写写的[项目报告](http://plasmacleaner.top:3000/5Ue_a2IfQc66R0tgktMrCA)：



----
# 电赛国赛训练第二题协作文档


**作品**: 滚球控制系统

**Start Time**: 2021/7/17

**End Time**: 结束时间


---

# 摘要

这是一个以小球为载体，用树莓派控制小球在平板上实现静止或者按照预定轨迹移动的系统。本系统包括树莓派模块、传感器模块、驱动模块、电机模块等。在此滚球系统中，利用摄像头检测小球的位置、MPU6050六轴传感器反馈平板的倾斜程度给单片机，应用PWM调速方法作为动力源、PID为主要控制方法，控制步进电机的切换及转速，从而控制平板不断调整位置以使小球按期望要求动作。

**关键词：**

**Abstract：**

This is a small ball as the carrier, using raspberry pie to control the small ball on the plate to achieve static or move according to the predetermined trajectory. The system includes raspberry pie module, sensor module, drive module, motor module and so on. In this rolling ball system, the camera is used to detect the position of the ball and the mpu6050 six axis sensor is used to feed back the tilt degree of the plate to the single chip microcomputer. PWM speed regulation method is used as the power source and PID is used as the main control method to control the switching and speed of the stepping motor, so as to control the plate to adjust the position continuously so that the ball can act as expected.

**Keywords: PID算法 图像识别 轨迹控制**

# 目录


# 设计方案工作原理

## 预期目标与技术路线

1. 使用摄像头获取小球的位置
2. 用小球的位置给电机驱动反馈
3. 电机驱动改变板面倾角，让小球改变位置

## 技术方案比较分析

（1）电机的选择

**方案1：**   使用舵机，可以用连杆进行传动，效果较好，但是舵机的扭矩不够，而且也难以得到合适的传动轴。

**方案2：**   使用步进电机，可以对斜面的角度进行更精确的调整，但是灵活度和流畅度不如舵机。

综上所述，选择方案2。

（2）小球的选择

**方案1：** 无孔的铁球

**方案2：** 有小孔的球，对小球的运动有一定的干扰

综上所述，选择方案1。



## 系统结构

整体结构图：
![](/uploads/upload_791978ed288190d6c0a5d7cf09acf54f.jpg)








## 树莓派zero配置
[树莓派zero配置](http://plasmacleaner.top:3000/sm-0cI7sR1a-dUUXv0h8vA)



## 电机驱动工作机理
**TB6600步进电机驱动**
[电机驱动说明](http://plasmacleaner.top:3000/lJ80G1OAQpiF9U9_7qQROQ)

## 关键电机驱动接口
![](/uploads/upload_712569d0ebb5e412b62ee6241cbed80c.jpg)








# 系统软件设计分析



## 调试参数


| 现象 | KP      | kI       | KD   | K   |
| ---- | ------- | -------- | ---- | --- |
|      |  |  |  |  |


## 待解决的问题
- [x] 快速反转，之前的控制量还能完成吗？会阻塞gpio口
- [ ] 可以尝试用姿态传感器辅助调平以及过程滞后处理
- [x] 增量式PID初始值设定 (功能还未测试)
- [ ] 新的适用于步进电机的全新算法
- [ ] 


## 系统总体工作流程

```flow
st=>start: 开始
e=>end: 结束
op=>operation: 图像识别获取小球位置
op1=>operation: PDI算法处理
op2=>operation: 驱动电机转动
cond=>condition: 是否到达目标位置?

st->op->op1->op2->cond
cond(yes)->e
cond(no)->op
```

## 关键程序代码



    
# 竞赛工作环境条件

炎热的西安，要注意各种设备尤其步进电机的发热问题

## 设计分析软件环境

Windows10操作系统...


## 配套加工安装工具
打孔机、胶枪、螺丝刀...

## 系统安装与调试


### 仪器组装

组装仪器包括两块50cm*50cm的木板、两个步进电机、万向轴等。	

### 调试方法 

导轨主要用于前期限定在一维状态下的控制算法设计。直流稳压电源在测试期间为步进电机供电。示波器用于探测某接口输出是否正常。


## 软件调试

本程序较大且复杂，因此采用python语言编写，通过不断修改，采用自下而上的调试方法，先调试一维的，再调试整个二维系统。在调试的过程中与图像识别的调试相结合，提高了调试的效率。

## 软硬件联合调试

当软件和硬件的基本功能分别调试后，进行软硬件联合调试及优化。

### 测试结果

按照题目要求，分步测试滚球控制系统的功能。

题目要求 试验次数 成功次数 备注
xx       xx      xx    xx
xx       xx      xx    xx


### 测试分析与结论

板球控制系统虽然是个经典的控制系统，其涉及的知识多且面广，没有想象中那么简单。板球控制系统的硬件的搭架特别耗时耗力，比赛所用到的许多材料不能现场购买。在这四天三夜里，我们队员争分夺秒，在搭架好硬件后开始调试程序，最终把基础部分都较好完成，发挥部分完成了xx，多少有些许遗憾。

经过小组讨论分析，我们认为测试结果主要与硬件条件和程序算法密切相关。底架不够稳定会使摄像头跟着平板摆动而摇晃，再好的程序没有良好的硬件基础也不能很好发挥程序功能。程序的算法很多，只有进行多次修改协调才能找出最利于实现题目要求指标。


# 设计总结

在学校里我们学习到的知识和简单的动手实践，要转化成为社会的生产力还需要一个平台。全国大学生电子设计竞赛给我们提供了一个培养创新、协作和钻研精神的平台，是大学生展现自己、积累经验的舞台。 参加过电子设计竞赛的人，都从中体会到了奋斗的快乐、团队力量的伟大和来自压力的动力。

培训到竞赛是一个漫长的过程，期间心态很重要，会遇到很多问题，比如：做训练时不懂的知识，硬件、软件调不出来，队员之间的矛盾，外界压力等，都需要我们去克服。队员多交流！交流不仅能促进队员们的学习，还能及时发现问题处理问题，利用一切可以提高自己能力的资源。

  对我们而言，知识上的收获重要，精神上的丰收更加可喜。挫折是一份财富，经历是一份拥有。这次电子设计大赛必将成为人生旅途上一个非常美好的回忆！
  
# 参考资料



