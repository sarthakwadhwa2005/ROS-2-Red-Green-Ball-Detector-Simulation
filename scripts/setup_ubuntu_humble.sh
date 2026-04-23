#!/usr/bin/env bash
set -euo pipefail

sudo apt update
sudo apt install -y \
  ros-humble-desktop \
  ros-humble-gazebo-ros-pkgs \
  ros-humble-cv-bridge \
  python3-opencv \
  python3-colcon-common-extensions

echo "source /opt/ros/humble/setup.bash" >> "$HOME/.bashrc"
echo "ROS 2 Humble dependencies installed. Open a new terminal or run: source /opt/ros/humble/setup.bash"
