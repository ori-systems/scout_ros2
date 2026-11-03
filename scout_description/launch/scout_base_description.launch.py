"""Publish Scout Mini Omni (default), standard Mini or Scout V2 TF and joint states."""
import launch
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.conditions import IfCondition
from launch.substitutions import Command, FindExecutable, LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare
from launch_ros.parameter_descriptions import ParameterValue


def generate_launch_description():
    # Latest coloured Scout Mini Omni is the default. Paths are relative to urdf/.
    model = LaunchConfiguration('model')
    robot_description = Command([
        FindExecutable(name='xacro'), ' ',
        PathJoinSubstitution([FindPackageShare('scout_description'), 'urdf', model]),
    ])
    robot_description = ParameterValue(robot_description, value_type=str)
    return LaunchDescription([
        DeclareLaunchArgument(
            'model', default_value='scout_mini/scout_mini_omni.xacro',
            description='Path under scout_description/urdf/; '
                        'e.g. scout_mini/scout_mini_omni.xacro'),
        DeclareLaunchArgument('use_sim_time', default_value='false'),
        DeclareLaunchArgument(
            'publish_joint_states', default_value='true',
            description='Publish zero-position wheel joints when no hardware joint publisher exists'),
        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            name='robot_state_publisher',
            output='screen',
            parameters=[{
                'use_sim_time': LaunchConfiguration('use_sim_time'),
                'robot_description': robot_description,
            }],
        ),
        Node(
            package='joint_state_publisher',
            executable='joint_state_publisher',
            name='joint_state_publisher',
            output='screen',
            condition=IfCondition(LaunchConfiguration('publish_joint_states')),
            parameters=[{
                    'use_sim_time': LaunchConfiguration('use_sim_time'),
                    'robot_description': robot_description,
                }],
        ),
    ])
