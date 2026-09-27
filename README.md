# 🚕 End-to-End ELT Pipeline: NYC Taxi Data

## 📌 Présentation du Projet
Ce projet démontre la conception et l'orchestration d'un pipeline ELT (Extract, Load, Transform) complet, conteneurisé et reproductible. Il extrait les données publiques des trajets de taxis new-yorkais (NYC TLC), les charge de manière brute dans un Data Warehouse cloud, et exécute des transformations analytiques et des tests de qualité de données.

## 🏗️ Architecture technique et Flux de données
Le pipeline est entièrement orchestré par **Apache Airflow** (exécuté via Docker) et se divise en deux phases distinctes :
1. **Ingestion (Extract & Load) :** Un script Python récupère les fichiers Parquet sources et les charge dans le `TAXI_STAGE` interne de **Snowflake**, puis copie ces données brutes dans la table `RAW.TAXI_TRIPS`.
2. **Transformation & Testing (Transform) :** **dbt (Data Build Tool)** prend le relais pour nettoyer les données (modèles de staging) et générer les tables de faits (marts) prêtes pour l'analyse dans le schéma `ANALYTICS`, tout en validant l'intégrité des données (tests de non-nullité et d'unicité).

## 🛠️ Stack Technologique
* **Orchestration :** Apache Airflow 2.9.3
* **Data Warehouse :** Snowflake
* **Transformation :** dbt (dbt-snowflake)
* **Langages :** Python, SQL, YAML
* **Infrastructure :** Docker / Docker Compose (Développé sous environnement Debian 12)