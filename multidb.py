# ------------------------- #
# Don't Remove Credit 
# Owner @Mr_Mohammed_29
# ------------------------- #

from motor.motor_asyncio import AsyncIOMotorClient

databases = {}
clients = {}
active_db = None

# ------------------------- #
# Don't Remove Credit 
# Owner @Mr_Mohammed_29
# ------------------------- #

async def load_database(uri, name):

    global active_db

    client = AsyncIOMotorClient(uri)

    db = client["FileStoreBot"]

    # Test connection
    await client.admin.command("ping")

    clients[name] = client
    databases[name] = db

    if active_db is None:
        active_db = name
        
# ------------------------- #
# Don't Remove Credit 
# Owner @Mr_Mohammed_29
# ------------------------- #

def switch_database(name):

    global active_db

    if name in databases:
        active_db = name
        return True

    return False

# ------------------------- #
# Don't Remove Credit 
# Owner @Mr_Mohammed_29
# ------------------------- #

def get_database():

    if active_db is None:
        return None

    return databases[active_db]

# ------------------------- #
# Don't Remove Credit 
# Owner @Mr_Mohammed_29
# ------------------------- #

def get_active_database():

    return active_db

# ------------------------- #
# Don't Remove Credit 
# Owner @Mr_Mohammed_29
# ------------------------- #

def database_list():

    return list(databases.keys())

# ------------------------- #
# Don't Remove Credit 
# Owner @Mr_Mohammed_29
# ------------------------- #

def has_database(name):

    return name in databases
    
# ------------------------- #
# Don't Remove Credit 
# Owner @Mr_Mohammed_29
# ------------------------- #

def total_databases():

    return len(databases)

# ------------------------- #
# Don't Remove Credit 
# Owner @Mr_Mohammed_29
# ------------------------- #

async def remove_database(name):

    global active_db

    if name not in databases:
        return False

    clients[name].close()

    del clients[name]
    del databases[name]

    if active_db == name:

        if databases:
            active_db = list(databases.keys())[0]
        else:
            active_db = None

    return True

# ------------------------- #
# Don't Remove Credit 
# Owner @Mr_Mohammed_29
# ------------------------- #

async def database_status():

    status = []

    for name, client in clients.items():

        try:
            await client.admin.command("ping")

            state = "ONLINE"

        except Exception:

            state = "OFFLINE"

        status.append(
            {
                "name": name,
                "status": state
            }
        )

    return status

# ------------------------- #
# Don't Remove Credit 
# Owner @Mr_Mohammed_29
# ------------------------- #