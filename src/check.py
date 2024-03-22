from app import app, db
from app.models import User

# Create an application context
app_ctx = app.app_context()
app_ctx.push()

try:
    # Your database query code goes here
    # For example, querying all users and printing their information
    all_users = User.query.all()
    for user in all_users:
        print(f"User ID: {user.id}, Name: {user.name}, Creation Date: {user.creation_date}")

finally:
    # Pop the application context to clean up resources
    app_ctx.pop()