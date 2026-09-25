from app.utils.categorizer import predict_category


def test_food_category():
    result = predict_category("Coffee and snacks", "Starbucks")
    assert result == "Food"


def test_travel_category():
    result = predict_category("Bus pass", "MSRTC")
    assert result == "Travel"


def test_bills_category():
    result = predict_category("Electric bill", "Tata Power")
    assert result == "Bills"


def test_uber_category():
    result = predict_category("Office commute", "Uber")
    assert result == "Travel"


def test_mcdonalds_category():
    result = predict_category("Dinner", "McDonalds")
    assert result == "Food"