"""
Transforms and Loads data into Azure Databricks
"""
import os
from databricks import sql
import pandas as pd
from dotenv import load_dotenv

def load(dataset="data/performer-scores.csv", dataset2="data/show-data.csv"):
    """Transforms and Loads data into the local databricks database"""
    df = pd.read_csv(dataset, delimiter=",")
    df2 = pd.read_csv(dataset2, delimiter=",")
    
    load_dotenv()
    server_h = os.getenv("SERVER_HOSTNAME")
    access_token = os.getenv("ACCESS_TOKEN")
    http_path = os.getenv("HTTP_PATH")
    
    with sql.connect(
        server_hostname=server_h,
        http_path=http_path,
        access_token=access_token,
    ) as connection:
        c = connection.cursor()
        
        # Create DemCandidatesDB table if not exists
        c.execute(
            """
            CREATE TABLE IF NOT EXISTS performerscoresDB (
                Performer string,
                Score_per_year float,
                Total_score float,
                Show string
            )
            """
        )
        
        # Insert data into DemCandidatesDB
        for _, row in df.iterrows():
            values = tuple(row)
            c.execute(f"INSERT INTO performerscoresDB VALUES {values}")
        
        # Create RepIncumbentsDB table if not exists
        c.execute(
            """
            CREATE TABLE IF NOT EXISTS showdataDB (
                Performer string,
                Show string,
                Show_Start string,
                Show_End string,
                CharEnd string
            )
            """
        )
        
        # Insert data into RepIncumbentsDB
        for _, row in df2.iterrows():
            values = tuple(row)
            c.execute(f"INSERT INTO showdataDB VALUES {values}")
        
        c.close()

    return "success"
