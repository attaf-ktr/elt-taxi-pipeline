import os
from pathlib import Path
import snowflake.connector

# Définit le chemin absolu vers le dossier data/raw local
RAW_DIR = Path(__file__).parent.parent.parent / "data" / "raw"

def get_snowflake_conn():
    return snowflake.connector.connect(
        account="QWXXWYG-VN45087",
        user="KAOUTARA7",
        password="LrZyP2M;6,)zvTm", 
        warehouse="COMPUTE_WH",
        database="TAXI_DB",
        schema="RAW",
    )

def load_to_warehouse():
    print(f"Recherche des fichiers dans : {RAW_DIR}")
    conn = get_snowflake_conn()
    cur = conn.cursor()
    
    try:
        # 1. Upload des fichiers Parquet locaux vers le stage Snowflake
        print("Upload vers TAXI_STAGE en cours (cela peut prendre 1 à 2 minutes)...")
        cur.execute(f"PUT file://{RAW_DIR}/*.parquet @TAXI_DB.RAW.TAXI_STAGE AUTO_COMPRESS=FALSE OVERWRITE=TRUE;")
        print("Upload terminé.")

        # 2. Copie des données du stage vers la table finale
        print("Chargement dans TAXI_TRIPS (COPY INTO)...")
        copy_query = """
        COPY INTO TAXI_DB.RAW.TAXI_TRIPS
        FROM (
            SELECT 
                $1:VendorID::INT,
                $1:tpep_pickup_datetime::TIMESTAMP_NTZ,
                $1:tpep_dropoff_datetime::TIMESTAMP_NTZ,
                $1:passenger_count::NUMBER,
                $1:trip_distance::FLOAT,
                $1:RatecodeID::NUMBER,
                $1:store_and_fwd_flag::VARCHAR,
                $1:PULocationID::INT,
                $1:DOLocationID::INT,
                $1:payment_type::INT,
                $1:fare_amount::FLOAT,
                $1:extra::FLOAT,
                $1:mta_tax::FLOAT,
                $1:tip_amount::FLOAT,
                $1:tolls_amount::FLOAT,
                $1:improvement_surcharge::FLOAT,
                $1:total_amount::FLOAT,
                $1:congestion_surcharge::FLOAT,
                $1:Airport_fee::FLOAT
            FROM @TAXI_DB.RAW.TAXI_STAGE
        )
        FILE_FORMAT = (FORMAT_NAME = 'TAXI_DB.RAW.PARQUET_FORMAT')
        ON_ERROR = 'CONTINUE';
        """
        cur.execute(copy_query)
        print("Chargement terminé avec succès !")
        
    except Exception as e:
        print(f"Erreur rencontrée : {e}")
    finally:
        cur.close()
        conn.close()

if __name__ == "__main__":
    load_to_warehouse()