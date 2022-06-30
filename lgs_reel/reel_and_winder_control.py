#!/usr/bin/env python3
import serial
import time
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist 
from std_msgs.msg import Int16

class GeneralControl(Node):

    def __init__(self):
        super().__init__('reel_winder_ctrl')
        self.publisher_   = self.create_publisher(Twist, 'cmd_vel', 10)
        self.subscription = self.create_subscription(Int16, 'reel_cmd', self.listener_cb,1)
        self.ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
        self.ser.reset_input_buffer()
                
    def listener_cb(self, msg):
        self.get_logger().info('Processing reel_cmd "%s"' % msg.data)
        cmd_vel_msg = Twist()
        cmd_vel_msg.linear.x = float(msg.data)
        self.publisher_.publish(cmd_vel_msg)
        self.get_logger().info('Publishing: "%s"' % cmd_vel_msg.linear.x)
        t_units_abs = abs(msg.data)
        t_units_abs.to_bytes(2, byteorder='big')
        self.ser.write(t_units_abs)
        self.ser.write(b"\n")

def main(args=None):
    rclpy.init(args=args)
    reelController = GeneralControl()
    rclpy.spin(reelController)
    reelController.destroy_node()
    rclpy.shutdown()
    
if __name__ == '__main__':
    main()