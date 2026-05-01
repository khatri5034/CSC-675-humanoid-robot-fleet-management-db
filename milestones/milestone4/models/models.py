"""Robo-Nexus ORM model definitions."""

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


class Manufacturers(Base):
    __tablename__ = "Manufacturers"
    ManufacturerID = Column(Integer, primary_key=True, auto_increment=True, nullable=False)
    Name = Column(String(length=64), nullable=False)


class RobotModels(Base):
    __tablename__ = "RobotModels"
    RobotModelID = Column(Integer, primary_key=True, auto_increment=True, nullable=False)
    Model = Column(String(type="ENUM('Model1', 'Model2')", length=None), nullable=True)
    ManufacturerID = Column(Integer, nullable=True, foreign_key="Manufacturers(ManufacturerID)")


class Addresses(Base):
    __tablename__ = "Addresses"
    AddressID = Column(Integer, primary_key=True, auto_increment=True, nullable=False)
    Street = Column(String(length=90), nullable=False)
    City = Column(String(length=90), nullable=False)
    State = Column(String(type="CHAR", length=2), nullable=False)
    Zipcode = Column(String(type="CHAR", length=5), nullable=False)


class DeploymentLocations(Base):
    __tablename__ = "DeploymentLocations"
    DeploymentLocationID = Column(Integer, primary_key=True, auto_increment=True, nullable=False)
    EnvironmentType = Column(
        String(type="ENUM('HOME', 'HOSPITAL', 'WAREHOUSE', 'FACTORY')", length=None),
        nullable=False,
    )
    AddressID = Column(Integer, nullable=False, foreign_key="Addresses(AddressID)")


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


class Alerts(Base):
    __tablename__ = "Alerts"
    AlertID = Column(Integer, primary_key=True, auto_increment=True, nullable=False)
    RobotID = Column(Integer, nullable=False, foreign_key="Robots(RobotID)")
    Severity = Column(String(type="ENUM('Low', 'Medium', 'High', 'Critical')", length=None), nullable=False)
    TimeStamp = Column(DateTime(type="TIMESTAMP"), nullable=False)


class PerformanceMetrics(Base):
    __tablename__ = "PerformanceMetrics"
    PerformanceMetricID = Column(Integer, primary_key=True, auto_increment=True, nullable=False)
    RobotID = Column(Integer, nullable=False, foreign_key="Robots(RobotID)")
    MetricType = Column(String(length=45), nullable=False)
    MetricValue = Column(Integer, nullable=False)
    TimeStamp = Column(DateTime, nullable=False)


class Technicians(Base):
    __tablename__ = "Technicians"
    TechnicianID = Column(Integer, primary_key=True, auto_increment=True, nullable=False)
    DeploymentLocationID = Column(Integer, nullable=True, foreign_key="DeploymentLocations(DeploymentLocationID)")


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


class TaskExecutions(Base):
    __tablename__ = "TaskExecutions"
    TaskExecutionID = Column(Integer, primary_key=True, auto_increment=True, nullable=False)
    TaskID = Column(Integer, nullable=False, foreign_key="Tasks(TaskID)")
    StartTime = Column(DateTime(type="TIMESTAMP"), nullable=False)
    EndTime = Column(DateTime(type="TIMESTAMP"), nullable=False)
    Status = Column(Integer(type="TINYINT"), nullable=False)


class Hardwares(Base):
    __tablename__ = "Hardwares"
    HardwareID = Column(Integer, primary_key=True, auto_increment=True, nullable=False)
    ManufacturerID = Column(Integer, nullable=True, foreign_key="Manufacturers(ManufacturerID)")


class RobotHardware(Base):
    __tablename__ = "RobotHardware"
    RobotHardwareID = Column(Integer, primary_key=True, auto_increment=True, nullable=False)
    RobotID = Column(Integer, nullable=False, foreign_key="Robots(RobotID)")


