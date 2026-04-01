# 🏦 Moroccan Bank Reviews - Data Warehouse

Project Title: "Analyzing Customer Reviews of Bank Agencies in Morocco using a Modern Data Stack"

## 🎯 Objective
The goal of this project is to collect, process, and analyze Google Maps reviews for bank agencies in Morocco to extract valuable insights using topics analysis, sentiment detection, and other key insights. 
We are building a fully operational data pipeline using modern tools (Airflow, DBT, PostgreSQL, Looker Studio), ensuring efficient data extraction, transformation, storage, and visualization.

---

## 🏗️ Architecture & Evolution of Data Extraction (Phase 1)

**1. Proof of Concept (PoC) - Web Scraping :** Initial data exploration and dynamic extraction were developed "from scratch" using **Python and Playwright**. This exploratory phase successfully validated the structure of Google Maps data (DOM parsing, handling infinite scrolling, and text cleaning). The code and raw sample data from this exploratory phase are archived in the `v1_playwright_exploration/` folder for reference.

**2. Production Pipeline - API Integration (Current) :** To meet industry production standards and the requirements of the Modern Data Stack, the architecture evolved towards a third-party API solution. This strategic pivot guarantees:
* **Reliability:** Immunity to frequent Google Maps UI/DOM changes.
* **Scalability:** Ability to extract large volumes of data (hundreds of reviews per agency, strictly necessary for robust NLP and Sentiment Analysis) without hitting the official Google Places API 5-review limit.
* **Orchestration:** Lightweight, memory-efficient integration within **Apache Airflow**, avoiding the overhead of running headless browsers in the pipeline.

---

## 🛠️ Tech Stack
* **Data Collection:** Python, Web Scraping (Playwright PoC), API Integration
* **Scheduling:** Apache Airflow
* **Data Storage:** PostgreSQL (Data Warehouse)
* **Transformation:** DBT (Data Build Tool)
* **Analysis & BI:** Looker Studio ...