from glob import glob
from setuptools import setup

package_name = 'ball_detector_sim'

setup(
    name=package_name,
    version='0.1.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages', ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        ('share/' + package_name + '/launch', glob('launch/*.py')),
        ('share/' + package_name + '/models/camera_station', glob('models/camera_station/*')),
        ('share/' + package_name + '/models/red_ball', glob('models/red_ball/*')),
        ('share/' + package_name + '/models/green_ball', glob('models/green_ball/*')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Mini Project Team',
    maintainer_email='student@example.com',
    description='ROS 2 Humble + Gazebo project for red/green ball detection using OpenCV.',
    license='MIT',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'ball_detector_node = ball_detector_sim.ball_detector_node:main',
        ],
    },
)
