# ROS 2 Mini Project: Red/Green Ball Detection in Gazebo

This project is built for **Ubuntu 22.04 LTS**, **ROS 2 Humble**, and **Gazebo**.

## 1. Project Objective
Detect red and green balls in a simulated environment using computer vision.

## 2. Expected Outcome
- Camera stream is generated in Gazebo.
- A ROS 2 node detects red and green balls in each frame.
- Detection results are published as JSON on a topic.
- Annotated image (with circles and labels) is published on another topic.

## 3. Workspace Structure

```text
ros2_ball_detector_ws/
  src/
    ball_detector_sim/
      ball_detector_sim/
        ball_detector_node.py
      launch/
        simulation.launch.py
      models/
        camera_station/
        red_ball/
        green_ball/
```

## 4. Install Dependencies (Ubuntu 22.04)

```bash
sudo apt update
sudo apt install -y \
  ros-humble-desktop \
  ros-humble-gazebo-ros-pkgs \
  ros-humble-cv-bridge \
  python3-opencv \
  python3-colcon-common-extensions
```

Or use the included script:

```bash
cd ~/ros2_ball_detector_ws
chmod +x scripts/setup_ubuntu_humble.sh
./scripts/setup_ubuntu_humble.sh
```

Source ROS 2:

```bash
source /opt/ros/humble/setup.bash
```

## 5. Build

```bash
cd ~/ros2_ball_detector_ws
colcon build --symlink-install
source install/setup.bash
```

## 6. Run Simulation + Detector

```bash
ros2 launch ball_detector_sim simulation.launch.py
```

One-command build + launch:

```bash
cd ~/ros2_ball_detector_ws
chmod +x scripts/build_and_run.sh
./scripts/build_and_run.sh ~/ros2_ball_detector_ws
```

## 7. Verify Outputs

Check active topics:

```bash
ros2 topic list
```

Expected key topics:
- `/camera/camera/image_raw`
- `/ball_detector/annotated_image`
- `/ball_detector/detections`

View annotated image:

```bash
ros2 run rqt_image_view rqt_image_view
```

Inspect detections (simple count):

```bash
ros2 topic echo /ball_detector/detections
```

## 8. Example Detection Message

```json
{
  "red_balls": 1,
  "green_balls": 1,
  "total": 2
}
```

View output:
```bash
ros2 topic echo /ball_detector/detections
```
