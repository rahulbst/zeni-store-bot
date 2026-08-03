# ------------------------- #
# Don't Remove Credit 
# Ask Doubt @AU_Bot_Discussion 
# Owner @Mr_Mohammed_29 
# ------------------------- #

from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import DESCENDING
from config import MONGO_URI
from datetime import datetime

# ------------------------- #
# Don't Remove Credit 
# Owner @Mr_Mohammed_29
# ------------------------- #

import time

# ------------------------- #
# Don't Remove Credit 
# Owner @Mr_Mohammed_29
# ------------------------- #

client = AsyncIOMotorClient(MONGO_URI)
db = client.filebot
db = client["FileStoreBot"]
multi_db = db["multi_database"]
db_settings = db["db_settings"]

# ------------------------- #
# Don't Remove Credit 
# Owner @Mr_Mohammed_29
# ------------------------- #

files = db.files
users = db.users
admins = db["admins"]
forcesubs = db["forcesubs"]
banned = db["banned"]
stats = db["stats"]
word_filters = db["word_filters"]

# ------------------------- #
# Don't Remove Credit 
# Owner @Mr_Mohammed_29
# ------------------------- #

# FILES
async def save_file(
    file_id,
    file_unique_id,
    file_type,
    caption="",
    thumb=None,
    file_name="",
    file_size=0,
    uploader_id=0
):

    data = {
        "file_id": file_id,
        "file_unique_id": file_unique_id,
        "file_type": file_type,
        "caption": caption,
        "thumb": thumb,
        "file_name": file_name,
        "file_size": file_size,
        "uploader_id": uploader_id,
        "upload_time": int(time.time()),
        "download_count": 0
    }

    await files.update_one(
        {"file_unique_id": file_unique_id},
        {"$set": data},
        upsert=True
    )
    
# ------------------------- #
# Don't Remove Credit 
# Owner @Mr_Mohammed_29
# ------------------------- #

async def get_file(file_unique_id):
    return await files.find_one({"file_unique_id": file_unique_id})
    
# ------------------------- #
# Don't Remove Credit 
# Owner @Mr_Mohammed_29
# ------------------------- #

# USERS
async def add_user(user_id):
    # FIX (new-user log spam): previously this returned nothing, so
    # bot.py had no way to know whether a user was genuinely new or
    # already existed - it just sent a "new user" log on every /start.
    # Now we return True only when a document was actually INSERTED
    # (upserted_id is set), and False when it already existed / no
    # user_id was given.
    if not user_id:
        return False

    result = await users.update_one(
        {"user_id": int(user_id)},
        {"$setOnInsert": {"user_id": int(user_id)}},
        upsert=True
    )

    return result.upserted_id is not None
    
# ------------------------- #
# Don't Remove Credit 
# Owner @Mr_Mohammed_29
# ------------------------- #

async def get_all_users():
    return [u["user_id"] async for u in users.find({}, {"user_id": 1, "_id": 0})]
    
# ------------------------- #
# Don't Remove Credit 
# Owner @Mr_Mohammed_29
# ------------------------- #

async def total_users():
    return await users.count_documents({})

# ------------------------- #
# Don't Remove Credit 
# Owner @Mr_Mohammed_29
# ------------------------- #

# ADMIN SYSTEM

async def add_admin_db(user_id, name, username):

    user_id = int(user_id)

    await admins.update_one(
        {"user_id": user_id},
        {"$set": {
            "user_id": user_id,
            "name": name,
            "username": username,
            "joined_date": datetime.utcnow()
        }},
        upsert=True
    )

# ------------------------- #
# Don't Remove Credit 
# Owner @Mr_Mohammed_29
# ------------------------- #

async def get_all_admins():
    admins_list = []
    async for admin in admins.find({}, {"_id": 0}):
        admins_list.append(admin)
    return admins_list
    
# ------------------------- #
# Don't Remove Credit 
# Owner @Mr_Mohammed_29
# ------------------------- #

async def remove_admin_db(user_id):
    await admins.delete_one({"user_id": int(user_id)})

