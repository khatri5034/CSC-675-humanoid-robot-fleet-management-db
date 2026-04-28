"""Robo-Nexus ORM model definitions.

These models map core milestone tables and are used by `services/services.py`.
Class names match SQL table names so `Base.table_descriptor()` resolves correctly.

Use `foreign_key=True` on columns that reference other tables (per your SQL schema).
For `REFERENCES ...` in generated DDL, use `foreign_key="Table(Col)"` instead.
"""

from orm.columns import Column
from orm.datatypes import DateTime, Integer, String
from orm.base import Base


class Users(Base):
    UserID = Column(Integer, primary_key=True)
    UserName = Column(String, nullable=False)

    def __repr__(self):
        return f"Users(UserID={self.UserID}, UserName={self.UserName})"


class Robots(Base):
    RobotID = Column(Integer, primary_key=True)
    RobotRoleID = Column(Integer, nullable=False, foreign_key=True)
    RobotModelID = Column(Integer, nullable=False, foreign_key=True)
    DeploymentLocationID = Column(Integer, nullable=True, foreign_key=True)
    UserID = Column(Integer, nullable=False, foreign_key=True)
    SoftwareVersionID = Column(Integer, nullable=False, foreign_key=True)

    def __repr__(self):
        return f"Robots(RobotID={self.RobotID}, UserID={self.UserID})"


class Tasks(Base):
    TaskID = Column(Integer, primary_key=True)
    TaskName = Column(String, nullable=False)
    Description = Column(String, nullable=False)
    Priority = Column(String, nullable=False)
    Status = Column(Integer, nullable=False)

    def __repr__(self):
        return (
            f"Tasks(TaskID={self.TaskID}, TaskName={self.TaskName}, "
            f"Status={self.Status})"
        )


class TaskAssignments(Base):
    TaskAssignmentID = Column(Integer, primary_key=True)
    RobotID = Column(Integer, nullable=False, foreign_key=True)
    UserID = Column(Integer, nullable=False, foreign_key=True)
    TaskID = Column(Integer, nullable=False, foreign_key=True)
    AssignedAt = Column(DateTime, nullable=False)

    def __repr__(self):
        return (
            f"TaskAssignments(TaskAssignmentID={self.TaskAssignmentID}, "
            f"RobotID={self.RobotID}, TaskID={self.TaskID})"
        )


class SupportRequests(Base):
    SupportRequestID = Column(Integer, primary_key=True)
    RobotID = Column(Integer, nullable=False, foreign_key=True)
    IssueDetails = Column(String, nullable=False)
    TimeReported = Column(DateTime, nullable=False)

    def __repr__(self):
        return (
            f"SupportRequests(SupportRequestID={self.SupportRequestID}, "
            f"RobotID={self.RobotID})"
        )
