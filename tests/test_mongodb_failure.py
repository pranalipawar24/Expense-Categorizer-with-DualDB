from unittest.mock import MagicMock, patch
import io

from app.main import app


def test_mongodb_failure():
    client = app.test_client()

    csv_content = """description,merchant,amount,date,payment_method,notes
Coffee and snacks,Starbucks,250,2025-01-08,UPI,Evening snacks
"""

    # Mock MySQL
    mock_connection = MagicMock()
    mock_cursor = MagicMock()
    mock_connection.cursor.return_value = mock_cursor
    mock_cursor.lastrowid = 101

    # Mock MongoDB failure
    mock_mongo = MagicMock()
    mock_mongo.insert_one.side_effect = Exception(
        "MongoDB insertion failed"
    )

    with patch(
        "app.main.get_mysql_connection",
        return_value=mock_connection
    ), patch(
        "app.main.notes_collection",
        mock_mongo
    ), patch(
        "app.main.predict_category",
        return_value="Food"
    ):

        response = client.post(
            "/upload_csv",
            data={
                "file": (
                    io.BytesIO(csv_content.encode("utf-8")),
                    "test_mongodb_failure.csv"
                )
            },
            content_type="multipart/form-data"
        )

    # API should return server error
    assert response.status_code == 500

    data = response.get_json()

    # Verify expected error message
    assert "MongoDB insertion failed" in data["error"]

    # MySQL transaction should have been committed
    assert mock_connection.commit.called

    # MongoDB insertion should have been attempted
    assert mock_mongo.insert_one.called