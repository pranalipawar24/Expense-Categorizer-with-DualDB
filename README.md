# 💰 Expense Categorizer with Dual Database

An intelligent **Expense Categorization and Management System** that automatically categorizes expenses using **Machine Learning** and stores data using both **MySQL and MongoDB**.

The project also includes **automated testing, Docker containerization, GitHub Actions CI/CD, and Docker Hub deployment**.

---

## 🚀 Project Overview

Managing and categorizing expenses manually can be time-consuming.

This project provides an automated solution where users can upload expense data through a CSV file. The system uses a **Machine Learning model based on TF-IDF and Multinomial Naive Bayes** to predict expense categories.

The application stores:

- Structured transaction data in **MySQL**
- Additional notes in **MongoDB**

It also provides a monthly expense report and includes automated testing and CI/CD integration.

---

## ✨ Features

- 📂 Upload expenses using CSV files
- 🤖 Automatic expense categorization using Machine Learning
- 🗄️ Store transaction data in MySQL
- 🍃 Store expense notes in MongoDB
- 📊 Generate monthly expense reports
- 🧪 Automated testing using Pytest
- 📈 Test coverage reporting
- 🐳 Docker containerization
- 🔄 Docker Compose for multi-container setup
- ⚙️ GitHub Actions CI/CD pipeline
- 🔐 Secure GitHub Secrets for Docker Hub authentication
- 📦 Automatic Docker image push to Docker Hub

---

## 🛠️ Tech Stack

### Backend
- Python
- Flask

### Machine Learning
- Scikit-learn
- TF-IDF Vectorization
- Multinomial Naive Bayes
- Pandas
- NumPy

### Databases
- MySQL
- MongoDB

### Testing
- Pytest
- Pytest-Cov

### DevOps
- Docker
- Docker Compose
- GitHub Actions
- Docker Hub

---

## 🏗️ System Architecture

                    ┌─────────────────────┐
                    │     CSV Upload      │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │     Flask API       │
                    └──────────┬──────────┘
                               │
                    ┌──────────▼──────────┐
                    │   ML Categorizer    │
                    │                     │
                    │ TF-IDF + Naive Bayes│
                    └──────────┬──────────┘
                               │
                 ┌─────────────┴─────────────┐
                 │                           │
                 ▼                           ▼
        ┌─────────────────┐        ┌─────────────────┐
        │      MySQL      │        │     MongoDB     │
        │                 │        │                 │
        │ Transactions    │        │ Expense Notes   │
        └─────────────────┘        └─────────────────┘
                 │
                 ▼
        ┌─────────────────┐
        │ Monthly Report  │
        └─────────────────┘
# 🤖 Machine Learning

The project uses a text classification model to categorize expenses.

### Input

The model uses:

~~~text
Description + Merchant
~~~

Example:

~~~text
"Friday dinner Domino's"
~~~

### Processing

The text is converted into numerical features using:

~~~text
TF-IDF Vectorization
~~~

The classification model used is:

~~~text
Multinomial Naive Bayes
~~~

### Output

The model predicts categories such as:

~~~text
Food
Travel
Bills
~~~

The trained model is stored as:

~~~text
app/models/category_model.pkl
~~~

---

# 📂 Project Structure

~~~text
Expense-Categorizer-with-DualDB/
│
├── app/
│   ├── main.py
│   │
│   ├── db/
│   │   └── mysql_conn.py
│   │
│   ├── models/
│   │   └── category_model.pkl
│   │
│   └── utils/
│       ├── categorizer.py
│       └── ml_model_trainer.py
│
├── evaluation/
│   └── evaluate_model.py
│
├── tests/
│   ├── test_categorizer.py
│   ├── test_validation.py
│   ├── test_upload_api.py
│   ├── test_database_failure.py
│   ├── test_mongodb_failure.py
│   ├── test_monthly_report.py
│   └── test_monthly_report_failure.py
│
├── TestingDocumentation/
│   ├── TEST PLAN.docx
│   ├── TestCases.xlsx
│   └── TEST REPORT.docx
│
├── ScreenShots/
│
├── training_data.csv
├── sample_expenses.csv
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── .dockerignore
├── .gitignore
└── README.md
~~~

---

# 🗄️ Database Design

The application uses a **dual database architecture**.

## MySQL

MySQL stores structured transaction information.

Database:

~~~text
expense_db
~~~

Table:

~~~text
transactions
~~~

Example fields include:

~~~text
id
merchant
category
amount
date
payment_method
description
~~~

---

## MongoDB

MongoDB stores expense-related notes.

Database:

~~~text
expenses
~~~

Collection:

~~~text
notes
~~~

MongoDB is used because its document-based structure provides flexibility for storing notes and additional information.

---

# 🔌 API Endpoints

## Upload CSV

~~~text
POST /upload_csv
~~~

Uploads the expense CSV file and processes the transactions.

---

## Monthly Report

~~~text
GET /monthly_report/<month>/<year>
~~~

Example:

~~~text
GET /monthly_report/1/2025
~~~

Returns the monthly expense summary by category.

Example:

~~~text
{
    "Food": 1550,
    "Travel": 1450,
    "Bills": 2698,
    "Total": 5698
}
~~~

---

# 🧪 Testing

Testing is an important part of this project.

The project uses **Pytest** for automated testing.

Tests cover:

-  Machine Learning prediction 
-  Input validation 
-  CSV upload 
-  MySQL database failures 
-  MongoDB database failures 
-  Monthly reports 
-  Monthly report failure scenarios 
-  API functionality 

Run all tests using:

~~~bash
python -m pytest -q
~~~

The project currently contains:

