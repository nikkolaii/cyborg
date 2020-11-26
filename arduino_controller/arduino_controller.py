#!/usr/bin/env python
from pyfirmata import Arduino,util
import time
import sys
import rospy
from geometry_msgs.msg import Twist


def talker():
    pub = rospy.Publisher('/move_base/cmd_vel', Twist, queue_size=10)
    rospy.init_node('Arduino_controller', anonymous=False)


    board = Arduino('/dev/ttyUSB0') #Check which port the arduino is connected to!
    it = util.Iterator(board)
    it.start()
    board.analog[0].enable_reporting()
    board.analog[1].enable_reporting()
    board.analog[2].enable_reporting()
    com = Twist()
# A delay must be added to give the arduino enough time to output the signal from the controller.
# Otherwise, the first values the script recieves are of type NONE which will cause the program to fail.
    rospy.sleep(2)
    rate = rospy.Rate(40) # 40hz
    while not rospy.is_shutdown():
	# Linear velocity
	x_vel = board.analog[0].read() - 0.5112 # Makes the controller input 0 when idle
	speed = board.analog[2].read()*1.5 # Potentiometer 
	com.linear.x = x_vel*speed
	if com.linear.x >=-0.1 and com.linear.x <= 0.1:
		com.linear.x = 0
	if com.linear.x <=-0.2:
		com.linear.x = -0.2
	com.linear.y = 0
	com.linear.z = 0
        # Angular velocity
	z_rot = -board.analog[1].read() + 0.5112
	com.angular.x = 0
	com.angular.y = 0

	com.angular.z = z_rot*1.5
	if com.angular.z >=-0.1 and com.angular.z <= 0.1:
		com.angular.z = 0
	print('x = :',x_vel)
	print('z = ',z_rot)
        pub.publish(com)
	rate.sleep()
if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass
