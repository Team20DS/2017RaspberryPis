#!/usr/bin/env python
#----------------------------------------------------------------
#       Note:
#               ds18b20's data pin must be connected to pin7.
#               replace the 28-XXXXXXXXX as yours.
#----------------------------------------------------------------
import os
import time

ds18b20 = []

def setup():
        clear = open('/home/pi/Documents/Diagnostics/Log', 'w')
        clear.write('')
        clear.close()
        start = time.time()
        global start
        global ds18b20
        for i in os.listdir('/sys/bus/w1/devices'):
               if i != 'w1_bus_master1':
                       ds18b20.append(i)

def tempOnce():
        retTemp = '*' + str(len(ds18b20)) + '*'
        for i in ds18b20:
                location = '/sys/bus/w1/devices/' + i + '/w1_slave'
                tfile = open(location, 'r')
                text = tfile.read()
                tfile.close()
                secondline = text.split("\n")[1]
                temperaturedata = secondline.split(" ")[9]
                temp = float(temperaturedata[2:])
                temp = temp / 1000
                retTemp += str(temp) + '*'
        logTemp(retTemp)
        print retTemp
        return retTemp
        
def tempLoop():
        while True:
                tempOnce()

def logTemp(retTemp):
        logFile = open('/home/pi/Documents/Diagnostics/Log', 'a')
        sinceStart = round(time.time() - start, 1)
        logFile.write(str(sinceStart) + '\t')
        s = retTemp.split('*')
        for i in range(2, int(s[1]) + 2):
                logFile.write(s[i] + '\t')
        logFile.write('\n')

def destroy():
        pass

if __name__ == '__main__':
        try:
                setup()
                tempLoop()
        except KeyboardInterrupt:
                destroy()
