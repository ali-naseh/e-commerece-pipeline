# e-commerce

Repository for our e-commerce project

# Project Structure

```text
.
├── airflow/
├── clickhouse/
├── docker/
│   └── README.md
├── docs/
├── kafka/
├── mongodb/
├── postgres/
├── scripts/
├── Makefile
├── docker-compose.yaml
├── README.md
└── LICENSE

```

## Directory Overview

| Directory/File | Purpose |
|---|---|
| `airflow/` | Airflow DAGs and orchestration logic |
| `clickhouse/` | ClickHouse schemas and analytics queries |
| `docker/` | Docker-related configuration files |
| `docs/` | Project documentation |
| `kafka/` | Kafka topics, schemas, and streaming components |
| `mongodb/` | MongoDB collections and initialization scripts |
| `postgres/` | PostgreSQL schemas and SQL scripts |
| `scripts/` | Helper scripts and ETL utilities |
| `docker-compose.yaml` | Main infrastructure orchestration file |
| `Makefile` | Common development and deployment commands |
| `README.md` | Main project documentation |
| `LICENSE` | Project license |

> Docker Compose manages the full local data platform.

## Pipeline Overview

This project implements a local end-to-end data pipeline for an e-commerce platform. It generates source data, ingests it through different storage and streaming layers, and prepares analytics-ready data in ClickHouse.

The pipeline uses:

- **Airflow** for orchestration
- **PostgreSQL** for relational transactional data
- **MongoDB** for behavioral event data
- **Kafka** for streaming events and extracted records
- **ClickHouse** for analytical storage and reporting

At a high level, the project processes:

- users data
- orders data
- products data
- behavioral event data

These datasets are generated locally, processed by Airflow DAGs, and finally ingested into ClickHouse for analysis.

---

## How to Run the Pipeline

Before running the Airflow DAGs, you must first generate the source data.

### 1. Generate Source Data

Run the data generator script:
```bash
python scripts/generator-data.py

This script creates a folder beside the project folder named `data/`.

The generated `data/` directory will have the following structure:

text
data/
├── behavioral/
│   └── {json files for events}
├── users.csv
├── orders.csv
└── products.csv

### Generated Files

| File/Folder | Description |
|---|---|
| `data/users.csv` | Contains generated user records |
| `data/orders.csv` | Contains generated order records |
| `data/products.csv` | Contains generated product records |
| `data/behavioral/` | Contains JSON files for behavioral events |

The CSV files are used as the source for relational ingestion, while the JSON files represent user behavioral events.

---

### 2. Start the Project Services

After generating the data, start the local infrastructure using Docker Compose.

bash
docker compose up -d

Docker Compose starts the required services for the pipeline, including Airflow, PostgreSQL, MongoDB, Kafka, and ClickHouse.

---

### 3. Run the Airflow DAGs

After the services are running, open the Airflow UI and trigger the required DAGs.

The DAGs will process the generated files and load the data into the appropriate systems.

The pipeline performs tasks such as:

- reading generated CSV files
- loading transitional data into PostgreSQL
- processing behavioral JSON events
- producing data to Kafka
- consuming and transforming data
- loading analytical data into ClickHouse

---

### 4. Wait for Data Processing

After triggering the DAGs, wait until all required tasks are completed successfully.

The generated files will be processed and ingested through the pipeline.

Once the DAG runs finish successfully, the transformed data should be available in ClickHouse.

---

### 5. Analyze Data in ClickHouse

After ingestion is complete, ClickHouse can be used for analytical queries and reporting.

The project supports analytics such as:

- overall sales performance
- product catalog analytics
- category performance
- top products by popularity
- low-inventory popular products
- behavioral event analysis

---

## Expected Run Order

The recommended execution order is:

text
1. Generate source data
2. Start Docker Compose services
3. Trigger Airflow DAGs
4. Wait for the files and events to be processed
5. Query analytical tables in ClickHouse

Or in short:

bash
python scripts/generator-data.py
docker compose up -d

Then run the DAGs from the Airflow UI and analyze the final data in ClickHouse.

---

## Data Flow Summary

text
Generated Data
|
|-- users.csv
|-- orders.csv
|-- products.csv
|-- behavioral JSON files
|
v
Airflow DAGs
|
|-- PostgreSQL
|-- MongoDB
|-- Kafka
|
v
ClickHouse
|
v
Analytics and Reports

The final analytical layer in ClickHouse is used to run business queries and build reports for the e-commerce platform.