class ChargingSessions(Base):
    __tablename__ = "ChargingSessions"
    ChargingSessionID = Column(Integer, primary_key=True, auto_increment=True, nullable=False)
    DeploymentLocationID = Column(Integer, nullable=False, foreign_key="DeploymentLocations(DeploymentLocationID)")
    StartTime = Column(DateTime(type="TIMESTAMP"), nullable=False)
    EndTime = Column(DateTime(type="TIMESTAMP"), nullable=True)


class EnergyStatus(Base):
    __tablename__ = "EnergyStatus"
    EnergyStatusID = Column(Integer, primary_key=True, auto_increment=True, nullable=False)
    ChargingSessionID = Column(Integer, nullable=False, foreign_key="ChargingSessions(ChargingSessionID)")
    BatteryLevel = Column(Integer(type="TINYINT"), nullable=False)
    RecordedAt = Column(DateTime(type="TIMESTAMP"), nullable=False)
    RobotID = Column(Integer, nullable=False, foreign_key="Robots(RobotID)")


class ChargingStations(Base):
    __tablename__ = "ChargingStations"
    ChargingStationID = Column(Integer, primary_key=True, auto_increment=True, nullable=False)
    StationName = Column(String(length=64), nullable=True)
    Capacity = Column(Integer(type="TINYINT"), nullable=False)
    Status = Column(
        String(type="ENUM('AVAILABLE', 'OCCUPIED', 'MAINTENANCE', 'OFFLINE')", length=None),
        nullable=False,
    )


class ChargingStationSessions(Base):
    __tablename__ = "ChargingStationSessions"
    ChargingStationSessionID = Column(Integer, primary_key=True, auto_increment=True, nullable=False)
    ChargingSessionID = Column(Integer, nullable=False, foreign_key="ChargingSessions(ChargingSessionID)")
    ChargingStationID = Column(Integer, nullable=False, foreign_key="ChargingStations(ChargingStationID)")


class RobotChargingStations(Base):
    __tablename__ = "RobotChargingStations"
    RobotChargingStationID = Column(Integer, primary_key=True, auto_increment=True, nullable=False)
    ChargingStationID = Column(Integer, nullable=False, foreign_key="ChargingStations(ChargingStationID)")
    RobotID = Column(Integer, nullable=False, foreign_key="Robots(RobotID)")


class Logs(Base):
    __tablename__ = "Logs"
    LogID = Column(Integer, primary_key=True, auto_increment=True, nullable=False)
    RobotID = Column(Integer, nullable=False, foreign_key="Robots(RobotID)")
    CreatedAt = Column(DateTime(type="TIMESTAMP"), nullable=False)
    EventType = Column(String(length=64), nullable=False)
    EventDetails = Column(String(type="TEXT", length=None), nullable=True)


class TechnicianNames(Base):
    __tablename__ = "TechnicianNames"
    TechnicianNameID = Column(Integer, primary_key=True, auto_increment=True, nullable=False)
    TechnicianID = Column(Integer, nullable=False, foreign_key="Technicians(TechnicianID)")
    FirstName = Column(String(length=64), nullable=False)
    LastName = Column(String(length=64), nullable=False)


class LogSessions(Base):
    __tablename__ = "LogSessions"
    LogSessionID = Column(Integer, primary_key=True, auto_increment=True, nullable=False)
    ChargingSessionID = Column(Integer, nullable=False, foreign_key="ChargingSessions(ChargingSessionID)")
    LogID = Column(Integer, nullable=False, foreign_key="Logs(LogID)")


class Sensors(Base):
    __tablename__ = "Sensors"
    SensorID = Column(Integer, primary_key=True, auto_increment=True, nullable=False)
    RobotID = Column(Integer, nullable=False, foreign_key="Robots(RobotID)")
    SensorType = Column(String(length=45), nullable=False)
    Status = Column(String(type="ENUM('ACTIVE', 'INACTIVE')", length=None), nullable=False)


class UserDeploymentLocation(Base):
    __tablename__ = "UserDeploymentLocation"
    UserDeploymentLocationID = Column(Integer, primary_key=True, auto_increment=True, nullable=False)
    DeploymentLocationID = Column(Integer, nullable=False, foreign_key="DeploymentLocations(DeploymentLocationID)")
    UserID = Column(Integer, nullable=False, foreign_key="Users(UserID)")


