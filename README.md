# 💸 Expense Auto-Categorizer with Dual DB (MySQL + MongoDB)

A Python-based real-time expense tracker that uses **machine learning** to auto-categorize transactions and stores data in both **MySQL** and **MongoDB** for hybrid flexibility.

---

## 📌 Features

- ✅ Upload expenses via CSV (manual uploads supported)
- 🤖 Automatically categorizes transactions using ML/NLP
- 🗃 Stores structured data (amount, date, method, merchant, category) in **MySQL**
- 📎 Stores unstructured data (notes, receipts, tags) in **MongoDB**
- 📊 Monthly category-wise spending reports
- 🔐 Environment variables for DB credentials
- 🧠 Easily extendable (add OCR, retraining, user accounts, etc.)

---

## ⚙️ Tech Stack

| Component              | Technology                      |
|------------------------|---------------------------------|
| Backend                | Python + Flask                  |
| Database (Relational)  | MySQL                           |
| Database (NoSQL)       | MongoDB                         |
| ML Model               | Naive Bayes + TF-IDF (Scikit-learn) |
| File Upload            | CSV (via API/Postman or UI)     |
| Environment Mgmt       | Python Dotenv                   |

---

## 📁 Project Structure

```
expense-auto-categorizer/
│
├── app/
│   ├── main.py               # Flask app (API)
│   ├── db/
│   │   ├── mysql_conn.py     # MySQL connector
│   │   └── mongo_conn.py     # MongoDB connector
│   ├── utils/
│   │   ├── parser.py         # CSV parser
│   │   ├── categorizer.py    # ML predictor
│   │   └── ml_model_trainer.py # Model training
│   ├── models/
│   └── category_model.pkl    # Saved ML model
│
├── uploads/                  # Uploaded CSV files
├── sample_expenses.csv       # Example CSV to test
├── .env                      # Environment variables
├── requirements.txt          # Dependencies
├── README.md                 # This file
```

---

## 🚀 Getting Started

### 🔧 1. Clone the Repo

```bash
git clone https://github.com/sujalgangarde/expense-auto-categorizer.git
cd expense-auto-categorizer
```

### 📦 2. Install Requirements

```bash
pip install -r requirements.txt
```

### 🔐 3. Setup .env File

Create a `.env` file in root:

```ini
MYSQL_HOST=localhost
MYSQL_USER=root
MYSQL_PASSWORD=password
MYSQL_DATABASE=expenses_db

MONGO_URI=mongodb://localhost:27017/
MONGO_DB=expenses
```

### 🛢 4. Create MySQL DB & Table

```sql
CREATE DATABASE expenses_db;

USE expenses_db;

CREATE TABLE transactions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    amount DECIMAL(10, 2),
    date DATE,
    payment_method VARCHAR(50),
    merchant VARCHAR(100),
    category VARCHAR(50)
);
```

### 💾 5. Train the ML Model

```bash
python app/utils/ml_model_trainer.py
```

### ▶️ 6. Run the Flask Server

```bash
python app/main.py
```

---

## 📤 API Endpoints

### 📍 POST `/upload_csv`

Upload CSV of transactions.

**Form-data:**

| Key  | Type | Value                |
|------|------|----------------------|
| file | File | sample_expenses.csv  |

**Response:**
```json
{ "message": "✅ CSV processed and data stored." }
```

---

### 📍 GET `/monthly_report/<month>/<year>`

Example:

```bash
GET http://localhost:5000/monthly_report/7/2025
```

**Response:**
```json
[
  {"category": "Food", "total": 870.0},
  {"category": "Travel", "total": 920.0}
]
```

---

## 🧪 Sample CSV Format

```csv
description,merchant,amount,date,method,notes,tags
Pizza dinner,Domino's,450.00,2025-07-01,Credit Card,Friday treat,"['food', 'takeout']"
Uber ride,Uber,120.00,2025-07-02,UPI,Morning commute,"['travel']"
```

---

## 📷 Screenshots

You can add Postman screenshots, DB screenshots, and charts here.

---

## 🧠 Future Improvements

- 📷 OCR for scanned receipts
- 🧠 Auto ML retraining with feedback
- 🌐 Frontend (React/Streamlit)
- 📈 Charts and Dashboards
- 🔒 JWT login and multiple users

---

## 🛡 License

This project is licensed under the MIT License.

---
