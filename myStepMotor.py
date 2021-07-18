import RPi.GPIO as GPIO
import time


class StepMotor:
    sum = 0  # 步进电机总个数
    protectMaxLoaction = 1300

    def __init__(self, GPIOused=[11, 12]) -> None:
        self.loaction = 0           # +-整数
        self.direction = 0          # 0/1 1:电机位置增加
        self.GPIOused = GPIOused    # 脉冲,方向

        GPIO.setup(GPIOused, GPIO.OUT, initial=0)
        StepMotor.sum += 1

    def changeDirection(self, d) -> None:
        GPIO.output(self.GPIOused[1], d)
        self.direction = d
        time.sleep(20e-6)  # >= 5e-6

    def 电机脉冲(self):
        GPIO.output(self.GPIOused[0], 1)
        time.sleep(0.3e-3)  # >= 1.2e-6
        GPIO.output(self.GPIOused[0], 0)
        time.sleep(0.3e-3)

    def 改变电机位置(self, l):  # 一路
        d = 1 if l-self.loaction > 0 else 0
        if d == self.direction:
            print("保留方向：", self.loaction)
            pass
        else:
            self.changeDirection(1-self.direction)
            print("改变方向：", self.loaction)

        for _ in range(abs(self.loaction-l)):
            self.loaction += d*2-1
            self.电机脉冲()
            self.checkProtect()
        self.loaction = l

    def 发送电机脉冲系列(self, 脉冲数):  # +-
        d = 1 if 脉冲数 > 0 else 0
        if d == self.direction:
            # print("保留方向：",电机方向)
            pass
        else:
            self.changeDirection(1-self.direction)
            # print("改变方向：",电机方向)

        for _ in range(abs(脉冲数)):
            self.loaction += d*2-1
            self.电机脉冲()
            self.checkProtect()

    def checkProtect(self):
        if abs(self.loaction) > StepMotor.protectMaxLoaction:
            raise Exception("protectMaxLoaction")


if __name__ == '__main__':
    GPIO.cleanup()
    GPIO.setmode(GPIO.BOARD)

    xStepMotor = StepMotor([11, 12])
    xStepMotor.改变电机位置(500)
    xStepMotor.改变电机位置(-500)
    xStepMotor.改变电机位置(0)

    GPIO.cleanup()

# # 控制方向
# 电机方向 = [0,0] # 0/1 1:电机位置增加
# 电机位置 = [0,0] # +-整数
# 电机GPIO = [[11,12],[15,16]] # 脉冲,方向

# def 改变电机方向(电机, 方向):
#     GPIO.output(电机GPIO[电机][1], 方向)
#     电机方向[电机] = 方向
#     time.sleep(20e-6) # >= 5e-6

# def 电机脉冲(电机):
#     GPIO.output(电机GPIO[电机][0],1)
#     time.sleep(0.3e-3) # >= 1.2e-6
#     GPIO.output(电机GPIO[电机][0],0)
#     time.sleep(0.3e-3)


# def 改变电机位置(电机, 目标位置): # 一路
#     d = 1 if 目标位置-电机位置[电机] > 0 else 0
#     if d == 电机方向[电机]:
#         print("保留方向：",电机方向)
#         pass
#     else:
#         改变电机方向(电机, 1-电机方向[电机])
#         print("改变方向：",电机方向)

#     for _ in range(abs(电机位置[电机]-目标位置)):
#         电机脉冲(电机)
#     电机位置[电机]=目标位置


# def 发送电机脉冲(电机, 脉冲数): # +-
#     d = 1 if 脉冲数 > 0 else 0
#     if d == 电机方向[电机]:
#         # print("保留方向：",电机方向)
#         pass
#     else:
#         改变电机方向(电机, 1-电机方向[电机])
#         # print("改变方向：",电机方向)

#     for _ in range(abs(脉冲数)):
#         电机脉冲(电机)
#         电机位置[电机] += d*2-1
#         assert abs(电机位置[电机]) < 1200
