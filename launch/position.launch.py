import os

from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch_ros.actions import Node

import xacro


def generate_launch_description():

    # Get URDF via xacro
    robot_description_path = os.path.join(
        get_package_share_directory('ros2_control_kuka_demo_driver'),
        'description',
        'kr6.urdf.xacro')
    robot_description_config = xacro.process_file(robot_description_path)
    robot_description = {'robot_description': robot_description_config.toxml()}

    rrbot_forward_controller = os.path.join(
        get_package_share_directory('ros2_control_kuka_demo_driver'),
        'controllers',
        'kuka_6dof_controller_position.yaml'
        )

    return LaunchDescription([
      Node(
        package='controller_manager',
        executable='ros2_control_node',
        parameters=[robot_description, rrbot_forward_controller],
        output={
          'stdout': 'screen',
          'stderr': 'screen',
          },
        ),
        Node(
          package='robot_state_publisher',
          executable='robot_state_publisher',
          output='both',
          parameters=[robot_description]
        )

    ])
