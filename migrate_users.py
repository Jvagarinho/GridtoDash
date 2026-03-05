"""
Migration script: Transfer users from local dev storage to MongoDB
Run this after configuring MongoDB in secrets.toml
"""

import json
import os
from pymongo import MongoClient
import streamlit as st

def migrate_users():
    """Migrate users from .dev_users.json to MongoDB"""
    
    # Check if dev database exists
    dev_db_file = ".dev_users.json"
    if not os.path.exists(dev_db_file):
        print("No development database found.")
        return False
    
    # Load dev users
    with open(dev_db_file, 'r') as f:
        dev_users = json.load(f)
    
    if not dev_users:
        print("Development database is empty.")
        return False
    
    print(f"Found {len(dev_users)} users in development database.")
    
    # Get MongoDB connection from Streamlit secrets
    try:
        MONGODB_URI = st.secrets["MONGODB_URI"]
        MONGODB_DB = st.secrets.get("MONGODB_DB", "gridtodash")
    except Exception:
        print("ERROR: MongoDB not configured in .streamlit/secrets.toml")
        print("Please configure MONGODB_URI first.")
        return False
    
    # Connect to MongoDB
    try:
        client = MongoClient(MONGODB_URI, serverSelectionTimeoutMS=10000)
        client.admin.command('ping')
        db = client[MONGODB_DB]
        collection = db.users
        print("✅ Connected to MongoDB")
    except Exception as e:
        print(f"❌ MongoDB connection error: {e}")
        return False
    
    # Migrate each user
    migrated_count = 0
    for user in dev_users:
        # Check if user already exists
        existing = collection.find_one({"email": user["email"]})
        if existing:
            print(f"  ⚠️  User {user['email']} already exists, skipping...")
            continue
        
        # Insert user (remove local _id if present)
        user_doc = user.copy()
        if '_id' in user_doc:
            del user_doc['_id']  # Let MongoDB generate its own _id
        
        try:
            collection.insert_one(user_doc)
            migrated_count += 1
            print(f"  ✅ Migrated: {user['email']}")
        except Exception as e:
            print(f"  ❌ Error migrating {user['email']}: {e}")
    
    print(f"\n✅ Migration complete! {migrated_count} users migrated.")
    
    # Backup dev database
    backup_file = ".dev_users_backup.json"
    with open(backup_file, 'w') as f:
        json.dump(dev_users, f, indent=2)
    print(f"📦 Development database backed up to: {backup_file}")
    
    return True

if __name__ == "__main__":
    # This script should be run with: streamlit run migrate_users.py
    # But we need to set up Streamlit context for secrets
    import sys
    sys.path.append('.')
    
    # Check if running in Streamlit
    try:
        # This will only work when run through Streamlit
        success = migrate_users()
        if success:
            print("\n✅ Migration successful! You can now use MongoDB.")
            print("Don't forget to restart the app.")
        else:
            print("\n❌ Migration failed or no data to migrate.")
    except Exception as e:
        print(f"Error: {e}")
        print("\nTo run this script properly, use:")
        print("  streamlit run migrate_users.py")
