from database import get_connection

COLLECTION_SELECT = """
                SELECT 
                    c.id, 
                    c.driver_id, 
                    d.driver_name, 
                    c.vehicle_number, 
                    c.collection_date,
                    c.morning_trips, 
                    c.evening_trips, 
                    c.morning_collection, 
                    c.evening_collection,
                    c.fuel_expense, 
                    c.other_expense, 
                    c.total_trips, 
                    c.total_collection,
                    c.total_expense, 
                    c.net_collection, 
                    c.report_file_path, 
                    c.created_at
                FROM transport_collections c JOIN drivers d ON d.driver_id = c.driver_id
                """

class CollectionRepository:
    async def create(self, data: dict, totals):
        async with await get_connection() as connection:
            async with connection.cursor() as cursor:
                await cursor.execute(
                    """INSERT INTO transport_collections
                        (driver_id, 
                        vehicle_number, 
                        collection_date, 
                        morning_trips, 
                        evening_trips,
                        morning_collection, 
                        evening_collection, 
                        fuel_expense, 
                        other_expense,
                        total_trips, 
                        total_collection, 
                        total_expense, 
                        net_collection)
                        VALUES 
                        (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) 
                        RETURNING id
                        """,
                        (data["driver_id"], 
                         data["vehicle_number"], 
                         data["collection_date"],
                        data["morning_trips"], 
                        data["evening_trips"], 
                        data["morning_collection"],
                        data["evening_collection"], 
                        data["fuel_expense"], 
                        data["other_expense"],
                        totals.total_trips, 
                        totals.total_collection, 
                        totals.total_expense, 
                        totals.net_collection)
                )
                row = await cursor.fetchone()

        return await self.get_by_id(row["id"])

    async def get_by_id(self, collection_id: int):
        async with await get_connection() as connection:
            async with connection.cursor() as cursor:

                await cursor.execute(COLLECTION_SELECT + " WHERE c.id=%s", (collection_id,))
                
                return await cursor.fetchone()

    async def get_page(self, page: int, page_size: int, driver_id: int | None):
        where = " WHERE c.driver_id=%s" if driver_id is not None else ""
        params = (driver_id,) if driver_id is not None else ()
        offset = (page - 1) * page_size
        async with await get_connection() as connection:
            async with connection.cursor() as cursor:
                await cursor.execute("SELECT COUNT(*) AS total FROM transport_collections c" + where, params)
                total = (await cursor.fetchone())["total"]
                await cursor.execute(COLLECTION_SELECT + where + " ORDER BY c.collection_date DESC, c.id DESC LIMIT %s OFFSET %s", (*params, page_size, offset))
                items = await cursor.fetchall()
        return items, total

    async def update(self, collection_id: int, data: dict, totals):
        async with await get_connection() as connection:
            async with connection.cursor() as cursor:
                await cursor.execute(
                    """UPDATE transport_collections SET driver_id=%s, vehicle_number=%s, collection_date=%s,
                    morning_trips=%s, evening_trips=%s, morning_collection=%s, evening_collection=%s,
                    fuel_expense=%s, other_expense=%s, total_trips=%s, total_collection=%s,
                    total_expense=%s, net_collection=%s WHERE id=%s RETURNING id""",
                    (data["driver_id"], data["vehicle_number"], data["collection_date"], data["morning_trips"],
                     data["evening_trips"], data["morning_collection"], data["evening_collection"],
                     data["fuel_expense"], data["other_expense"], totals.total_trips,
                     totals.total_collection, totals.total_expense, totals.net_collection, collection_id)
                )
                row = await cursor.fetchone()
        return await self.get_by_id(row["id"]) if row else None

    async def update_report_path(self, collection_id: int, file_path: str):
        async with await get_connection() as connection:
            async with connection.cursor() as cursor:
                await cursor.execute("UPDATE transport_collections SET report_file_path=%s WHERE id=%s RETURNING id", (file_path, collection_id))
                return await cursor.fetchone()

    async def delete(self, collection_id: int):
        async with await get_connection() as connection:
            async with connection.cursor() as cursor:
                await cursor.execute("DELETE FROM transport_collections WHERE id=%s RETURNING id", (collection_id,))
                return await cursor.fetchone()
