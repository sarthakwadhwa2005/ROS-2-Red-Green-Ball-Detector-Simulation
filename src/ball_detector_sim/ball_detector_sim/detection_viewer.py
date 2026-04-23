#!/usr/bin/env python3
import json
import rclpy
from rclpy.node import Node
from std_msgs.msg import String


class DetectionViewer(Node):
    def __init__(self) -> None:
        super().__init__('detection_viewer')
        self.sub = self.create_subscription(
            String, '/ball_detector/detections', self.on_detection, 10
        )
        self.get_logger().info('Detection Viewer started. Listening for detections...')

    def on_detection(self, msg: String) -> None:
        try:
            data = json.loads(msg.data)
            print('\n' + '='*80)
            print(f"Frame: {data.get('frame_id', 'N/A')} | Timestamp: {data['stamp_sec']}.{data['stamp_nanosec']}")
            print(f"Total Detections: {data['count']}")
            print('='*80)
            
            for i, det in enumerate(data['detections'], 1):
                print(f"\n[Detection {i}]")
                print(f"  Color:       {det['color']}")
                print(f"  Position:    x={det['x']}, y={det['y']}")
                print(f"  Radius:      {det['radius']}")
                print(f"  Area:        {det['area']}")
                print(f"  Circularity: {det['circularity']}")
            
            print('\n')
        except Exception as e:
            self.get_logger().error(f'Failed to parse detection: {e}')


def main(args=None) -> None:
    rclpy.init(args=args)
    node = DetectionViewer()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
