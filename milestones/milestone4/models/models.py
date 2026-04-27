"""Robo-Nexus ORM model definitions.

These models map core milestone tables and are used by `services/services.py`.
Class names match SQL table names so `Base.table_descriptor()` resolves correctly.
"""

from orm.columns import Column
from orm.datatypes import DateTime, Integer, String
from orm.base import Base


class Users(Base):
    UserID = Column(Integer, primary_key=True)
    UserName = Column(String, nullable=False)


class Robots(Base):
    RobotID = Column(Integer, primary_key=True)
    RobotRoleID = Column(Integer, nullable=False)
    RobotModelID = Column(Integer, nullable=False)
    DeploymentLocationID = Column(Integer, nullable=True)
    UserID = Column(Integer, nullable=False)
    SoftwareVersionID = Column(Integer, nullable=False)


class Tasks(Base):
    TaskID = Column(Integer, primary_key=True)
    TaskName = Column(String, nullable=False)
    Description = Column(String, nullable=False)
    Priority = Column(String, nullable=False)
    Status = Column(Integer, nullable=False)


class TaskAssignments(Base):
    TaskAssignmentID = Column(Integer, primary_key=True)
    RobotID = Column(Integer, nullable=False)
    UserID = Column(Integer, nullable=False)
    TaskID = Column(Integer, nullable=False)
    AssignedAt = Column(DateTime, nullable=False)


class SupportRequests(Base):
    SupportRequestID = Column(Integer, primary_key=True)
    RobotID = Column(Integer, nullable=False)
    IssueDetails = Column(String, nullable=False)
    TimeReported = Column(DateTime, nullable=False)
