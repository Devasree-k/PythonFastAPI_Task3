# Transport Collection Management API

FastAPI + PostgreSQL project for managing drivers and daily transport collections.

## Setup
1. Create a NEW PostgreSQL database named `transport_collection_db`. Do not use your old database.
2. Copy `.env.example` to `.env` and replace the database password.
3. Activate your virtual environment and run `python -m pip install -r requirements.txt`.
4. Run `schema.sql` against the new database in pgAdmin or psql.
5. Start the API: `python -m uvicorn main:app --reload`
6. Open `http://127.0.0.1:8000/docs`.

## Endpoints
- `POST /drivers/` create a driver
- `GET /drivers/` list drivers
- `GET /drivers/{driver_id}` get one driver
- `PUT /drivers/{driver_id}` update a driver
- `DELETE /drivers/{driver_id}` delete if no collection records refer to the driver
- `POST /collections/` create a daily collection
- `GET /collections/?page=1&page_size=10` paginated collection list
- `GET /collections/?driver_id=1` filter by driver
- `GET /collections/{collection_id}` get one collection
- `PUT /collections/{collection_id}` update a collection
- `DELETE /collections/{collection_id}` delete a collection
- `POST /collections/{collection_id}/report` upload a PDF/JPG/PNG report (5 MB max)

## Example driver request
```json
{"driver_name":"Arun Kumar","phone_number":"9876543210","is_active":true}
```

## Example collection request
```json
{
  "driver_id": 1,
  "vehicle_number": "TN38AB1234",
  "collection_date": "2026-10-09",
  "morning_trips": 5,
  "evening_trips": 4,
  "morning_collection": "2500.00",
  "evening_collection": "2200.00",
  "fuel_expense": "900.00",
  "other_expense": "150.00"
}
```
Calculated totals are computed by the API; do not send them in the request.

The file itself is saved under `uploads/reports`; only its path is stored in PostgreSQL. In a public production deployment, add authentication, authorization, and file-content validation.

Run the calculation test with `python -m pytest`.
