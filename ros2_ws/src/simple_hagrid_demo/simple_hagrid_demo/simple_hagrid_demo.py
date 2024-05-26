# useful stuff https://docs.ros.org/en/eloquent/Tutorials/Writing-A-Simple-Py-Publisher-And-Subscriber.html
# hagrid@tablebot:~/ros2_ws/src/simple_hagrid_demo/simple_hagrid_demo$ python3 simple_hagrid_demo.py 
# sudo docker run -it --rm --net=host microros/micro-ros-agent:iron udp4 --port 8888

import rclpy
from rclpy.node import Node

from std_msgs.msg import Byte
from std_msgs.msg import Float32
from std_msgs.msg import Int32

from geometry_msgs.msg import Twist

from example_interfaces.msg import Bool

class SimpleHagridDemo(Node):
    def __init__(self):
        super().__init__('simple_hagrid_demo')
        self.cmd_vel_publisher=self.create_publisher(Twist,'rcm/cmd_vel',1)
        self.enable_publisher=self.create_publisher(Bool,'rcm/enabled',1)

        self.batterySubscription=self.create_subscription(Float32,'rcm/battery',self.battery_callback,1)
        self.batterySubscription # prevent warning

        self.loop_time_period=1.0/10.0
        self.loop_timer=self.create_timer(self.loop_time_period,self.loop)
        self.time=0.0

    def battery_callback(self, msg):
        self.get_logger().info('battery voltage "%d"' % msg.data)
    
    def loop(self):
        self.time=self.time+self.loop_time_period

        self.get_logger().info("time: %d"%(self.time))

        enableMsg=Bool()
        enableMsg.data=True
        self.enable_publisher.publish(enableMsg)

        velocityMsg=Twist()
        velocityMsg.linear.z=0.0
        velocityMsg.angular.x=0.0
        velocityMsg.angular.y=0.0
        velocityMsg.linear.y=0.0
        velocityMsg.angular.z=0.0
        velocityMsg.linear.x=0.0
        if self.time>=2 and self.time<4:
            velocityMsg.linear.x=0.5
        if self.time>=4 and self.time<7:
            velocityMsg.linear.x=0.0
        if self.time>=7 and self.time<9:
            velocityMsg.linear.x=-0.5
        if self.time>=9:
            velocityMsg.linear.x=0.0
        self.cmd_vel_publisher.publish(velocityMsg)
        

def main(args=None):
    rclpy.init(args=args)

    simple_hagrid_demo=SimpleHagridDemo()

    rclpy.spin(simple_hagrid_demo)

    simple_hagrid_demo.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
