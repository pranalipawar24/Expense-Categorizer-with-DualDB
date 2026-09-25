from unittest.mock import patch

from app.main import app


def test_monthly_report_mysql_failure():
    client = app.test_client()

    # Simulate MySQL connection failure
    with patch(
        "app.main.get_mysql_connection",
        side_effect=Exception("MySQL connection failed")
    ):

        response = client.get("/monthly_report/1/2025")

    # API should return server error
    assert response.status_code == 500

    # Flask returns an HTML error page for this unhandled exception
    assert response.data is not None
    assert len(response.data) > 0