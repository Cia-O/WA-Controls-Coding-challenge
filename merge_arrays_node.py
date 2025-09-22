#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from std_msgs.msg import Int32MultiArray

class MergedArraysNode(Node):
    def __init__(self):
        super().__init__('merged_arrays_node')
        self.array1 = []
        self.array2 = []
        self.subscr1 = self.create_subscription(Int32MultiArray, '/input/array1', self.array1_callback, 10)
        self.subscr2 = self.create_subscription(Int32MultiArray, '/input/array2', self.array2_callback, 10)
        self.pub = self.create_publisher(Int32MultiArray, '/output/array', 10)

    # Call back to array 1
    def array1_callback(self, msg):
        self.array1 = list(msg.data)
        # only publish if the other has data, making sure to work and not give continuous endless output
        if self.array2:
            self.merge_plus_publish()

    # Call back to array2
    def array2_callback(self, msg):
        self.array2 = list(msg.data)
        # trying to publish on when there is data cause i keep getting repeated code
        if self.array1:
            self.merge_plus_publish()


    # merge_plus_publish is defined:
    def merge_plus_publish(self):
        if (not self.array1) or (not self.array2):
            return
        merged = self.array1 + self.array2
        merged.sort()
        msg = Int32MultiArray()
        msg.data = merged
        self.pub.publish(msg)
        self.get_logger().info(f'The two arrays have now been sorted and merged: {merged}')

        # main method defined
def main(args=None):
    rclpy.init(args=args)
    node = MergedArraysNode()


    node.get_logger().info("This is up and running")

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass

    # I know that python automatically destroys the object, but for mysake, i am going to destroy it here.
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
