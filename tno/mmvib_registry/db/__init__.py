import sys

from tno.mmvib_registry.db.base import RegistryDB
from tno.mmvib_registry.db.memorydb import MemoryDB
from tno.mmvib_registry.db.sqldb import SqlDB
from tno.mmvib_registry.settings import EnvSettings

registrydb: RegistryDB
# create a singleton for this DB
if EnvSettings.db_type() == "postgres":
    registrydb = SqlDB()
elif EnvSettings.db_type() == "memorydb":
    registrydb = MemoryDB()
else:
    print(f"ERROR: Unknown DB type set: {EnvSettings.db_type()}")
    sys.exit(1)
