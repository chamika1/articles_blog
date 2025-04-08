from app.utils.db import get_db
from bson import ObjectId

def make_user_admin(email):
    db = get_db()
    
    # First check if the user exists
    user = db.users.find_one({'email': email})
    
    if not user:
        print(f"User with email {email} not found in the database.")
        return
    
    # Check if user is already an admin
    if user.get('is_admin', False):
        print(f"User {email} is already an admin.")
        return
    
    # Make the user an admin
    result = db.users.update_one(
        {'email': email},
        {'$set': {'is_admin': True}}
    )
    
    if result.modified_count > 0:
        print(f"User {email} is now an admin!")
    else:
        print(f"Failed to update user status. Please try again.")

def list_users():
    db = get_db()
    users = list(db.users.find({}, {'email': 1, 'username': 1, 'is_admin': 1}))
    
    if not users:
        print("No users found in the database.")
        return
    
    print("\nAvailable users:")
    print("-" * 60)
    print(f"{'Email':<30} {'Username':<20} {'Admin Status'}")
    print("-" * 60)
    
    for user in users:
        email = user.get('email', 'N/A')
        username = user.get('username', 'N/A')
        is_admin = "Yes" if user.get('is_admin', False) else "No"
        print(f"{email:<30} {username:<20} {is_admin}")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) == 1:
        # No arguments, list all users
        list_users()
        print("\nUsage:")
        print("  python make_admin.py                  - List all users")
        print("  python make_admin.py <email>          - Make user an admin")
    elif len(sys.argv) == 2:
        email = sys.argv[1]
        make_user_admin(email)
    else:
        print("Usage: python make_admin.py [email]")
        sys.exit(1)