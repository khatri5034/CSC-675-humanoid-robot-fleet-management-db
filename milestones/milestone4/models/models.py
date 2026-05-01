"""Core Robo-Nexus ORM models used by milestone4 services."""

from orm.base import Base
from orm.columns import Column
from orm.datatypes import DateTime, Integer, String


class Users(Base):
    __tablename__ = "Users"
    UserID = Column(Integer, primary_key=True, auto_increment=True, nullable=False)
    UserName = Column(String(length=45), nullable=False)


class RobotRoles(Base):
    __tablename__ = "RobotRoles"
    RobotRoleID = Column(Integer, primary_key=True, auto_increment=True, nullable=False)
    RobotRole = Column(String(type="ENUM('Senior', 'Worker')", length=None), nullable=True)
    UserID = Column(Integer, nullable=False, foreign_key="Users(UserID)")
    AIResponseID = Column(Integer, nullable=False)


class RobotModels(Base):
    __tablename__ = "RobotModels"
    RobotModelID = Column(Integer, primary_key=True, auto_increment=True, nullable=False)
    Model = Column(String(type="ENUM('Model1', 'Model2')", length=None), nullable=True)
    ManufacturerID = Column(Integer, nullable=True)


class DeploymentLocations(Base):
    __tablename__ = "DeploymentLocations"
    DeploymentLocationID = Column(Integer, primary_key=True, auto_increment=True, nullable=False)
    EnvironmentType = Column(
        String(type="ENUM('HOME', 'HOSPITAL', 'WAREHOUSE', 'FACTORY')", length=None),
        nullable=False,
    )
    AddressID = Column(Integer, nullable=False)


class SoftwareVersions(Base):
    __tablename__ = "SoftwareVersions"
    SoftwareVersionID = Column(Integer, primary_key=True, auto_increment=True, nullable=False)


class Robots(Base):
    __tablename__ = "Robots"
    RobotID = Column(Integer, primary_key=True, auto_increment=True, nullable=False)
    RobotRoleID = Column(Integer, nullable=False, foreign_key="RobotRoles(RobotRoleID)")
    RobotModelID = Column(Integer, nullable=False, foreign_key="RobotModels(RobotModelID)")
    DeploymentLocationID = Column(Integer, nullable=True, foreign_key="DeploymentLocations(DeploymentLocationID)")
    UserID = Column(Integer, nullable=False, foreign_key="Users(UserID)")
    SoftwareVersionID = Column(Integer, nullable=False, foreign_key="SoftwareVersions(SoftwareVersionID)")


class Tasks(Base):
    __tablename__ = "Tasks"
    TaskID = Column(Integer, primary_key=True, auto_increment=True, nullable=False)
    TaskName = Column(String(length=64), nullable=False)
    Description = Column(String(type="TEXT", length=None), nullable=False)
    Priority = Column(String(type="ENUM('1', '2', '3', '4', '5')", length=None), nullable=False)
    Status = Column(Integer(type="TINYINT"), nullable=False)


class TaskAssignments(Base):
    __tablename__ = "TaskAssignments"
    TaskAssignmentID = Column(Integer, primary_key=True, auto_increment=True, nullable=False)
    RobotID = Column(Integer, nullable=False, foreign_key="Robots(RobotID)")
    UserID = Column(Integer, nullable=False, foreign_key="Users(UserID)")
    TaskID = Column(Integer, nullable=False, foreign_key="Tasks(TaskID)")
    AssignedAt = Column(DateTime(type="TIMESTAMP"), nullable=False)


class SupportRequests(Base):
    __tablename__ = "SupportRequests"
    SupportRequestID = Column(Integer, primary_key=True, auto_increment=True, nullable=False)
    RobotID = Column(Integer, nullable=False, foreign_key="Robots(RobotID)")
    IssueDetails = Column(String(type="TEXT", length=None), nullable=False)
    TimeReported = Column(DateTime, nullable=False)


class AIModels(Base):
    __tablename__ = "AIModels"
    AIModelID = Column(Integer, primary_key=True, auto_increment=True, nullable=False)
    ModelName = Column(String(length=45), nullable=False)
    ServiceType = Column(String(length=45), nullable=False)
    VersionLabel = Column(String(length=45), nullable=False)


class AIRequests(Base):
    __tablename__ = "AIRequests"
    AIRequestID = Column(Integer, primary_key=True, auto_increment=True, nullable=False)
    AIModelID = Column(Integer, nullable=False, foreign_key="AIModels(AIModelID)")
    RobotID = Column(Integer, nullable=False, foreign_key="Robots(RobotID)")
    RequestedAt = Column(DateTime, nullable=False)


class AIResponses(Base):
    __tablename__ = "AIResponses"
    AIResponseID = Column(Integer, primary_key=True, auto_increment=True, nullable=False)
    AIRequestsID = Column(Integer, nullable=False, foreign_key="AIRequests(AIRequestID)")
    RobotRoleID = Column(Integer, nullable=False, foreign_key="RobotRoles(RobotRoleID)")
    TaskID = Column(Integer, nullable=False, foreign_key="Tasks(TaskID)")
    GeneratedAt = Column(DateTime, nullable=False)
    Response = Column(String(type="TEXT", length=None), nullable=False)