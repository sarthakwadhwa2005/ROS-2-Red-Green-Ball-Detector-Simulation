#!/usr/bin/env bash
set -euo pipefail

source /opt/ros/humble/setup.bash

WS_DIR="${1:-$HOME/ros2_ball_detector_ws}"

cd "$WS_DIR"
colcon build --symlink-install
source install/setup.bash
ros2 launch ball_detector_sim simulation.launch.py
