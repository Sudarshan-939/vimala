from pymongo import MongoClient
import bcrypt

# Connect to MongoDB
client = MongoClient('mongodb+srv://ys7709995_db_user:M4mnir5IzF1AjMJv@vimala.9c8xz3l.mongodb.net/?appName=Vimala')
db = client['cine_rental']

def update_admin_password():
    print("Updating admin password to use bcrypt hashing...")
    
    # Hash the password
    hashed_password = bcrypt.hashpw('vimala'.encode('utf-8'), bcrypt.gensalt())
    
    # Update the admin user
    result = db.users.update_one(
        {'email': 'vimala', 'role': 'admin'},
        {'$set': {'password': hashed_password}}
    )
    
    if result.modified_count > 0:
        print("✓ Admin password successfully updated with bcrypt hash!")
    else:
        print("Admin user not found or password already hashed.")

if __name__ == '__main__':
    update_admin_password()
