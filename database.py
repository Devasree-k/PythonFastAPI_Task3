# import psycopg
# from psycopg.rows import dict_row
# from config import settings

# async def get_connection():
#     return await psycopg.AsyncConnection.connect(settings.database_url, row_factory=dict_row)

import psycopg
from psycopg.rows import dict_row
from config import settings

async def get_connection():
    return await psycopg.AsyncConnection.connect(
        host=settings.db_host,
        port=settings.db_port,
        dbname=settings.db_name,
        user=settings.db_user,
        password=settings.db_password,
        row_factory=dict_row
    )
