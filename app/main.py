import sys
import os
import datetime
import math

from flask import Flask, request, jsonify

# Add root folder to path so we can import app modules directly
sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..")
    )
)

from app.db.mysql_conn import get_mysql_connection
from app.db.mongo_conn import notes_collection
from app.utils.parser import parse_csv
from app.utils.categorizer import predict_category


# Flask app setup
app = Flask(__name__)

UPLOAD_FOLDER = "uploads"

# Create uploads folder if it does not exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


# Required CSV columns
REQUIRED_COLUMNS = [
    "description",
    "merchant",
    "amount",
    "date",
    "payment_method",
    "notes"
]


# ---------------------------------------------------------
# HELPER FUNCTION
# ---------------------------------------------------------

def clean_value(value):
    """
    Convert None, NaN, and other values into
    clean strings for validation.
    """

    if value is None:
        return ""

    if isinstance(value, float) and math.isnan(value):
        return ""

    return str(value).strip()


# ---------------------------------------------------------
# UPLOAD CSV API
# ---------------------------------------------------------

@app.route("/upload_csv", methods=["POST"])
def upload_csv():

    # -----------------------------------------------------
    # 1. CHECK FILE
    # -----------------------------------------------------

    if "file" not in request.files:
        return jsonify({
            "error": "No file part in request"
        }), 400

    file = request.files["file"]

    # Handle no file selected
    if file.filename == "":
        return jsonify({
            "error": "No file selected"
        }), 400

    # -----------------------------------------------------
    # 2. SAVE UPLOADED FILE
    # -----------------------------------------------------

    path = os.path.join(
        UPLOAD_FOLDER,
        file.filename
    )

    file.save(path)

    # -----------------------------------------------------
    # 3. PARSE CSV
    # -----------------------------------------------------

    try:
        records = parse_csv(path)

    except Exception as e:

        error_message = str(e)

        # Handle completely empty CSV
        if "No columns to parse from file" in error_message:
            return jsonify({
                "error": "CSV file is empty"
            }), 400

        return jsonify({
            "error": f"Failed to parse CSV: {error_message}"
        }), 400

    # Check if CSV contains records
    if not records:
        return jsonify({
            "error": "CSV file is empty"
        }), 400

    # -----------------------------------------------------
    # 4. VALIDATE REQUIRED COLUMNS
    # -----------------------------------------------------

    missing_columns = [
        column
        for column in REQUIRED_COLUMNS
        if column not in records[0]
    ]

    if missing_columns:
        return jsonify({
            "error": "CSV is missing required columns",
            "missing_columns": missing_columns,
            "required_columns": REQUIRED_COLUMNS
        }), 400

    # -----------------------------------------------------
    # 5. VALIDATE ALL RECORDS
    # -----------------------------------------------------

    validated_records = []

    for row_number, record in enumerate(
        records,
        start=2
    ):

        # Raw values
        description_raw = record["description"]
        merchant_raw = record["merchant"]
        amount_raw = record["amount"]
        date_raw = record["date"]
        payment_method_raw = record["payment_method"]
        notes_raw = record["notes"]

        # Clean values
        description = clean_value(
            description_raw
        )

        merchant = clean_value(
            merchant_raw
        )

        amount_raw = clean_value(
            amount_raw
        )

        date_raw = clean_value(
            date_raw
        )

        payment_method = clean_value(
            payment_method_raw
        )

        notes = clean_value(
            notes_raw
        )

        # -------------------------------------------------
        # DESCRIPTION
        # -------------------------------------------------

        if not description:
            return jsonify({
                "error": (
                    f"Row {row_number}: "
                    "description cannot be empty"
                )
            }), 400

        # -------------------------------------------------
        # MERCHANT
        # -------------------------------------------------

        if not merchant:
            return jsonify({
                "error": (
                    f"Row {row_number}: "
                    "merchant cannot be empty"
                )
            }), 400

        # -------------------------------------------------
        # AMOUNT
        # -------------------------------------------------

        if not amount_raw:
            return jsonify({
                "error": (
                    f"Row {row_number}: "
                    "amount cannot be empty"
                )
            }), 400

        try:
            amount = float(amount_raw)

        except ValueError:
            return jsonify({
                "error": (
                    f"Row {row_number}: "
                    f"invalid amount '{amount_raw}'"
                )
            }), 400

        if not math.isfinite(amount):
            return jsonify({
                "error": (
                    f"Row {row_number}: "
                    "amount must be a valid number"
                )
            }), 400

        if amount <= 0:
            return jsonify({
                "error": (
                    f"Row {row_number}: "
                    "amount must be greater than 0"
                )
            }), 400

        # -------------------------------------------------
        # DATE
        # -------------------------------------------------

        if not date_raw:
            return jsonify({
                "error": (
                    f"Row {row_number}: "
                    "date cannot be empty"
                )
            }), 400

        try:

            date_obj = datetime.datetime.strptime(
                date_raw,
                "%Y-%m-%d"
            ).date()

            date = date_obj.strftime(
                "%Y-%m-%d"
            )

        except ValueError:

            return jsonify({
                "error": (
                    f"Row {row_number}: "
                    f"invalid date '{date_raw}'. "
                    "Expected format YYYY-MM-DD"
                )
            }), 400

        # -------------------------------------------------
        # PAYMENT METHOD
        # -------------------------------------------------

        if not payment_method:
            return jsonify({
                "error": (
                    f"Row {row_number}: "
                    "payment_method cannot be empty"
                )
            }), 400

        # -------------------------------------------------
        # ADD VALIDATED RECORD
        # -------------------------------------------------

        validated_records.append({
            "description": description,
            "merchant": merchant,
            "amount": amount,
            "date": date,
            "payment_method": payment_method,
            "notes": notes
        })

    # ---------------------------------------------------------
    # 6. CONNECT TO MYSQL
    # ---------------------------------------------------------

    conn = get_mysql_connection()

    if conn is None:
        return jsonify({
            "error": "Could not connect to MySQL database"
        }), 500

    cursor = conn.cursor()

    inserted_records = []

    try:

        # -------------------------------------------------
        # 7. INSERT VALIDATED RECORDS INTO MYSQL
        # -------------------------------------------------

        for record in validated_records:

            description = record["description"]
            merchant = record["merchant"]
            amount = record["amount"]
            date = record["date"]
            method = record["payment_method"]
            notes = record["notes"]

            # Predict category using ML model
            category = predict_category(
                description,
                merchant
            )

            # Insert into MySQL
            cursor.execute(
                """
                INSERT INTO transactions
                (
                    user_id,
                    amount,
                    date,
                    payment_method,
                    merchant,
                    category
                )
                VALUES (%s, %s, %s, %s, %s, %s)
                """,
                (
                    1,
                    amount,
                    date,
                    method,
                    merchant,
                    category
                )
            )

            txn_id = cursor.lastrowid

            inserted_records.append({
                "transaction_id": txn_id,
                "merchant": merchant,
                "category": category,
                "amount": amount,
                "date": date,
                "payment_method": method,
                "notes": notes
            })

        # Commit only after ALL records succeed
        conn.commit()

    except Exception as e:

        # Roll back MySQL if anything fails
        conn.rollback()

        return jsonify({
            "error": "Failed to store records",
            "details": str(e)
        }), 500

    finally:

        cursor.close()
        conn.close()

    # ---------------------------------------------------------
    # 8. INSERT INTO MONGODB
    # ---------------------------------------------------------

    try:

        for record in inserted_records:

            notes_collection.insert_one({
                "transaction_id": record["transaction_id"],
                "merchant": record["merchant"],
                "category": record["category"],
                "amount": record["amount"],
                "date": record["date"],
                "payment_method": record["payment_method"],
                "notes": record["notes"],
                "tags": [],
                "timestamp": datetime.datetime.now()
            })

    except Exception as e:

        return jsonify({
            "error": (
                "MySQL data stored, "
                "but MongoDB insertion failed"
            ),
            "details": str(e)
        }), 500

    # ---------------------------------------------------------
    # 9. SUCCESS RESPONSE
    # ---------------------------------------------------------

    return jsonify({
        "message": (
            "✅ CSV processed and "
            "data stored successfully."
        ),
        "records_inserted": len(
            inserted_records
        )
    }), 200


# ---------------------------------------------------------
# MONTHLY REPORT API
# ---------------------------------------------------------

@app.route(
    "/monthly_report/<int:month>/<int:year>",
    methods=["GET"]
)
def monthly_report(month, year):

    conn = get_mysql_connection()

    if conn is None:
        return jsonify({
            "error": "Could not connect to MySQL database"
        }), 500

    cursor = conn.cursor(
        dictionary=True
    )

    try:

        cursor.execute(
            """
            SELECT
                category,
                SUM(amount) AS total
            FROM transactions
            WHERE MONTH(date) = %s
            AND YEAR(date) = %s
            GROUP BY category
            """,
            (
                month,
                year
            )
        )

        data = cursor.fetchall()

    finally:

        cursor.close()
        conn.close()

    return jsonify(data)


# ---------------------------------------------------------
# RUN FLASK
# ---------------------------------------------------------

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)