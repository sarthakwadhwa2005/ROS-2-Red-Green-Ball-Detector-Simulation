from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.actions import TimerAction
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory
import os


def generate_launch_description():
    gazebo_ros_share = get_package_share_directory('gazebo_ros')
    this_pkg_share = get_package_share_directory('ball_detector_sim')

    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(gazebo_ros_share, 'launch', 'gazebo.launch.py')
        )
    )

    spawn_camera = Node(
        package='gazebo_ros',
        executable='spawn_entity.py',
        arguments=[
            '-entity', 'camera_station',
            '-file', os.path.join(this_pkg_share, 'models', 'camera_station', 'model.sdf'),
            '-x', '0.0', '-y', '0.0', '-z', '3.0',
        ],
        output='screen',
    )

    spawn_red_ball = Node(
        package='gazebo_ros',
        executable='spawn_entity.py',
        arguments=[
            '-entity', 'red_ball',
            '-file', os.path.join(this_pkg_share, 'models', 'red_ball', 'model.sdf'),
            '-x', '2.4', '-y', '0.8', '-z', '0.12',
        ],
        output='screen',
    )

    spawn_green_ball = Node(
        package='gazebo_ros',
        executable='spawn_entity.py',
        arguments=[
            '-entity', 'green_ball',
            '-file', os.path.join(this_pkg_share, 'models', 'green_ball', 'model.sdf'),
            '-x', '2.2', '-y', '-0.7', '-z', '0.12',
        ],
        output='screen',
    )

    detector = Node(
        package='ball_detector_sim',
        executable='ball_detector_node',
        name='ball_detector',
        output='screen',
        parameters=[
            {'image_topic': '/camera/camera/image_raw'},
            {'annotated_topic': '/ball_detector/annotated_image'},
            {'min_radius_px': 6.0},
        ],
    )

    return LaunchDescription([
        gazebo,
        TimerAction(period=2.0, actions=[spawn_camera]),
        TimerAction(period=3.0, actions=[spawn_red_ball, spawn_green_ball]),
        TimerAction(period=4.0, actions=[detector]),
    ])