class timestamps(Base):
    __tablename__ = "timestamps"
    create_time = Column(DateTime(type="TIMESTAMP"), primary_key=True, nullable=True)
    update_time = Column(DateTime(type="TIMESTAMP"), nullable=True)


class Hospitals(Base):
    __tablename__ = "Hospitals"
    HospitalID = Column(Integer, primary_key=True, auto_increment=True, nullable=False)
    DeploymentLocationID = Column(Integer, nullable=False, foreign_key="DeploymentLocations(DeploymentLocationID)")


class Warehouses(Base):
    __tablename__ = "Warehouses"
    WarehouseID = Column(Integer, primary_key=True, auto_increment=True, nullable=False)
    DeploymentLocationID = Column(Integer, nullable=False, foreign_key="DeploymentLocations(DeploymentLocationID)")


class Homes(Base):
    __tablename__ = "Homes"
    HomeID = Column(Integer, primary_key=True, auto_increment=True, nullable=False)
    DeploymentLocationID = Column(Integer, nullable=False, foreign_key="DeploymentLocations(DeploymentLocationID)")


class Factories(Base):
    __tablename__ = "Factories"
    FactoryID = Column(Integer, primary_key=True, auto_increment=True, nullable=False)
    DeploymentLocationID = Column(Integer, nullable=False, foreign_key="DeploymentLocations(DeploymentLocationID)")


class Department(Base):
    __tablename__ = "Department"
    DepartmentID = Column(Integer, primary_key=True, auto_increment=True, nullable=False)
    DepartmentName = Column(String(length=45), nullable=False)
    HosptialID = Column(Integer, nullable=False, foreign_key="Hospitals(HospitalID)")


class AIModels(Base):
    __tablename__ = "AIModels"
    AIModelID = Column(Integer, primary_key=True, auto_increment=True, nullable=False)
    ModelName = Column(String(length=45), nullable=False)
    ServiceType = Column(String(length=45), nullable=False)
    VersionLabel = Column(String(length=45), nullable=False)


class EmotionalPatterns(Base):
    __tablename__ = "EmotionalPatterns"
    EmotionalPatternID = Column(Integer, primary_key=True, auto_increment=True, nullable=False)
    RobotID = Column(Integer, nullable=False, foreign_key="Robots(RobotID)")
    AIModelID = Column(Integer, nullable=False, foreign_key="AIModels(AIModelID)")
    PatternSummary = Column(String(type="TEXT", length=None), nullable=False)


class MaintenanceRecord(Base):
    __tablename__ = "MaintenanceRecord"
    MaintenanceRecordID = Column(Integer, primary_key=True, auto_increment=True, nullable=False)
    RobotID = Column(Integer, nullable=False, foreign_key="Robots(RobotID)")
    TechinicianID = Column(Integer, nullable=False, foreign_key="Technicians(TechnicianID)")
    RecordedAt = Column(DateTime(type="TIMESTAMP"), nullable=False)
    Description = Column(String(type="TEXT", length=None), nullable=False)


class EmotionalRecords(Base):
    __tablename__ = "EmotionalRecords"
    Emotional_ID = Column(Integer, primary_key=True, auto_increment=True, nullable=False)
    EmotionalPatternID = Column(Integer, nullable=False, foreign_key="EmotionalPatterns(EmotionalPatternID)")
    EmotionalState = Column(String(type="ENUM('1', '2', '3')", length=None), nullable=False)
    Timestamp = Column(DateTime, nullable=False)
    Description = Column(String(length=45), nullable=False)


class InteractionSessions(Base):
    __tablename__ = "InteractionSessions"
    InteractionID = Column(Integer, primary_key=True, auto_increment=True, nullable=False)
    RobotID = Column(Integer, nullable=False, foreign_key="Robots(RobotID)")
    UserID = Column(Integer, nullable=False, foreign_key="Users(UserID)")
    HomeID = Column(Integer, nullable=False, foreign_key="Homes(HomeID)")
    StartTIme = Column(DateTime, nullable=False)
    EndTIme = Column(DateTime, nullable=False)


