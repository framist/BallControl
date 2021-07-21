from machine import UART, Pin
import time
import _thread


from myStepMotor import StepMotor

# uart = UART(1, baudrate=9600, tx=Pin(8), rx=Pin(9))

uart = UART(0, baudrate=9600, tx=Pin(0), rx=Pin(1))
xStepMotor = StepMotor([2,3])
yStepMotor = StepMotor([6,7])
print('start:')

time.sleep(0.1)
r = ''
try:
    while 1:
        rxData = b''
        while uart.any() > 0:
            rxData += uart.read(1)
        if len(rxData)>0:
            print(rxData,end='|')
            r += rxData.decode('utf-8')
            if r[-1] == '\n':
                print('\nreceved:"',r[:-1].split(','),'"\n')
                if r[:-1].split(',')[0] == '0':
                    xStepMotor.改变电机位置(int(r[:-1].split(',')[1]))
                elif r[:-1].split(',')[0] == '1':
                    yStepMotor.改变电机位置(int(r[:-1].split(',')[1]))
                uart.write('receved!\n')
                r = ''
except:
    pass
finally:
    print("protect!stop...")
    xStepMotor.改变电机位置(0)
    yStepMotor.改变电机位置(0)
    
