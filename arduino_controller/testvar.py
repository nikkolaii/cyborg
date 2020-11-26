from pyfirmata import Arduino,util
import time
import sys

board = Arduino('/dev/ttyUSB0') #Check which port your arduino is connecte to!
it = util.Iterator(board)
it.start()
board.analog[0].enable_reporting()
board.analog[1].enable_reporting()
board.analog[2].enable_reporting() # Potentiometer
time.sleep(2)
for i in range(10000):
    time.sleep(0.1)
    x = board.analog[0].read() - 0.5112
    if x <= 0.001 and x>= -0.001:
	x = 0
    if x == 0.4888:
	x = 0.5112

    y = -board.analog[1].read() +0.5112
    if y <= 0.005 and y>= -0.005:
	y = 0
    if y == -0.4888:
	y = 0.5112
    print('y = :', y)
    print(x)
    pot = board.analog[2].read()
    print(pot)
