import io

from app.main import app


def test_missing_file():
    client = app.test_client()

    response = client.post("/upload_csv")

    assert response.status_code == 400
    assert response.json["error"] == "No file part in request"


def test_empty_filename():
    client = app.test_client()

    response = client.post(
        "/upload_csv",
        data={
            "file": (
                io.BytesIO(b""),
                ""
            )
        },
        content_type="multipart/form-data"
    )

    assert response.status_code == 400
    assert response.json["error"] == "No file selected"


def test_empty_csv():
    client = app.test_client()

    response = client.post(
        "/upload_csv",
        data={
            "file": (
                io.BytesIO(b""),
                "empty.csv"
            )
        },
        content_type="multipart/form-data"
    )

    assert response.status_code == 400
    assert response.json["error"] == "CSV file is empty"


def test_missing_required_column():
    client = app.test_client()

    csv_data = (
        "description,merchant,amount,date\n"
        "Dinner,Restaurant,500,2025-01-01\n"
    )

    response = client.post(
        "/upload_csv",
        data={
            "file": (
                io.BytesIO(csv_data.encode()),
                "missing_column.csv"
            )
        },
        content_type="multipart/form-data"
    )

    assert response.status_code == 400
    assert response.json["error"] == "CSV is missing required columns"


def test_invalid_amount():
    client = app.test_client()

    csv_data = (
        "description,merchant,amount,date,payment_method,notes\n"
        "Dinner,Restaurant,abc,2025-01-01,UPI,Dinner\n"
    )

    response = client.post(
        "/upload_csv",
        data={
            "file": (
                io.BytesIO(csv_data.encode()),
                "invalid_amount.csv"
            )
        },
        content_type="multipart/form-data"
    )

    assert response.status_code == 400
    assert "invalid amount" in response.json["error"]


def test_negative_amount():
    client = app.test_client()

    csv_data = (
        "description,merchant,amount,date,payment_method,notes\n"
        "Dinner,Restaurant,-500,2025-01-01,UPI,Dinner\n"
    )

    response = client.post(
        "/upload_csv",
        data={
            "file": (
                io.BytesIO(csv_data.encode()),
                "negative_amount.csv"
            )
        },
        content_type="multipart/form-data"
    )

    assert response.status_code == 400
    assert "amount must be greater than 0" in response.json["error"]


def test_invalid_date():
    client = app.test_client()

    csv_data = (
        "description,merchant,amount,date,payment_method,notes\n"
        "Dinner,Restaurant,500,01-01-2025,UPI,Dinner\n"
    )

    response = client.post(
        "/upload_csv",
        data={
            "file": (
                io.BytesIO(csv_data.encode()),
                "invalid_date.csv"
            )
        },
        content_type="multipart/form-data"
    )

    assert response.status_code == 400
    assert "invalid date" in response.json["error"]


def test_empty_payment_method():
    client = app.test_client()

    csv_data = (
        "description,merchant,amount,date,payment_method,notes\n"
        "Dinner,Restaurant,500,2025-01-01,,Dinner\n"
    )

    response = client.post(
        "/upload_csv",
        data={
            "file": (
                io.BytesIO(csv_data.encode()),
                "empty_payment.csv"
            )
        },
        content_type="multipart/form-data"
    )

    assert response.status_code == 400
    assert "payment_method cannot be empty" in response.json["error"]