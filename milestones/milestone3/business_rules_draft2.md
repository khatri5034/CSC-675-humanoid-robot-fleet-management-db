# AI-Powered Humanoid Robot Fleet Management System

## Milestone 3 – Phase 1: Business Rules Definition

---

## Rule 1: Minimum Battery to Execute Task

**Purpose:** Prevent robots from executing tasks when battery is critically low.

**Description:** A robot shall not start a task execution if its battery level is below 20%.

**Challenges:** checking latest timestamp battery level per robot

**Assumptions:** Latest EnergyStatus record represent current battery

**Planned Approach:** Trigger on task execution

---

## Rule 2: Charging Station Capacity Enforcement

**Purpose:** Prevent from overloading the charging stations.

**Description:** The number of active Charging Sessions (robots) in charging stations shall not exceed its capacity.

**Challenges:** Count the number of active sessions and the capacity of the stations.

**Assumptions:** Active session records represent the latest number of robots at charging stations.

**Planned Approach:** Trigger on ChargingStationsSessions.

---

## Rule 3: One active task per Robot

**Purpose:** Prevents overloading robots.

**Description:** A robot can only have one active task at a time and must finish the task before getting another active task.

**Challenges:** Can cause race conditions with other robots trying to take roles that are dependent on other roles.

**Assumptions:** a robot can not be multitasking.

**Planned Approach:** Triggers on Task Execution.

---

## Rule 4: SupportRequest Must Reference Existing Robot

**Purpose:** Ensure support

**Description:** When assigned a task a robot shall also need a time to begin executing the task, making sure the robot doesn’t crash into another one or interfere with other activities depending on the deployment location

**Challenges:** Can cause delays in execution of all tasks across robot fleet

**Assumptions:** Robots can move, and will not always be monitored by a user

**Planned Approach:** FOREIGN KEY constraint on SupportRequest.robot_id referencing Robot.robot_id.

---

## Rule 5: Task Must Exist Before Execution

**Purpose:** Prevent Robot from unauthorized execution.

**Description:** A robot shall not execute a task by itself unless the robot has a senior role or assigned by a user or by AI to make sure the robot gets tasks as per their specs and status.

**Challenges:** Checking multiple tables before assigning.

**Assumptions:** TaskAssignment table must exist and contains the tasks needed to be completed.

**Planned Approach:** FOREIGN KEY constraint on TaskExecution.task_id referencing Task.task_id.

---

## Rule 6: Robot cannot charge and execute a task at the same time

**Purpose:** Prevents robots from having multiple states at once.

**Description:** A robot can not be doing a task while charging at the same time.

**Challenges:** A robot might need to start charging while still working on a task.

**Assumptions:** A robot must stop a task execution before starting to charge.

**Planned Approach:** triggers on TaskExecutions and ChargingSessions.

---

## Rule 7: Robots cannot have multiple active roles.

**Purpose:** Enforce one role at a time

**Description:** A robot shall have only one role during the active sessions assigned by AI or user.

**Challenges:** Must have the details of the robots and also its existing role and also look up multiple tables.

**Assumptions:** Role is stored in RobotRole table and description of robot in robot table.

**Planned Approach:** Trigger on RobotRole.

---

## Rule 8: Emotional Record must belong to existing interactions

**Purpose:** Prevent data from corruption and stale.

**Description:** Emotional record shall not exist without interactionSession and user

**Challenges:** Keeping track of emotion of the users based on the interactions

**Assumptions:** Robots shall record user emotions in the Emotional record table based on interaction sessions.

**Planned Approach:** FOREIGN KEY constraint on EmotionalRecord.interaction_id.

---

## Rule 9: InteractionSession Must Reference Existing Robot and User

**Purpose:** To ensure all interactions are valid

**Description:** An InteractionSession shall reference an existing Robot and User. The database shall prevent creating interaction records with non-existent robots or users.

**Challenges:** Maintaining referential integrity during insert, update, and delete operations.

**Assumptions:** Robots and users are registered in the system before interaction sessions are recorded.

