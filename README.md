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

📸 Preuves d'exécution
1. Orchestration Airflow des Tâches

L'exécution séquentielle du téléchargement, du chargement Snowflake, de la transformation dbt et des tests de qualité.
2. Validation de la Qualité des Données (dbt Tests)

Validation réussie des règles métier (ex: total_amount et vendor_id non nuls).
3. Modélisation Finale dans Snowflake

Génération automatisée des tables analytiques (FCT_DAILY_REVENUE, STG_TAXI_TRIPS) prêtes à être connectées à un outil de BI.
⚙️ Configuration et Exécution locale
Prérequis

    Docker et Docker Compose installés.

    Un compte Snowflake actif avec une base TAXI_DB.

Installation

    Cloner le dépôt :
    Bash

git clone [https://github.com/attaf-ktr/elt-taxi-pipeline.git](https://github.com/attaf-ktr/elt-taxi-pipeline.git)
cd elt-taxi-pipeline

Créer un fichier .env à la racine pour sécuriser les identifiants Snowflake (ce fichier est ignoré par Git) :
Extrait de code

SNOWFLAKE_PASSWORD="votre_mot_de_passe_secret"

Lancer l'infrastructure Airflow :
Bash

    docker compose up -d

    Accéder à l'interface Airflow via http://localhost:8080 (identifiants par défaut : airflow/airflow), activer le DAG taxi_elt_pipeline et déclencher l'exécution manuelle.

🚀 Améliorations prévues pour un environnement de Production

Ce projet a été architecturé pour démontrer la logique ELT et la résolution de problèmes d'infrastructure en environnement local. Dans un contexte de production d'entreprise, les optimisations suivantes seraient appliquées :

    Images Docker Customisées : Création d'un Dockerfile dédié pour pré-installer les dépendances métier (dbt, connecteurs Python) au lieu de les résoudre à l'exécution.

    Isolation des ressources de calcul : Remplacement du BashOperator par le KubernetesPodOperator ou DockerOperator afin d'isoler l'exécution dbt et garantir la stabilité du serveur maître Airflow.

    Gestion des Secrets : Remplacement du fichier .env local par un gestionnaire de secrets type HashiCorp Vault ou AWS Secrets Manager.