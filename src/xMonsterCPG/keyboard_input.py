#! /usr/bin/python3
import rospy
import sys, select, tty, termios
from std_msgs.msg import String

def readchar():
	fd = sys.stdin.fileno()
	old_settings = termios.tcgetattr(fd)
	try:
		tty.setraw(sys.stdin.fileno())
		ch = sys.stdin.read(1)
	finally:
		termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
	return ch

def readkey(getchar_fn=None):
	getchar = getchar_fn or readchar
	c1 = getchar()
	if ord(c1) != 0x1b:
		return c1
	c2 = getchar()
	if ord(c2) != 0x5b:
		return c1
	c3 = getchar()
	return chr(0x10 + ord(c3) - 65)

def talker():
	rospy.init_node('keyboard')
	pub = rospy.Publisher('keys', String, queue_size=1)
	rate = rospy.Rate(100)  # publish rate
	# old_attr = termios.tcgetattr(sys.stdin)
	# tty.setcbreak(sys.stdin.fileno())
	while not rospy.is_shutdown():
		key = readkey()
		pub.publish(key)
		if key.strip() == '':
			# print('bye!')
			break
		# else:
			# print 'You pressed', ch
		rate.sleep()
		# if select.select([sys.stdin], [], [], 0)[0] == [sys.stdin]:
		# 	pub.publish(sys.stdin.read(1))
		# rate.sleep()
	# termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_attr)

if __name__ == '__main__':
	try:
		talker()
	except rospy.ROSInterruptException:
		pass
