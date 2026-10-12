from database import get_connection


class DriverRepository:

    async def create(self, data: dict):
        async with await get_connection() as connection:
            async with connection.cursor() as cursor:
                await cursor.execute(
                    '''
                    INSERT INTO drivers (
                        driver_name,
                        phone_number,
                        is_active
                    )
                    VALUES (%s, %s, %s)
                    RETURNING
                        driver_id,
                        driver_name,
                        phone_number,
                        is_active
                    ''',
                    (
                        data["driver_name"],
                        data["phone_number"],
                        data["is_active"]
                    )
                )
                return await cursor.fetchone()

    async def get_all(self):
        async with await get_connection() as connection:
            async with connection.cursor() as cursor:
                await cursor.execute(
                    '''
                    SELECT
                        driver_id,
                        driver_name,
                        phone_number,
                        is_active
                    FROM drivers
                    ORDER BY driver_id
                    '''
                )
                return await cursor.fetchall()

    async def get_by_id(self, driver_id: int):
        async with await get_connection() as connection:
            async with connection.cursor() as cursor:
                await cursor.execute(
                    '''
                    SELECT
                        driver_id,
                        driver_name,
                        phone_number,
                        is_active
                    FROM drivers
                    WHERE driver_id = %s    
                    ''',
                    (driver_id,)
                )
                return await cursor.fetchone()


    async def update(self, driver_id: int, data: dict):
        allowed_fields = {"driver_name", "phone_number", "is_active"}
        data = {key: value for key, value in data.items() if key in allowed_fields}

        if not data:
            return await self.get_by_id(driver_id)

        set_clause = ", ".join(f"{key} = %s" for key in data)
        values = list(data.values()) + [driver_id]  

        async with await get_connection() as connection:
            async with connection.cursor() as cursor:
                await cursor.execute(
                    f"""
                    UPDATE drivers
                    SET {set_clause}
                    WHERE driver_id = %s
                    RETURNING
                        driver_id,
                        driver_name,
                        phone_number,
                        is_active
                    """,
                    values
                )
                return await cursor.fetchone()


    async def delete(self, driver_id: int):
        async with await get_connection() as connection:
            async with connection.cursor() as cursor:
                await cursor.execute(
                    '''
                    DELETE FROM drivers
                    WHERE driver_id = %s
                    RETURNING driver_id
                    ''',
                    (driver_id,)
                )
                return await cursor.fetchone()