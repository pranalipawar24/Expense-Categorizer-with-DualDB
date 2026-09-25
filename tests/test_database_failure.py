from unittest.mock import MagicMock, patch
import io

from app.main import app


def test_mysql_failure_rolls_back():
    client = app.test_client()

    csv_content = """description,merchant,amount,date,payment_method,notes
Coffee and snacks,Starbucks,250,2025-01-08,UPI,Evening snacks
"""

    # Mock MySQL connection
    mock_connection = MagicMock()
    mock_cursor = MagicMock()

    mock_connection.cursor.return_value = mock_cursor

    # Simulate MySQL insertion failure
    mock_cursor.execute.side_effect = Exception("MySQL insertion failed")

    with patch(
        "app.main.get_mysql_connection",
        return_value=mock_connection
    ), patch(
        "app.main.predict_category",
        return_value="Food"
    ):

        response = client.post(
            "/upload_csv",
            data={
                "file": (
                    io.BytesIO(csv_content.encode("utf-8")),
                    "test_failure.csv"
                )
            },
            content_type="multipart/form-data"
        )

    # API should return server error
    assert response.status_code == 500

    # Transaction must be rolled back
    assert mock_connection.rollback.called

    # Commit must NOT happen
    assert not mock_connection.commit.called