"""Simple smoke tests for milestone 4 models.

Run:
    python3 tests.py
"""

from models.models import Tasks, Users


# create a new user in the database
user = Users.create(UserName="test_user")

# get an existing user from the database with UserID=1
user1 = Users.get(UserID=1)

# update the name of an existing user in the database
user1.UserName = "updated_test_user"
user1.save()

# get all users from the database
users = Users.all()


# create a new task in the database
task = Tasks.create(
    TaskName="Inspect Battery",
    Description="Run battery health diagnostics",
    Priority="2",
    Status=0,
)

# get an existing task from the database with TaskID=1
task1 = Tasks.get(TaskID=1)

# update the status of an existing task in the database
task1.Status = 1
task1.save()

# get all tasks from the database
tasks = Tasks.all()


# print("Simple model  tests executed.")
# print(f"Users fetched: {len(users)}")
# print(f"Tasks fetched: {len(tasks)}")

task = Tasks.get(TaskID=1)
print(task)