class DiagnosticReports(Base):
    __tablename__ = "DiagnosticReports"
    DiagnosticReportID = Column(Integer, primary_key=True, auto_increment=True, nullable=False)
    RobotID = Column(Integer, nullable=False, foreign_key="Robots(RobotID)")
    AIModelID = Column(Integer, nullable=False, foreign_key="AIModels(AIModelID)")
    GeneratedAt = Column(DateTime, nullable=False)
    Summary = Column(String(type="TEXT", length=None), nullable=False)


class SupportRequests(Base):
    __tablename__ = "SupportRequests"
    SupportRequestID = Column(Integer, primary_key=True, auto_increment=True, nullable=False)
    RobotID = Column(Integer, nullable=False, foreign_key="Robots(RobotID)")
    IssueDetails = Column(String(type="TEXT", length=None), nullable=False)
    TimeReported = Column(DateTime, nullable=False)


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


class EmotionalAnalyzes(Base):
    __tablename__ = "EmotionalAnalyzes"
    EmotionalAnalyzeID = Column(Integer, primary_key=True, auto_increment=True, nullable=False)
    EmotionalID = Column(Integer, nullable=False, foreign_key="EmotionalRecords(Emotional_ID)")
    AIRequestID = Column(Integer, nullable=False, foreign_key="AIRequests(AIRequestID)")


class PerformanceDiagnostics(Base):
    __tablename__ = "PerformanceDiagnostics"
    PerformanceDiagnosticID = Column(Integer, primary_key=True, auto_increment=True, nullable=False)
    DiagnosticReportID = Column(Integer, nullable=False, foreign_key="DiagnosticReports(DiagnosticReportID)")
    PerformanceMetricID = Column(Integer, nullable=False, foreign_key="PerformanceMetrics(PerformanceMetricID)")
    PerformanceDiagnosticscol = Column(String(length=45), nullable=True)


class EmotionalInteractionSessions(Base):
    __tablename__ = "EmotionalInteractionSessions"
    EmotionalInteractionSessionID = Column(Integer, primary_key=True, auto_increment=True, nullable=False)
    EmotionalID = Column(Integer, nullable=False, foreign_key="EmotionalRecords(Emotional_ID)")
    InteractionID = Column(Integer, nullable=False, foreign_key="InteractionSessions(InteractionID)")


class TechnicianSupportRequests(Base):
    __tablename__ = "TechnicianSupportRequests"
    TechnicianSupportRequestID = Column(Integer, primary_key=True, auto_increment=True, nullable=False)
    SupportRequestID = Column(Integer, nullable=False, foreign_key="SupportRequests(SupportRequestID)")
    TechnicianID = Column(Integer, nullable=False, foreign_key="Technicians(TechnicianID)")


class HardwareMaintenances(Base):
    __tablename__ = "HardwareMaintenances"
    HardwareMaintenancesID = Column(Integer, primary_key=True, auto_increment=True, nullable=False)
    HardwareID = Column(Integer, nullable=False, foreign_key="Hardwares(HardwareID)")
    MaintenanceRecordID = Column(Integer, nullable=False, foreign_key="MaintenanceRecord(MaintenanceRecordID)")


class PatientEmotionalRecords(Base):
    __tablename__ = "PatientEmotionalRecords"
    PatientEmotionalRecordID = Column(Integer, primary_key=True, auto_increment=True, nullable=False)
    EmotionalID = Column(Integer, nullable=False, foreign_key="EmotionalRecords(Emotional_ID)")
    HospitalID = Column(Integer, nullable=False, foreign_key="Hospitals(HospitalID)")


class MetricThresholds(Base):
    __tablename__ = "MetricThresholds"
    MetricType = Column(String(length=45), primary_key=True, nullable=False)
    ThresholdValue = Column(Integer, nullable=False)