# ------------------------- #
# Don't Remove Credit 
# Owner @Mr_Mohammed_29
# ------------------------- #

async def is_admin(user_id):
    return await admins.find_one({"user_id": int(user_id)}) is not None

async def total_admins():
    return await admins.count_documents({})
# ------------------------- #
# Don't Remove Credit 
# Owner @Mr_Mohammed_29
# ------------------------- #

async def add_force_sub(channel):

    await forcesubs.update_one(
        {"channel": str(channel)},
        {"$set": {"channel": str(channel)}},
        upsert=True
    )
# ------------------------- #
# Don't Remove Credit 
# Owner @Mr_Mohammed_29
# ------------------------- #

async def remove_force_sub(channel):

    await forcesubs.delete_many(
        {
            "channel": {
                "$in": [
                    str(channel),
                    str(channel).replace("@", "")
                ]
            }
        }
    )

# ------------------------- #
# Don't Remove Credit 
# Owner @Mr_Mohammed_29
# ------------------------- #

async def get_force_subs():

    channels = []

    async for ch in forcesubs.find({}, {"_id": 0}):
        channels.append(ch["channel"])

    return channels
    
# ------------------------- #
# Don't Remove Credit 
# Owner @Mr_Mohammed_29
# ------------------------- #

verify_db = db.verify_cache


async def save_verify(user_id, param):
    await verify_db.update_one(
        {"user_id": user_id},
        {"$set": {"param": param}},
        upsert=True
    )

# ------------------------- #
# Don't Remove Credit 
# Owner @Mr_Mohammed_29
# ------------------------- #

async def get_verify(user_id):
    data = await verify_db.find_one({"user_id": user_id})
    if data:
        return data.get("param")
    return None

# ------------------------- #
# Don't Remove Credit 
# Owner @Mr_Mohammed_29
# ------------------------- #

async def delete_verify(user_id):
    await verify_db.delete_one({"user_id": user_id})

# ------------------------- #
# Don't Remove Credit 
# Owner @Mr_Mohammed_29
# ------------------------- #

# ------------------------- #
# BAN SYSTEM
# ------------------------- #

async def ban_user(user_id):
    await banned.update_one(
        {"user_id": int(user_id)},
        {"$set": {"user_id": int(user_id)}},
        upsert=True
    )

# ------------------------- #
# Don't Remove Credit 
# Owner @Mr_Mohammed_29
# ------------------------- #

async def unban_user(user_id):
    await banned.delete_one({"user_id": int(user_id)})

# ------------------------- #
# Don't Remove Credit 
# Owner @Mr_Mohammed_29
# ------------------------- #

async def is_banned(user_id):
    return await banned.find_one({"user_id": int(user_id)}) is not None

# ------------------------- #
# Don't Remove Credit 
# Owner @Mr_Mohammed_29
# ------------------------- #

async def get_banned_users():
    users = []
    async for user in banned.find({}, {"_id": 0}):
        users.append(user["user_id"])
    return users

# ------------------------- #
# Don't Remove Credit 
# Owner @Mr_Mohammed_29
# ------------------------- #

# ------------------------- #
# FILE MANAGEMENT
# ------------------------- #

async def get_file_by_unique_id(file_unique_id):
    return await files.find_one(
        {"file_unique_id": file_unique_id}
    )

async def total_files():
    return await files.count_documents({})

# ------------------------- #
# Don't Remove Credit 
# Owner @Mr_Mohammed_29
# ------------------------- #

# ------------------------- #
# DOWNLOAD COUNT
# ------------------------- #

async def increase_download(file_unique_id):

    await files.update_one(
        {"file_unique_id": file_unique_id},
        {
            "$inc": {
                "download_count": 1
            }
        }
    )

# ------------------------- #
# Don't Remove Credit 
# Owner @Mr_Mohammed_29
# ------------------------- #

# ------------------------- #
# TODAY FILES
# ------------------------- #

async def today_files():

    now = int(time.time())

    start = now - 86400

    return await files.count_documents(
        {
            "upload_time": {
                "$gte": start
            }
        }
    )

