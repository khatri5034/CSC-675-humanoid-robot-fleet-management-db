"""Robo-Nexus ORM model definitions.

These models map core milestone tables and are used by `services/services.py`.
"""

from orm.columns import Column
from orm.datatypes import DateTime, Integer, String
from orm.base import Base


class User(Base):
    __name__ = "Users"
    __tablename__ = "Users"

    UserID = Column(Integer, primary_key=True)
    UserName = Column(String, nullable=False)


class Robot(Base):
    __name__ = "Robots"
    __tablename__ = "Robots"

    RobotID = Column(Integer, primary_key=True)
    RobotRoleID = Column(Integer, nullable=False)
    RobotModelID = Column(Integer, nullable=False)
    DeploymentLocationID = Column(Integer, nullable=True)
    UserID = Column(Integer, nullable=False)
    SoftwareVersionID = Column(Integer, nullable=False)


class Task(Base):
    __name__ = "Tasks"
    __tablename__ = "Tasks"

    TaskID = Column(Integer, primary_key=True)
    TaskName = Column(String, nullable=False)
    Description = Column(String, nullable=False)
    Priority = Column(String, nullable=False)
    Status = Column(Integer, nullable=False)


class TaskAssignment(Base):
    __name__ = "TaskAssignments"
    __tablename__ = "TaskAssignments"

    TaskAssignmentID = Column(Integer, primary_key=True)
    RobotID = Column(Integer, nullable=False)
    UserID = Column(Integer, nullable=False)
    TaskID = Column(Integer, nullable=False)
    AssignedAt = Column(DateTime, nullable=False)


class SupportRequest(Base):
    __name__ = "SupportRequests"
    __tablename__ = "SupportRequests"

    SupportRequestID = Column(Integer, primary_key=True)
    RobotID = Column(Integer, nullable=False)
    IssueDetails = Column(String, nullable=False)
    TimeReported = Column(DateTime, nullable=False)







