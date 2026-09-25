import io
from unittest.mock import MagicMock, patch

from app.main import app


def test_successful_csv_upload():
    # Create Flask test client
    client = app.test_client()

    # Sample valid CSV
    csv_content = """description,merchant,amount,date,payment_method,notes
Coffee and snacks,Starbucks,250,2025-01-08,UPI,Evening snacks
Office commute,Uber,120,2025-01-02,UPI,Office travel
"""

    # Mock MySQL connection
    mock_connection = MagicMock()
    mock_cursor = MagicMock()

    # Simulate MySQL auto-increment ID
    mock_cursor.lastrowid = 101

    mock_connection.cursor.return_value = mock_cursor

    # Mock MongoDB collection
    mock_mongo = MagicMock()

    # Mock ML prediction
    def fake_prediction(description, merchant):
        if merchant == "Starbucks":
            return "Food"
        return "Travel"

    with patch(
        "app.main.get_mysql_connection",
        return_value=mock_connection
    ), patch(
        "app.main.notes_collection",
        mock_mongo
    ), patch(
        "app.main.predict_category",
        side_effect=fake_prediction
    ):

        response = client.post(
            "/upload_csv",
            data={
                "file": (
                    io.BytesIO(csv_content.encode("utf-8")),
                    "test_expenses.csv"
                )
            },
            content_type="multipart/form-data"
        )

    # Check HTTP response
    assert response.status_code == 200

    # Check response JSON
    data = response.get_json()

    assert data["message"] == "✅ CSV processed and data stored successfully."
    assert data["records_inserted"] == 2

    # MySQL checks
    assert mock_connection.commit.called
    assert mock_cursor.execute.call_count == 2

    # MongoDB checks
    assert mock_mongo.insert_one.call_count == 2

    # Rollback should NOT happen
    assert not mock_connection.rollback.called