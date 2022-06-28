#!/usr/bin/env python3
import serial
import time
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist 

class GeneralControl(Node):

    def __init__(self):
        super().__init__('reel_controller')
        self.publisher_ = self.create_publisher(Twist, 'topic', 10)
        timer_period = 0.5  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
        self.ser.reset_input_buffer()

    def timer_callback(self):
        msg = Twist()
        msg.linear.x = 1.0
        print("select number of seconds")
        self.publisher_.publish(msg)
        self.get_logger().info('Publishing: "%s"' % msg.linear.x)
        flashes = int(input())
        flashes.to_bytes(2, byteorder='big')
        self.ser.write(flashes)
        self.ser.write(b"\n")

def main(args=None):
    rclpy.init(args=args)
    reelController = GeneralControl()
    rclpy.spin(reelController)
    reelController.destroy_node()
    rclpy.shutdown()
    
if __name__ == '__main__':
    main()