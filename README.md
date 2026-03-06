# 🇮🇪 Irish Census Data Warehouse

A star schema data warehouse built on Ireland's Central Statistics Office (CSO) Census data, tracking population across all 26 counties from 1841 to 2022. Built with Python, dbt, PostgreSQL, and Metabase — fully containerised with Docker.

![Dashboard](docs/dashboard.png)

---

## 🏗️ Architecture

```
CSO PxStat API (free, no key required)
        │
        ▼
🐍 Python Ingestion (requests + pandas + SQLAlchemy)
        │
        ▼
🗄️ PostgreSQL — Bronze Layer (raw API data)
        │
        ▼
⚙️ dbt — Silver Layer (dimension tables)
        │
        ▼
🏆 dbt — Gold Layer (fact table with star schema)
        │
        ▼
📊 Metabase Dashboards
```

---

## ⭐ Star Schema Design

```
                ┌─────────────────┐
                │  fact_population│
                │─────────────────│
                │ county_code (FK)│
                │ census_year (FK)│
                │ population      │
                │ population_change│
                │ pct_change      │
                └────────┬────────┘
                         │
        ┌────────────────┴────────────────┐
        ▼                                 ▼
┌───────────────┐               ┌───────────────┐
│  dim_county   │               │   dim_year    │
│───────────────│               │───────────────│
│ county_code   │               │ census_year   │
│ county_name   │               │ century       │
│ province      │               │ is_modern_era │
│ province_order│               │ is_21st_century│
└───────────────┘               └───────────────┘
```

---

## 📊 Dashboard

Three charts built on 676 census records spanning 181 years:

- **Population by Province 1841–2022** — shows the Great Famine impact (1841–1871 decline) and Leinster's dramatic modern growth
- **County Population 2022** — Dublin at 1.4M dwarfs all other counties; Cork second at 600k
- **Population Growth by County since 1990** — Meath and Kildare lead at 80%+ growth, driven by Dublin commuter belt expansion

---

## 🔑 Key Insights

- All provinces lost population between 1841 and 1901 due to the Great Famine and emigration
- Leinster overtook all other provinces from the 1960s onwards driven by Dublin urbanisation
- Meath (+81%) and Kildare (+80%) are the fastest growing counties since 1990
- Dublin county alone accounts for ~29% of the entire Republic's population in 2022
- Mayo has the slowest growth rate since 1990 at ~19%

---

## 🛠️ Tech Stack

| Tool | Purpose |
|------|---------|
| Python (requests, pandas, SQLAlchemy) | API ingestion |
| PostgreSQL 15 | Data warehouse (Dockerised) |
| dbt Core 1.7.4 | Star schema transformations |
| Metabase | BI dashboards (Dockerised) |
| Docker Compose | Local orchestration |
| Git / GitHub | Version control |

---

## 📁 Project Structure

```
cso-census-warehouse/
├── data/                         ← raw API responses (git-ignored)
├── ingestion/
│   ├── ingest_cso.py             ← Python ingestion script
│   └── explore_cso.py            ← data exploration script
├── dbt_project/
│   ├── models/
│   │   ├── dimensions/
│   │   │   ├── sources.yml
│   │   │   ├── dim_county.sql    ← Silver: 26 Irish counties + province
│   │   │   └── dim_year.sql      ← Silver: 26 census years + flags
│   │   └── facts/
│   │       └── fact_population.sql ← Gold: 676 rows with YoY change
│   └── dbt_project.yml
├── docs/
│   └── dashboard.png
├── docker-compose.yml
├── .env.example
└── README.md
```

---

## 📋 dbt Models

| Layer | Model | Rows | Description |
|-------|-------|------|-------------|
| 🥈 Silver | `dim_county` | 26 | County name, code, province, province order |
| 🥈 Silver | `dim_year` | 26 | Census year, century, modern era flags |
| 🥇 Gold | `fact_population` | 676 | Population per county/year with YoY change and % change |

---

## 🚀 How to Run Locally

### Prerequisites
- Python 3.11+
- Docker Desktop
- Git

### Steps

**1. Clone the repo**
```bash
git clone https://github.com/SRG-Cy/cso-census-warehouse.git
cd cso-census-warehouse
```

**2. Create and activate virtual environment**
```bash
python -m venv venv
venv\Scripts\activate.bat        # Windows
source venv/bin/activate         # Mac/Linux
```

**3. Install Python dependencies**
```bash
pip install requests pandas psycopg2-binary python-dotenv sqlalchemy
```

**4. Set up environment variables**
```bash
copy .env.example .env
```

**5. Start PostgreSQL and Metabase**
```bash
docker compose up -d
```

**6. Run the ingestion script**
```bash
python ingestion/ingest_cso.py
```

**7. Run dbt transformations**
```bash
cd dbt_project
dbt run
dbt test
```

**8. Open Metabase**

Go to [http://localhost:3000](http://localhost:3000) and connect to PostgreSQL.

---

## 🌐 Data Source

- **Dataset:** Census of Population
- **Publisher:** Central Statistics Office (CSO) Ireland
- **API:** [CSO PxStat API](https://ws.cso.ie/public/api.restful/PxStat.Data.Cube_API.ReadDataset/FY001/JSON-stat/2.0/en)
- **Licence:** Public Sector Information (PSI) Licence
- **Coverage:** All 26 counties, 26 census years from 1841 to 2022

---

## 👤 Author

Built as part of an Irish Data Engineering portfolio targeting €45k–€60k roles in Ireland.

- MSc Business Analytics — University of Galway (NUIG)
- Skills: Python · SQL · dbt · PostgreSQL · Docker · Star Schema · Data Warehousing

---

## 📄 Licence

MIT
