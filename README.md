# 🏦 Moroccan Bank Reviews - Data Warehouse

**Project Title:** *"Analyzing Customer Reviews of Bank Agencies in Morocco using a Modern Data Stack"*

## 🎯 Objective
The goal of this project is to collect, process, and analyze Google Maps reviews for bank agencies in Morocco to extract valuable insights using topics analysis, sentiment detection, and other key insights. We are building a fully operational data pipeline using modern tools (**Airflow, dbt, PostgreSQL, Looker Studio**), ensuring efficient data extraction, transformation, storage, and visualization.

---

## 🏗️ Architecture & Evolution

### Phase 1: Data Extraction
1. **Proof of Concept (PoC) - Web Scraping:** Initial data exploration using **Python and Playwright**. Archived in `v1_playwright_exploration/`.
2. **Production Pipeline - API Integration:** Strategic pivot to a third-party API for **Reliability** (immunity to UI changes), **Scalability** (bypassing the 5-review limit), and **Orchestration** (lightweight execution in Airflow).

### Phase 2: Enrichment & Transformation (NLP)
Le défi majeur de ce projet est le traitement du **multilinguisme marocain** (Arabe, Français, Anglais et Darija).
* **Custom Language Detection:** Module Python capable de détecter le **Darija Latin** (souvent confondu avec d'autres langues). 
  * **Précision : 82%** sur les tests locaux.
* **Sentiment Analysis (dbt):** Transformation des données brutes en insights via des modèles SQL.
  * Classification : **Positif / Négatif / Neutre**.

---

## 🛠️ Tech Stack
* **Orchestration:** Apache Airflow (Running on WSL/Ubuntu)
* **Data Storage:** PostgreSQL
* **Transformation:** dbt (data build tool)
* **Language:** Python 3.10+
* **Analysis & BI:** Looker Studio

---

## 🔄 Pipeline Workflow
`Extraction (API) -> Loading (Postgres) -> Language Enrichment (Python) -> Transformation (dbt)`