~~~text
18 automated tests
~~~

All tests pass successfully.

### Test Coverage

Current overall test coverage:

~~~text
92%
~~~

---

# 📊 ML Model Evaluation

The ML model was evaluated using test datasets.

### Hard Test Dataset

~~~text
Samples: 15
Accuracy: 93%
Precision: 94%
Recall: 93%
F1 Score: 93%
~~~

### Unseen Test Dataset

~~~text
Samples: 30
Accuracy: 100%
~~~

These evaluations were performed separately from the application's automated test suite.

---

# 🐳 Docker

The application is containerized using Docker.

The Docker image packages:

-  Python 
-  Flask application 
-  Required Python dependencies 
-  Machine Learning model 
-  Application source code 

## Build Docker Image

~~~bash
docker build -t pranalipawar/expense-categorizer:latest .
~~~

## Run Docker Image

~~~bash
docker run -p 5000:5000 pranalipawar/expense-categorizer:latest
~~~

Application:

~~~text
http://localhost:5000
~~~

---

# 🐳 Docker Compose

The project uses Docker Compose to run multiple services together.

Services:

~~~text
┌──────────────────────────┐
│   Expense Categorizer    │
│        Flask App         │
│        Port 5000         │
└────────────┬─────────────┘
             │
      ┌──────┴──────┐
      │             │
      ▼             ▼
   MySQL          MongoDB
  Port 3307       Port 27017
~~~

Start the complete application:

~~~bash
docker compose up --build
~~~

Stop the containers:

~~~bash
docker compose down
~~~

---

# 🔄 CI/CD Pipeline

This project includes an automated **CI/CD pipeline using GitHub Actions**.

The workflow is triggered when code is pushed to the `main` branch or when a pull request is created.

### Pipeline

~~~text
Developer
    │
    │ git push
    ▼
GitHub Repository
    │
    ▼
GitHub Actions
    │
    ├── Install Dependencies
    │
    ├── Run Automated Tests
    │
    ├── Build Docker Image
    │
    ├── Login to Docker Hub
    │
    └── Push Docker Image
             │
             ▼
         Docker Hub
~~~

### CI

The CI stage:

-  Installs project dependencies 
-  Runs automated tests 
-  Builds the Docker image 

### CD

The CD stage:

-  Authenticates with Docker Hub 
-  Pushes the latest Docker image 

---

# 🔐 GitHub Secrets

Docker Hub authentication is handled securely using **GitHub Repository Secrets**.

The workflow uses:

~~~text
DOCKERHUB_USERNAME
DOCKERHUB_TOKEN
~~~

Secrets are referenced inside GitHub Actions using:

~~~text
${{ secrets.DOCKERHUB_USERNAME }}
~~~

and:

~~~text
${{ secrets.DOCKERHUB_TOKEN }}
~~~

No Docker Hub credentials are stored directly in the workflow file.

---

# 📦 Docker Hub

The Docker image is available on Docker Hub:

**Repository:**

~~~text
pranalipawar/expense-categorizer
~~~

The latest image is automatically pushed through the GitHub Actions CI/CD pipeline.

---

# ⚙️ Local Setup

## 1. Clone the Repository

~~~bash
git clone https://github.com/pranalipawar24/Expense-Categorizer-with-DualDB.git
~~~

Move into the project:

~~~bash
cd Expense-Categorizer-with-DualDB
~~~

---

## 2. Create Virtual Environment

~~~bash
python -m venv venv
~~~

Activate it on Windows:

~~~bash
venv\Scripts\activate
~~~

---

## 3. Install Dependencies

~~~bash
pip install -r requirements.txt
~~~

---

## 4. Configure Environment Variables

Create a `.env` file in the project root.

Example structure:

~~~text
MYSQL_HOST=localhost
MYSQL_USER=root
MYSQL_PASSWORD=your_password
MYSQL_DATABASE=expense_db

MONGO_URI=mongodb://localhost:27017/
MONGO_DB=expenses
~~~

---

## 5. Train the ML Model

If required, run:

~~~bash
python app/utils/ml_model_trainer.py
~~~

This generates:

~~~text
app/models/category_model.pkl
~~~

---

## 6. Run the Application

~~~bash
python app/main.py
~~~

The application will run on:

~~~text
http://127.0.0.1:5000
~~~

---

# 🧪 Run Tests

Run the complete test suite:

~~~bash
python -m pytest -q
~~~

Run tests with coverage:

~~~bash
python -m pytest --cov=. --cov-report=term-missing
~~~

---

# 📈 Project Results

The project successfully demonstrates:

-  Machine Learning-based expense categorization 
-  Dual database integration 
-  REST API development 
-  Automated software testing 
-  Test coverage analysis 
-  Docker containerization 
-  Docker Compose 
-  CI/CD automation 
-  Secure credential management 
-  Automated Docker image deployment 

---

# 🔮 Future Enhancements

Possible future improvements include:

-  📊 Expense visualization dashboard 
-  🔐 User authentication 
-  📱 Responsive frontend 
-  📈 Spending trend analysis 
-  💡 Personalized spending insights 
-  🧠 Improved ML model with more training data 
-  ☁️ Cloud deployment 
-  🔔 Budget and expense alerts 

---

# 👩‍💻 Author

**Pranali Pawar**

Computer Engineering Student

### GitHub

~~~text
https://github.com/pranalipawar24
~~~

---

# ⭐ Acknowledgements

This project was developed as a learning and portfolio project to demonstrate:

-  Backend development 
-  Machine Learning 
-  Database integration 
-  Software testing 
-  Docker 
-  CI/CD 
-  DevOps practices 

---
