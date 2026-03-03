import requests
import json
import os
import pandas as pd
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

load_dotenv()

BASE_URL = "https://ws.cso.ie/public/api.restful/PxStat.Data.Cube_API.ReadDataset"

PROVINCES = {
    "Carlow": "Leinster", "Dublin": "Leinster", "Kildare": "Leinster",
    "Kilkenny": "Leinster", "Laois": "Leinster", "Longford": "Leinster",
    "Louth": "Leinster", "Meath": "Leinster", "Offaly": "Leinster",
    "Westmeath": "Leinster", "Wexford": "Leinster", "Wicklow": "Leinster",
    "Clare": "Munster", "Cork": "Munster", "Kerry": "Munster",
    "Limerick": "Munster", "Tipperary": "Munster", "Waterford": "Munster",
    "Galway": "Connacht", "Leitrim": "Connacht", "Mayo": "Connacht",
    "Roscommon": "Connacht", "Sligo": "Connacht",
    "Cavan": "Ulster", "Donegal": "Ulster", "Monaghan": "Ulster"
}

def get_engine():
    conn_str = (
        f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}"
        f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
    )
    return create_engine(conn_str)

def fetch_dataset(code):
    url = f"{BASE_URL}/{code}/JSON-stat/2.0/en"
    logger.info(f"Fetching {code} from CSO API...")
    response = requests.get(url, timeout=30)
    response.raise_for_status()
    return response.json()

def parse_population(data):
    dims = data["id"]
    sizes = data["size"]
    values = data["value"]

    year_labels = data["dimension"]["TLIST(A1)"]["category"]["label"]
    county_labels = data["dimension"]["C02779V03348"]["category"]["label"]
    gender_labels = data["dimension"]["C02199V02655"]["category"]["label"]

    years = list(year_labels.values())
    counties = list(county_labels.items())
    genders = list(gender_labels.items())

    records = []
    idx = 0
    for year in years:
        for county_code, county_name in counties:
            for gender_code, gender_name in genders:
                value = values[idx] if idx < len(values) else None
                if county_name != "State" and gender_name == "Both sexes" and value:
                    records.append({
                        "census_year": int(year),
                        "county_code": county_code,
                        "county_name": county_name,
                        "province": PROVINCES.get(county_name, "Unknown"),
                        "population": int(value)
                    })
                idx += 1

    return pd.DataFrame(records)

def create_schemas(engine):
    with engine.connect() as conn:
        conn.execute(text("CREATE SCHEMA IF NOT EXISTS cso_bronze"))
        conn.execute(text("CREATE SCHEMA IF NOT EXISTS cso_silver"))
        conn.execute(text("CREATE SCHEMA IF NOT EXISTS cso_gold"))
        conn.commit()
    logger.info("Schemas created")

def load_to_bronze(df, engine):
    df.to_sql(
        "bronze_population",
        engine,
        schema="cso_bronze",
        if_exists="replace",
        index=False,
        chunksize=1000
    )
    logger.info(f"✅ Loaded {len(df):,} rows to cso_bronze.bronze_population")

if __name__ == "__main__":
    engine = get_engine()
    create_schemas(engine)
    data = fetch_dataset("FY001")
    df = parse_population(data)
    logger.info(f"Parsed {len(df):,} records")
    logger.info(f"Years: {sorted(df['census_year'].unique())}")
    logger.info(f"Counties: {sorted(df['county_name'].unique())}")
    load_to_bronze(df, engine)
    logger.info("🏁 Ingestion complete!")