from machine import UART, Pin
import time
import _thread

from myStepMotor import StepMotor

uart = UART(0, baudrate=115200, tx=Pin(0), rx=Pin(1))
xStepMotor = StepMotor([6,7])
yStepMotor = StepMotor([2,3])
exitFlag = False

tLock = _thread.allocate_lock()

y_g = 0    

def y_control():
    tLock.acquire()
    global y_g
    yStepMotor.改变电机位置(y_g)
    tLock.release()
    _thread.exit()
    
print('====start====')
time.sleep(0.1)

try:
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
                    # yStepMotor.改变电机位置(int(r[:-1].split(',')[-1]))
                    tLock.acquire()
                    y_g = int(r[:-1].split(',')[-1])
                    _thread.start_new_thread(y_control, ())
                    tLock.release()
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
    
