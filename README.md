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

```text
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