**Planned Approach:** Use FOREIGN KEY constraints on InteractionSession.robot_id and InteractionSession.user_id referencing Robot(robot_id) and User(user_id) with ON DELETE RESTRICT and ON UPDATE CASCADE.

---

## Rule 10: MaintenanceRecord Must Reference Existing Technician

**Purpose:** Ensure accountability for all maintenance activities performed on robots.

**Description:** A MaintenanceRecord shall not exist unless it references a valid and existing Technician. Every maintenance action must be associated with a specific technician in the system.

**Challenges:** Preventing insertion of maintenance record with  invalid technician id and also prevent deletion of a technician if maintenance records depend on that technician.

**Assumptions:** All technicians are stored in the Technician table before maintenance activities are recorded.

**Planned Approach:** Enforce using a FOREIGN KEY constraint on MaintenanceRecord.technician_id referencing Technician.technician_id.

---

## Rule 11: ChargingSession should be in Existing DeploymentLocation

**Purpose:** Ensure that all charging activities occur at valid and registered deployment locations.

**Description:** A ChargingSession shall not be created unless it references a valid DeploymentLocation. Every charging event must occur within a defined warehouse, hospital, home, or factory location stored in the system.

**Challenges:** Preventing insertion of charging sessions that reference non-existent locations.Cross checking multiple tables.

**Assumptions:** All deployment locations are created and maintained in the DeploymentLocation table before charging sessions occur. Each charging session occurs at exactly one deployment location.

**Planned Approach:** Enforce using a FOREIGN KEY constraint on ChargingSession.deployment_location_id referencing DeploymentLocation.deployment_location_id.

---

## Rule 12: PerformanceMetric Must Reference Existing Robot

**Purpose:** Ensure performance data is always associated with a valid robot in the system.

**Description:** PerformanceMetric record shall not exist unless it references an existing Robot. Performance measurements must be tied to a specific robot for historical tracking and analysis.

**Challenges:** Keeping track of performance and updating the data

**Assumptions:** Robots are created in the Robot table before performance metrics are recorded. Each performance metric belongs to exactly one robot.

**Planned Approach:** Enforce using a FOREIGN KEY constraint on PerformanceMetric.robot_id referencing Robot.robot_id.

---

## Rule 13: Alert Must Reference Existing Robot

**Purpose:** Ensure all alerts are associated with a valid robot and prevent invalid system notifications.

**Description:** An Alert record shall not be created unless it references an existing Robot. Every alert must correspond to a specific robot in the system.

**Challenges:** Keeping record of alerts associated with robots in each deployment location.

**Assumptions:** Alerts are generated only for robots already registered in the system. Each alert belongs to exactly one robot.

**Planned Approach:** Enforce using a FOREIGN KEY constraint on Alert.robot_id referencing Robot.robot_id.

---

## Rule 14: Deployment location with a valid address

**Purpose:** Ensure that every deployment location is associated with a valid physical address for accurate tracking

**Description:** A DeploymentLocation record shall not be created unless it references an existing Address. This ensures that all locations such as hospitals, warehouses, homes, and factories have valid address information.

**Challenges:** Maintaining referential integrity when inserting, updating, or deleting address records that are linked to deployment locations.

**Assumptions:** All valid addresses are stored in the Address table before deployment locations are created.

**Planned Approach:** FOREIGN KEY constraint on DeploymentLocation.address_id referencing Address.address_id

---

## Rule 15: AIRequest Must Reference an Existing Robot

**Purpose:** To ensure that every AI request in the system is associated with a valid robot

**Description:** An AIRequest shall reference exactly one existing Robot. The database shall prevent the creation of AI requests that are not linked to a valid robot in the system.

**Challenges:** Maintaining referential integrity when inserting, updating, or deleting robot records that are referenced by AI requests.

**Assumptions:** All robots are registered in the Robot table before any AI requests are created. Each AI request is generated for one specific robot.

**Planned Approach:** Enforce using a FOREIGN KEY constraint on AIRequest.robot_id referencing Robot.robot_id