# ------------------------- #
# Don't Remove Credit 
# Owner @Mr_Mohammed_29
# ------------------------- #

# ------------------------- #
# WEEK FILES
# ------------------------- #

async def week_files():

    now = int(time.time())

    start = now - (7 * 86400)

    return await files.count_documents(
        {
            "upload_time": {
                "$gte": start
            }
        }
    )

# ------------------------- #
# Don't Remove Credit 
# Owner @Mr_Mohammed_29
# ------------------------- #

# =====================================================
# Multi Database Functions
# =====================================================

async def add_database(name, mongo_uri):

    await multi_db.update_one(
        {"name": name},
        {
            "$set": {
                "name": name,
                "mongo_uri": mongo_uri,
                "status": "ONLINE"
            }
        },
        upsert=True
    )

# ------------------------- #
# Don't Remove Credit 
# Owner @Mr_Mohammed_29
# ------------------------- #

async def remove_database(name):

    await multi_db.delete_one(
        {"name": name}
    )

# ------------------------- #
# Don't Remove Credit 
# Owner @Mr_Mohammed_29
# ------------------------- #

async def get_database(name):

    return await multi_db.find_one(
        {"name": name}
    )

# ------------------------- #
# Don't Remove Credit 
# Owner @Mr_Mohammed_29
# ------------------------- #

async def get_all_databases():

    data = []

    async for db in multi_db.find():

        data.append(db)

    return data

# ------------------------- #
# Don't Remove Credit 
# Owner @Mr_Mohammed_29
# ------------------------- #

async def set_active_database(name):

    await db_settings.update_one(
        {"_id": "active_db"},
        {
            "$set": {
                "name": name
            }
        },
        upsert=True
    )
    
# ------------------------- #
# Don't Remove Credit 
# Owner @Mr_Mohammed_29
# ------------------------- #

async def get_active_database():

    data = await db_settings.find_one(
        {"_id": "active_db"}
    )

    if data:

        return data["name"]

    return None

# ------------------------- #
# Don't Remove Credit 
# Owner @Mr_Mohammed_29
# ------------------------- #

# ------------------------- #
# LINK STATS
# ------------------------- #

async def increase_single_links():
    await stats.update_one(
        {"_id": "links"},
        {"$inc": {"single_links": 1}},
        upsert=True
    )
    
# ------------------------- #
# Don't Remove Credit 
# Owner @Mr_Mohammed_29
# ------------------------- #

async def increase_batch_links():
    await stats.update_one(
        {"_id": "links"},
        {"$inc": {"batch_links": 1}},
        upsert=True
    )

# ------------------------- #
# Don't Remove Credit 
# Owner @Mr_Mohammed_29
# ------------------------- #

async def get_link_stats():
    data = await stats.find_one({"_id": "links"})

    if not data:
        return 0, 0

    return (
        data.get("single_links", 0),
        data.get("batch_links", 0)
    )

# ------------------------- #
# Don't Remove Credit 
# Owner @Mr_Mohammed_29
# ------------------------- #

# ------------------------- #
# CONTENT PROTECTION SYSTEM
# ------------------------- #
# Jab ON ho, delivered files forward/save/share
# nahi ki ja sakengi (Telegram's protect_content).
# Default: OFF (agar kabhi set na kiya gaya ho).
# ------------------------- #

async def set_protect_content(status: bool):

    await db_settings.update_one(
        {"_id": "protect_content"},
        {"$set": {"enabled": bool(status)}},
        upsert=True
    )

# ------------------------- #
# Don't Remove Credit 
# Owner @Mr_Mohammed_29
# ------------------------- #

async def get_protect_content():

    data = await db_settings.find_one({"_id": "protect_content"})

    if data and "enabled" in data:
        return data["enabled"]

    return False

# ------------------------- #
# Don't Remove Credit 
# Owner @Mr_Mohammed_29
# ------------------------- #

