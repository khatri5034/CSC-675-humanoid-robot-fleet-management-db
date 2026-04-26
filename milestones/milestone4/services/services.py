"""Public service-layer API for the Robo-Nexus database.

Service methods expose business operations and rely on ORM model methods.
No raw SQL should appear in this file.
"""

from datetime import datetime
from typing import Any, List, Optional


def create_user(user_name: str) -> Any:
    """Create and persist a user record."""
    from models.models import User

    if not user_name or not user_name.strip():
        raise ValueError("user_name is required.")

    user = User(UserName=user_name.strip())
    user.save()
    return user


def register_robot(
    robot_role_id: int,
    robot_model_id: int,
    user_id: int,
    software_version_id: int,
    deployment_location_id: Optional[int] = None,
) -> Any:
    """Register a robot in the fleet."""
    from models.models import Robot

    robot = Robot(
        RobotRoleID=robot_role_id,
        RobotModelID=robot_model_id,
        UserID=user_id,
        SoftwareVersionID=software_version_id,
        DeploymentLocationID=deployment_location_id,
    )
    robot.save()
    return robot


def create_task(task_name: str, description: str, priority: str, status: int = 0) -> Any:
    """Create a task that can later be assigned to a robot."""
    from models.models import Task

    if not task_name or not task_name.strip():
        raise ValueError("task_name is required.")
    if priority not in {"1", "2", "3", "4", "5"}:
        raise ValueError("priority must be one of: 1, 2, 3, 4, 5.")

    task = Task(
        TaskName=task_name.strip(),
        Description=description.strip(),
        Priority=priority,
        Status=status,
    )
    task.save()
    return task


def assign_task_to_robot(robot_id: int, user_id: int, task_id: int) -> Any:
    """Assign an existing task to a robot."""
    from models.models import TaskAssignment

    assignment = TaskAssignment(
        RobotID=robot_id,
        UserID=user_id,
        TaskID=task_id,
        AssignedAt=datetime.now(),
    )
    assignment.save()
    return assignment


def create_support_request(robot_id: int, issue_details: str) -> Any:
    """Open a support request for a robot issue."""
    from models.models import SupportRequest

    if not issue_details or not issue_details.strip():
        raise ValueError("issue_details is required.")

    support_request = SupportRequest(
        RobotID=robot_id,
        IssueDetails=issue_details.strip(),
        TimeReported=datetime.now(),
    )
    support_request.save()
    return support_request


def get_robot_by_id(robot_id: int) -> Optional[Any]:
    """Fetch one robot by primary key."""
    from models.models import Robot

    if robot_id <= 0:
        raise ValueError("robot_id must be a positive integer.")
    return Robot.get(RobotID=robot_id)


def list_robot_tasks(robot_id: int) -> List[Any]:
    """List task assignments for a robot."""
    from models.models import TaskAssignment

    if robot_id <= 0:
        raise ValueError("robot_id must be a positive integer.")
    return TaskAssignment.filter(RobotID=robot_id)

