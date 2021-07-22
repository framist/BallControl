from machine import UART, Pin
import time
import _thread

from myStepMotor import StepMotor

# xUart = UART(1, baudrate=9600, tx=Pin(8), rx=Pin(9))
# yUart = UART(0, baudrate=9600, tx=Pin(0), rx=Pin(1))
uart = UART(0, baudrate=9600, tx=Pin(0), rx=Pin(1))
xStepMotor = StepMotor([6,7])
yStepMotor = StepMotor([2,3])
exitFlag = False

# def main_x():
#     # print('X===start====')
#     global xStepMotor
#     global xUart
#     r = ''
#     while 1:
#         rxData = b''
#         while xUart.any() > 0:
#             rxData += xUart.read(1)
#         if len(rxData)>0:
#             # print(rxData,end='|')
#             r += rxData.decode('utf-8')
#             if r[-1] == '\n':
#                 # print('\nX receved:"',r[:-1].split(','),'"\n')
#                 if r[:-1].split(',')[-2] == '0':
#                     xStepMotor.改变电机位置(int(r[:-1].split(',')[-1]))
#                 elif r[:-1].split(',')[-2] == '-1':
#                     break
#                 # xUart.write('receved!\n')
#                 r = ''

# def main_y():
#     print('Y===start====')
#     global yStepMotor
#     global yUart
#     global exitFlag
#     r = ''
#     while not exitFlag:
#         rxData = b''
#         while yUart.any() > 0:
#             rxData += yUart.read(1)
#         if len(rxData)>0:
#             # print(rxData,end='|')
#             r += rxData.decode('utf-8')
#             if r[-1] == '\n':
#                 print('\nY receved:"',r[:-1].split(','),'"\n')
#                 if r[:-1].split(',')[-2] == '1':
#                     yStepMotor.改变电机位置(int(r[:-1].split(',')[-1]))
#                 elif r[:-1].split(',')[-2] == '-1':
#                     break
#                 # yUart.write('receved!\n')
#                 r = ''

x_g = 0
y_g = 0    
def x_control():
    global x_g
    global xStepMotor
    global exitFlag
    while not exitFlag:
        xStepMotor.改变电机位置(x_g)
    

def y_control():
    global y_g
    global yStepMotor
    global exitFlag
    while not exitFlag:
        yStepMotor.改变电机位置(y_g)

print('====start====')
time.sleep(0.1)

try:
    # _thread.start_new_thread(main_y, ())
    # main_x()
    x_g = 0
    y_g = 0 
    # _thread.start_new_thread(y_control, ())
    r = ''
    while 1:
        rxData = b''
        while uart.any() > 0:
            rxData += uart.read(1)
        if len(rxData)>0:
            # print(rxData,end='|')
            r += rxData.decode('utf-8')
            if r[-1] == '\n':
                print('\nX receved:"',r[:-1].split(','),'"\n')
                if r[:-1].split(',')[-2] == '0':
                    xStepMotor.改变电机位置(int(r[:-1].split(',')[-1]))
                elif r[:-1].split(',')[-2] == '1':
                    yStepMotor.改变电机位置(int(r[:-1].split(',')[-1]))
                    # y_g = int(r[:-1].split(',')[-1])
                elif r[:-1].split(',')[-2] == '-1':
                    break
                # uart.write('receved!\n')
                r = ''
except Exception as e: 
    print(e)
finally:
    print("\n====stop====")
    exitFlag = True
    xStepMotor.改变电机位置(0)
    yStepMotor.改变电机位置(0)
    
