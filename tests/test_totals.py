from decimal import Decimal
from services.collection_service import CollectionService

def test_calculate_totals():
    data = {"morning_trips": 4, 
            "evening_trips": 3,
            "morning_collection": Decimal("1200.00"), 
            "evening_collection": Decimal("900.00"),
            "fuel_expense": Decimal("500.00"), 
            "other_expense": Decimal("100.00")
            }
    totals = CollectionService.calculate_totals(data)
    assert totals.total_trips == 7
    assert totals.total_collection == Decimal("2100.00")
    assert totals.total_expense == Decimal("600.00")
    assert totals.net_collection == Decimal("1500.00")
