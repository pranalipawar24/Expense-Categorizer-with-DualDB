from unittest.mock import MagicMock, patch

from app.main import app


def test_monthly_report_success():
    client = app.test_client()

    # Mock MySQL connection
    mock_connection = MagicMock()
    mock_cursor = MagicMock()

    mock_connection.cursor.return_value = mock_cursor

    # Mock database result
    mock_cursor.fetchall.return_value = [
        ("Bills", 2698.0),
        ("Food", 1550.0),
        ("Travel", 1450.0),
    ]

    with patch(
        "app.main.get_mysql_connection",
        return_value=mock_connection
    ):

        response = client.get("/monthly_report/1/2025")

    # Check HTTP response
    assert response.status_code == 200

    data = response.get_json()

    # Check number of categories
    assert len(data) == 3

    # Check returned data structure
    assert data[0][0] == "Bills"
    assert data[0][1] == 2698.0

    assert data[1][0] == "Food"
    assert data[1][1] == 1550.0

    assert data[2][0] == "Travel"
    assert data[2][1] == 1450.0

    # Verify database query was executed
    assert mock_cursor.execute.called