# ------------------------- #
# AUTO DELETE TIME SYSTEM
# ------------------------- #
# Admin jitne minutes set karega, files delivery ke
# baad utne time me automatically delete ho jayengi.
# Default: 5 minutes agar kabhi set nahi kiya gaya ho.
# ------------------------- #

async def set_delete_time(minutes):

    await db_settings.update_one(
        {"_id": "delete_time"},
        {"$set": {"minutes": float(minutes)}},
        upsert=True
    )

# ------------------------- #
# Don't Remove Credit 
# Owner @Mr_Mohammed_29
# ------------------------- #

async def get_delete_time():

    data = await db_settings.find_one({"_id": "delete_time"})

    if data and "minutes" in data:
        return data["minutes"]

    return 5

# ------------------------- #
# Don't Remove Credit 
# Owner @Mr_Mohammed_29
# ------------------------- #

# ------------------------- #
# WORD FILTER SYSTEM
# ------------------------- #
# Har word/tag jo yaha add hoga, wo caption se
# automatically remove ho jayega jab file deliver hogi.
# ------------------------- #

async def add_word_filter(word):

    await word_filters.update_one(
        {"word": word.lower()},
        {"$set": {"word": word.lower()}},
        upsert=True
    )

# ------------------------- #
# Don't Remove Credit 
# Owner @Mr_Mohammed_29
# ------------------------- #

async def remove_word_filter(word):

    await word_filters.delete_one(
        {"word": word.lower()}
    )

# ------------------------- #
# Don't Remove Credit 
# Owner @Mr_Mohammed_29
# ------------------------- #

async def get_word_filters():

    result = []

    async for w in word_filters.find({}, {"_id": 0}):
        result.append(w["word"])

    return result

# ------------------------- #
# Don't Remove Credit 
# Owner @Mr_Mohammed_29
# ------------------------- #

# ------------------------- #
# FILENAME FILTER SYSTEM
# ------------------------- #
# Word_filters caption se text hatate hain, lekin filename
# alag hota hai. Yeh naya set sirf FILE NAME me se text/tag
# hatane ke liye hai (real rename ke liye /setrename bhi on
# karna padega, warna sirf caption/display pe reflect hoga).
# ------------------------- #

name_filters = db["name_filters"]

async def add_name_filter(word):

    await name_filters.update_one(
        {"word": word.lower()},
        {"$set": {"word": word.lower()}},
        upsert=True
    )

# ------------------------- #
# Don't Remove Credit 
# Owner @Mr_Mohammed_29
# ------------------------- #

async def remove_name_filter(word):

    await name_filters.delete_one(
        {"word": word.lower()}
    )

# ------------------------- #
# Don't Remove Credit 
# Owner @Mr_Mohammed_29
# ------------------------- #

async def get_name_filters():

    result = []

    async for w in name_filters.find({}, {"_id": 0}):
        result.append(w["word"])

    return result

# ------------------------- #
# Don't Remove Credit 
# Owner @Mr_Mohammed_29
# ------------------------- #

# ------------------------- #
# REAL RENAME TOGGLE
# ------------------------- #
# OFF (default): fast delivery, file_id reuse - filename
# filters sirf caption/display level pe kaam karte hain
# (Telegram document/audio ka real filename change nahi
# hota kyunki woh file ke andar hi baked hota hai).
# ON: bot file download karke naye (cleaned) naam se
# re-upload karega - real filename change hoga, lekin
# thoda extra time/bandwidth lagega.
# ------------------------- #

async def set_rename_enabled(status: bool):

    await db_settings.update_one(
        {"_id": "rename_enabled"},
        {"$set": {"enabled": bool(status)}},
        upsert=True
    )

# ------------------------- #
# Don't Remove Credit 
# Owner @Mr_Mohammed_29
# ------------------------- #

async def get_rename_enabled():

    data = await db_settings.find_one({"_id": "rename_enabled"})

    if data and "enabled" in data:
        return data["enabled"]

    return False

# ------------------------- #
# Don't Remove Credit 
# Owner @Mr_Mohammed_29
# ------------------------- #
