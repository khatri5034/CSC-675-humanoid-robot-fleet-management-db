# Milestone 4 tests — run: cd milestones/milestone4 && python tests.py
#
# Inserts: optional 2nd DeploymentLocations row, 3 Robots, 3 Tasks, 3 TaskAssignments.
# Uses UserID 1 and 2; robots 1–2 of this run share dep1 + user 1; robot 3 uses dep2 + user 2.
# Lazy/backref need Relationship -> Base.get(**kwargs); orm/relationships.py uses that form.

import os
import sys
from datetime import datetime

_ROOT = os.path.dirname(os.path.abspath(__file__))
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)

from models.models import DeploymentLocations, Robots, TaskAssignments, Tasks, Users


def from_cache(instance, attr_name):
    return hasattr(instance, f"_{attr_name}_cache")


print("========== Users 1 and 2 ==========")
user1 = Users.get(UserID=1)
user2 = Users.get(UserID=2)
print("Users.get(UserID=1):", user1)
print("Users.get(UserID=2):", user2)
if user1 is None or user2 is None:
    raise SystemExit("Need both UserID=1 and UserID=2 in the database.")

print("\n========== Deployment locations 1 and 2 (create second site if DB only has one) ==========")
locs = DeploymentLocations.all()
ids = sorted({L.DeploymentLocationID for L in locs})
dep1 = ids[0] if ids else 1
if len(ids) >= 2:
    dep2 = ids[1]
else:
    extra = DeploymentLocations.create(EnvironmentType="WAREHOUSE", AddressID=1)
    dep2 = extra.DeploymentLocationID
    print("created second deployment:", extra)
print("using DeploymentLocationID dep1=", dep1, "dep2=", dep2)

print("\n========== Create Robots 1–3 (User 1: R1+R2 at dep1; User 2: R3 at dep2) ==========")
template = Robots.get(RobotID=1)
if template is None:
    raise SystemExit("Need at least Robots(RobotID=1) as template for FKs (role, model, software).")

robot1 = Robots.create(
    RobotRoleID=template.RobotRoleID,
    RobotModelID=template.RobotModelID,
    SoftwareVersionID=template.SoftwareVersionID,
    UserID=1,
    DeploymentLocationID=dep1,
)
robot2 = Robots.create(
    RobotRoleID=template.RobotRoleID,
    RobotModelID=template.RobotModelID,
    SoftwareVersionID=template.SoftwareVersionID,
    UserID=1,
    DeploymentLocationID=dep1,
)
robot3 = Robots.create(
    RobotRoleID=template.RobotRoleID,
    RobotModelID=template.RobotModelID,
    SoftwareVersionID=template.SoftwareVersionID,
    UserID=2,
    DeploymentLocationID=dep2,
)
print("created:", robot1)
print("created:", robot2)
print("created:", robot3)

print("\n========== Create Tasks 1–3 + TaskAssignments (same pattern: TA1–2 user 1 + robots 1–2; TA3 user 2 + robot 3) ==========")
task1 = Tasks.create(TaskName="Demo task 1", Description="test", Priority="1", Status=0)
task2 = Tasks.create(TaskName="Demo task 2", Description="test", Priority="2", Status=0)
task3 = Tasks.create(TaskName="Demo task 3", Description="test", Priority="3", Status=0)
print("created:", task1)
print("created:", task2)
print("created:", task3)

now = datetime.now()
ta1 = TaskAssignments.create(RobotID=robot1.RobotID, UserID=1, TaskID=task1.TaskID, AssignedAt=now)
ta2 = TaskAssignments.create(RobotID=robot2.RobotID, UserID=1, TaskID=task2.TaskID, AssignedAt=now)
ta3 = TaskAssignments.create(RobotID=robot3.RobotID, UserID=2, TaskID=task3.TaskID, AssignedAt=now)
print("created:", ta1)
print("created:", ta2)
print("created:", ta3)

print("\n========== Lazy load + cache (Relationship on Robots.owner_user) ==========")
print("robot1 before owner_user | from_cache?", from_cache(robot1, "owner_user"))
u_a = robot1.owner_user
print("robot1 after 1st owner_user | from_cache?", from_cache(robot1, "owner_user"), "|", u_a)
print("robot1 after 2nd owner_user | same object?", u_a is robot1.owner_user)

print("\n========== Backref (Robots.owner_user -> setattr(user, 'robots', robot)) ==========")
owner_of_r1 = robot1.owner_user
print("owner_of_r1 from robot1.owner_user:", owner_of_r1)
print("backref owner_of_r1.robots is robot1?", getattr(owner_of_r1, "robots", None) is robot1)
owner_of_r3 = robot3.owner_user
print("owner_of_r3 from robot3.owner_user:", owner_of_r3)
print("backref owner_of_r3.robots is robot3?", getattr(owner_of_r3, "robots", None) is robot3)

print("\n========== One-to-many: all robots per deployment (Robots.filter) ==========")
print("This run's robots:", robot1, robot2, robot3)
loc1_rows = Robots.filter(DeploymentLocationID=dep1)
loc2_rows = Robots.filter(DeploymentLocationID=dep2)
print(f"DeploymentLocationID={dep1} (all rows in DB) -> {len(loc1_rows)} robot(s)")
print(f"DeploymentLocationID={dep2} (all rows in DB) -> {len(loc2_rows)} robot(s)")
print(f"  at dep1 among this run: robot1 & robot2 -> UserID 1")
print(f"  at dep2 among this run: robot3 -> UserID 2")

print("\n========== One-to-many: robots owned by user (Robots.filter by UserID) ==========")
for uid, label in ((1, "User 1"), (2, "User 2")):
    rows = Robots.filter(UserID=uid)
    print(f"{label} (UserID={uid}) -> {len(rows)} robot(s) in this run (includes older rows if any):")
    for r in rows[-5:]:
        print(" ", r)

print("\n========== TaskAssignments: lazy robot + user ==========")
print("ta1 before robot | from_cache?", from_cache(ta1, "robot"))
print("ta1.robot:", ta1.robot, "| from_cache after?", from_cache(ta1, "robot"))
print("ta1.robot again same object?", ta1.robot is ta1.robot)

print("\nDone.")
