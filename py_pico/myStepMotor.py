# import RPi.GPIO as GPIO
import time
import utime
from machine import Pin

class StepMotor:
    sum = 0  # 步进电机总个数
    protectMaxLoaction = 1300

    def __init__(self, GPIOused=[6,7]) -> None:
        self.loaction = 0           # +-整数
        self.direction = 0          # 0/1 1:电机位置增加
        self.GPIOused = GPIOused    # 脉冲,方向

        # GPIO.setup(GPIOused, GPIO.OUT, initial=0)
        self.脉冲pin = Pin(GPIOused[0],Pin.OUT,Pin.PULL_DOWN)
        self.方向pin = Pin(GPIOused[1],Pin.OUT,Pin.PULL_UP)
        self.changeDirection(self.direction)
        StepMotor.sum += 1
        print("init StepMotor success!; sum = ",StepMotor.sum)

    def changeDirection(self, d) -> None:
        self.方向pin.value(d)
        # GPIO.output(self.GPIOused[1], d)
        self.direction = d
        utime.sleep_us(5000)  # >= 5e-6

    def 电机脉冲(self):
        self.脉冲pin.value(1)
        utime.sleep_us(500)  # >= 1.2e-6
        self.脉冲pin.value(0)
        utime.sleep_us(250)
        
    def 改变电机位置(self, l):  # 一路
        d = 1 if l-self.loaction > 0 else 0
        if d == self.direction:
            # print("D:",self.direction,'l:',self.loaction)
            pass
        else:
            self.changeDirection(1-self.direction)
            # print("changeD:",self.direction,'l:',self.loaction)

        for _ in range(abs(self.loaction-l)):
            self.loaction += d*2-1
            self.电机脉冲()
            self.checkProtect()
        self.loaction = l

    def 发送电机脉冲系列(self, 正负脉冲数):  # +-
        d = 1 if 正负脉冲数 > 0 else 0
        if d == self.direction:
            # print("D:",self.direction,'l:',self.loaction)
            pass
        else:
            self.changeDirection(1-self.direction)
            # print("changeD:",self.direction,'l:',self.loaction)

        for _ in range(abs(正负脉冲数)):
            self.loaction += d*2-1
            self.电机脉冲()
            self.checkProtect()

    def checkProtect(self):
        if abs(self.loaction) > StepMotor.protectMaxLoaction:
            pass
            #print('\nprotect!')
            #raise Exception("protectMaxLoaction")



if __name__ == '__main__':
    pass
    xstepMotor = StepMotor([2,3])
    ystepMotor = StepMotor([6,7])
    try:
        pass
        # while True:
            # xstepMotor.发送电机脉冲系列(200)
            # ystepMotor.发送电机脉冲系列(200)
            # ystepMotor.发送电机脉冲系列(-200)
    except:
        pass
    finally:
        pass
    xstepMotor.改变电机位置(100)
    xstepMotor.改变电机位置(-100)
    xstepMotor.改变电机位置(0)
    ystepMotor.改变电机位置(100)
    ystepMotor.改变电机位置(-100)
    ystepMotor.改变电机位置(0)
#     stepMotor.发送电机脉冲系列(-300)
#     stepMotor.发送电机脉冲系列(300)


