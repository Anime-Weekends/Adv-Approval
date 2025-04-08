from pymongo import MongoClient
from config import MONGO_URI

client = MongoClient(MONGO_URI)
db = client["AutoApprovalBot"]

users_col = db["users"]
admins_col = db["admins"]
channels_col = db["channels"]

# Users
def add_user(user_id):
    if not users_col.find_one({"user_id": user_id}):
        users_col.insert_one({"user_id": user_id})

def get_all_users():
    return [user["user_id"] for user in users_col.find()]

def total_users():
    return users_col.count_documents({})

# Admins
def add_admin(user_id):
    if not admins_col.find_one({"user_id": user_id}):
        admins_col.insert_one({"user_id": user_id})

def remove_admin(user_id):
    admins_col.delete_one({"user_id": user_id})

def is_admin(user_id):
    return admins_col.find_one({"user_id": user_id}) is not None

def get_admins():
    return [admin["user_id"] for admin in admins_col.find()]

# Channels/Groups
def add_connected_chat(user_id, chat_id, chat_title):
    if not channels_col.find_one({"user_id": user_id, "chat_id": chat_id}):
        channels_col.insert_one({
            "user_id": user_id,
            "chat_id": chat_id,
            "chat_title": chat_title
        })

def get_user_channels(user_id):
    return channels_col.find({"user_id": user_id})
