# 🏦 Moroccan Bank Reviews - Data Warehouse & NLP Pipeline

**Project Title:**
*"Analyzing Customer Reviews of Bank Agencies in Morocco using a Modern Data Stack"*

---

## 🎯 Objective

This project automates the **collection, processing, and analysis** of Google Maps reviews for Moroccan banks.

It aims to extract **actionable insights** from a complex **multilingual dataset** (Arabic, French, English, and Darija) using advanced NLP techniques such as:

* Sentiment Analysis
* Topic Modeling (LDA)
* Language Detection

---

## 🏗️ Architecture & Pipeline Workflow

The project follows a **modern ELT (Extract, Load, Transform)** architecture orchestrated by **Apache Airflow**.

### 🔄 Pipeline Steps

#### 1️⃣ Extraction (API Layer)

* Data is collected from **Google Maps reviews** using the **Apify API**
* Ensures **high reliability and scalability**
* Output format: JSON

#### 2️⃣ Loading (Raw Layer - PostgreSQL)

* Raw data is ingested into a **PostgreSQL database**
* Stored in a **Raw Layer** without transformation
* Preserves data integrity for reproducibility

#### 3️⃣ Transformation (dbt Layer)

* Data is cleaned and structured using **dbt**
* Creation of:

  * Staging tables
  * Cleaned analytical datasets
* Ensures **modularity and maintainability**

#### 4️⃣ NLP Enrichment (Python / AI Layer)

* **Language Detection**

  * French
  * Arabic
  * Latin-alphabet Darija

* **Topic Modeling (LDA)**

  * Extracts key themes from reviews
  * Trained on **French reviews (71% of dataset)**

* **Sentiment Analysis**

  * Detects polarity (Positive / Negative / Neutral)

---

## 🛠️ Tech Stack

| Layer           | Tools                         |
| --------------- | ----------------------------- |
| Orchestration   | Apache Airflow                |
| Data Storage    | PostgreSQL                    |
| Transformation  | dbt                           |
| NLP             | Python (Pandas, NLTK, Gensim) |
| Data Collection | Apify API                     |
| Visualization   | Looker Studio                 |

---

## 🚀 Installation & Setup

### 1️⃣ Prerequisites

* WSL2 (Ubuntu)
* Python 3.9+
* PostgreSQL
* Apify API Token

---

### 2️⃣ Clone Repository

```bash
git clone https://github.com/votre-username/bank_reviews_dw.git
cd bank_reviews_dw
```

---

### 3️⃣ Virtual Environment

```bash
python3 -m venv venv_linux
source venv_linux/bin/activate
pip install -r requirements.txt
```

---

### 4️⃣ Environment Variables

Create `.env` file:

```env
DB_HOST=localhost
DB_NAME=bank_reviews_dw
DB_USER=your_user
DB_PASSWORD=your_password
APIFY_API_TOKEN=your_token
```

---

## ▶️ Run the Pipeline

### Create Airflow User

```bash
airflow users create \
  --username admin \
  --firstname Chaimae \
  --lastname Eng \
  --role Admin \
  --email admin@example.com \
  --password admin
```

---

### Start Airflow

Terminal 1:

```bash
airflow webserver -p 8080
```

Terminal 2:

```bash
airflow scheduler
```

---

### Launch

* Open: http://localhost:8080
* Trigger DAG: `bank_reviews_elt_pipeline`

---

## 📊 Key Insights

### 🌍 Multilingual Processing

Handles French, Arabic, and Darija (~82% accuracy)

### 🧠 Automated Insights

* Customer Support
* Staff Behavior
* Account Issues

### ⚡ Scalability

Portable and easy to deploy

---

## 📈 Future Improvements

* BERT for sentiment analysis
* Better Arabic NLP
* Kafka streaming
* Streamlit dashboard

---

## 📂 Project Structure

```bash
bank_reviews_dw/
├── dags/
├── dbt/
├── scripts/
├── data/
├── notebooks/
├── .env
├── requirements.txt
└── README.md
```

---

## 👩‍💻 Author

Chaimae
Data Science & Data Engineering Student

---

## ⭐ Acknowledgments

* Google Maps
* Apify
* Open-source NLP libraries
