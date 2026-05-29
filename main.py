import bluetooth
from ble_uart_peripheral import BLEUART
from machine import Pin, PWM, ADC
import time
from MPU6050 import MPU6050

angle=0
mpu = MPU6050()
led17=Pin(17, Pin.OUT) 
led16=Pin(16, Pin.OUT)
pwm=PWM(Pin(18,Pin.OUT),10000)
led16.value(1)
pwm.duty(0)

led=Pin(32, Pin.OUT)
led1=Pin(33, Pin.OUT)
compteur=0
top=0
top1=0
sens=1
duree=20
adc=ADC(34)

ble = bluetooth.BLE()
uart = BLEUART(ble)

def on_rx():
    uart_in = uart.read()
    print("UART IN: ", uart_in.decode().strip())
    if uart_in=='a':
       led17.value(0) 
    elif uart_in=='b': 
       led17.value(1) 
    elif uart_in=='d': 
       led16.value(0) 
    elif uart_in=='f':
       led16.value(1)
    elif uart_in=='z':
       global compteur
       compteur=0
    else:
        chaine=uart_in[1:-1]
        print(chaine)
        pwm.duty(int(chaine))
    
uart.irq(handler=on_rx)

def env_tx(val_tx):
    uart.write(str(val_tx))
    #print("tx", val_tx)
    
while True:
    pot = adc.read()
    if pot > 1900:
        led.value(1)
        if top == 0:
            if sens==1:
                compteur+=1
                #x=x+2.4*cos(3.14)
                #y=y+2.4*sin(3.14)
                sens=2
            top=1
    if pot < 1900: 
        led.value(0)
        top=0
    if pot < 1600:
        led1.value(1)
        if top1 == 0:
            if sens==2:
                compteur+=1
                #x=x+2.4*cos(3.14)
                #y=y+2.4*sin(3.14)
                sens=1
            top1=1
    if pot > 1600:
        led1.value(0)
        top1=0

    

    gyro = mpu.read_gyro_data()  
    gZ = gyro["z"]-2.136
    angle=angle+gZ*duree/1000
    #print(angle)
    if angle > 1:
        led.value(1)
        led1.value(0)
        #angle=0
    elif angle < -1 :
        led.value(0)
        led1.value(1)
        #angle=0
    else:
        led.value(0)
    led1.value(0)
    
    
    
    data=str(pot)+','+str(compteur)+','+str(round(angle,2))
    #data="q"+','+"x"+','+"k"+','+"v"+','+"r"
    env_tx(data)
    time.sleep_ms(duree)

uart.close()
