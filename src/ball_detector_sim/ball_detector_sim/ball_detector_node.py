#!/usr/bin/env python3
import json

import cv2
from cv_bridge import CvBridge, CvBridgeError
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from std_msgs.msg import String


class BallDetectorNode(Node):
    def __init__(self) -> None:
        super().__init__('ball_detector_node')

        self.declare_parameter('image_topic', '/camera/camera/image_raw')
        self.declare_parameter('annotated_topic', '/ball_detector/annotated_image')
        self.declare_parameter('min_radius_px', 10.0)

        image_topic = self.get_parameter('image_topic').get_parameter_value().string_value
        annotated_topic = self.get_parameter('annotated_topic').get_parameter_value().string_value
        self.min_radius_px = self.get_parameter('min_radius_px').get_parameter_value().double_value

        self.bridge = CvBridge()
        self.image_sub = self.create_subscription(Image, image_topic, self.on_image, 10)
        self.annotated_pub = self.create_publisher(Image, annotated_topic, 10)
        self.detections_pub = self.create_publisher(String, '/ball_detector/detections', 10)

        self.get_logger().info(f'Listening on image topic: {image_topic}')

    def _build_color_mask(self, hsv_image, color_name):
        if color_name == 'red':
            lower1 = (0, 120, 70)
            upper1 = (10, 255, 255)
            lower2 = (170, 120, 70)
            upper2 = (180, 255, 255)
            mask1 = cv2.inRange(hsv_image, lower1, upper1)
            mask2 = cv2.inRange(hsv_image, lower2, upper2)
            mask = cv2.bitwise_or(mask1, mask2)
        else:
            lower = (35, 80, 50)
            upper = (90, 255, 255)
            mask = cv2.inRange(hsv_image, lower, upper)

        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
        return mask

    def _find_circles(self, mask, color_name):
        blurred = cv2.GaussianBlur(mask, (9, 9), 2)
        circles = cv2.HoughCircles(
            blurred,
            cv2.HOUGH_GRADIENT,
            dp=1.2,
            minDist=max(16.0, self.min_radius_px * 1.6),
            param1=100,
            param2=18,
            minRadius=int(self.min_radius_px),
            maxRadius=80,
        )

        detections = []
        if circles is None:
            return detections

        for circle in circles[0]:
            x, y, radius = circle
            detections.append(
                {
                    'color': color_name,
                    'x': int(round(float(x))),
                    'y': int(round(float(y))),
                    'radius': int(round(float(radius))),
                }
            )

        return detections

    def _merge_near_duplicates(self, detections):
        # Keep larger circles first, then suppress near-overlapping duplicates of the same color.
        sorted_detections = sorted(detections, key=lambda d: d['radius'], reverse=True)
        merged = []

        for det in sorted_detections:
            duplicate = False
            for existing in merged:
                if det['color'] != existing['color']:
                    continue

                dx = det['x'] - existing['x']
                dy = det['y'] - existing['y']
                center_dist = (dx * dx + dy * dy) ** 0.5
                max_r = max(det['radius'], existing['radius'])
                min_r = min(det['radius'], existing['radius'])

                # Same ball often appears as nested/near-concentric circles in Hough output.
                near_same_center = center_dist < (1.1 * max_r)
                one_inside_other = (center_dist + min_r) < (1.15 * max_r)

                if near_same_center or one_inside_other:
                    duplicate = True
                    break

            if not duplicate:
                merged.append(det)

        return merged

    def on_image(self, msg: Image) -> None:
        try:
            frame = self.bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')
        except CvBridgeError as ex:
            self.get_logger().error(f'Failed to convert image: {ex}')
            return

        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        red_mask = self._build_color_mask(hsv, 'red')
        green_mask = self._build_color_mask(hsv, 'green')

        detections = self._find_circles(red_mask, 'red') + self._find_circles(green_mask, 'green')
        detections = self._merge_near_duplicates(detections)

        red_count = sum(1 for d in detections if d['color'] == 'red')
        green_count = sum(1 for d in detections if d['color'] == 'green')

        for det in detections:
            center = (det['x'], det['y'])
            draw_color = (0, 0, 255) if det['color'] == 'red' else (0, 255, 0)
            cv2.circle(frame, center, det['radius'], draw_color, 2)
            cv2.putText(
                frame,
                det['color'],
                (center[0] - 18, center[1] - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                draw_color,
                2,
                cv2.LINE_AA,
            )

        payload = {
            'red_balls': red_count,
            'green_balls': green_count,
            'total': len(detections),
        }

        detections_msg = String()
        detections_msg.data = json.dumps(payload, separators=(',', ':'))
        self.detections_pub.publish(detections_msg)

        try:
            annotated_msg = self.bridge.cv2_to_imgmsg(frame, encoding='bgr8')
            annotated_msg.header = msg.header
            self.annotated_pub.publish(annotated_msg)
        except CvBridgeError as ex:
            self.get_logger().error(f'Failed to publish annotated image: {ex}')


def main(args=None) -> None:
    rclpy.init(args=args)
    node = BallDetectorNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()


