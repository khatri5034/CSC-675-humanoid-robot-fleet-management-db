"""Simple smoke tests for milestone 4 models.

Run:
    python3 tests.py
"""

from models.models import Task, User


# create a new user in the database
user = User.create(UserName="test_user")

# get an existing user from the database with UserID=1
user1 = User.get(UserID=1)

# update the name of an existing user in the database
user1.UserName = "updated_test_user"
user1.save()

# get all users from the database
users = User.all()


# create a new task in the database
task = Task.create(
    TaskName="Inspect Battery",
    Description="Run battery health diagnostics",
    Priority="2",
    Status=0,
)

# get an existing task from the database with TaskID=1
task1 = Task.get(TaskID=1)

# update the status of an existing task in the database
task1.Status = 1
task1.save()

# get all tasks from the database
tasks = Task.all()


print("Simple model smoke tests executed.")
print(f"Users fetched: {len(users)}")
print(f"Tasks fetched: {len(tasks)}")

