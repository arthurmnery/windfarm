# Wind Farm – Data Lake on AWS

Streaming telemetry ingestion and processing pipeline for wind turbines,
built on managed AWS services.

## Context

Each turbine emits 3 telemetry signals every **10 seconds**:

| Signal | Simulated range | Relevance |
|---|---|---|
| `powerfactor` | 0.7 – 1.0 | Energy conversion efficiency |
| `batterytemperature` | 20 – 45 °C | Backup system health |
| `hydraulicpressure` | 70 – 80 bar | Pitch/brake system |

Each producer is a standalone Python script running in an infinite loop.

# How to run

You'll need:
- An AWS account
- [Google Colab](https://colab.research.google.com) account

## Step 1 — Create the S3 buckets

In the AWS Console, go to S3 → Create bucket:

- windfarm-raw	Receives the raw JSON data from Firehose
- windfarm-processed	Stores the Parquet files (your data lake, queried by Athena)

Keep all defaults. Make sure both of them are in the same region as your Kinesis stream.

## Step 2 — Create the streaming pipeline

### Kinesis Data Streams:

AWS Console → Kinesis Data Streams → Create stream

- Name: windfarm-stream

### Kinesis Data Firehose:

AWS Console → Kinesis Data Firehose → Create delivery stream

- Name: windfarm-firehose
- Source: select windfarm-stream
- Destination: select windfarm-raw


## Step 3 — Set up AWS credentials

You'll find your keys in AWS Console → your username (top right) → Security credentials.

## Step 4 — Run the producers

Open the 3 notebooks in Colab (one per producer) and run all cells:

- producers/powerfactor.ipynb
- producers/batterytemp.ipynb
- producers/hydraulic.ipynb

Each notebook loops and sends a reading to Kinesis every 10 seconds.
To stop, click the ■ button on the running cell.

To check if data is arriving: open windfarm-raw in the S3 Console and look for new JSON files.

## Step 6 — Catalog the data (Glue Crawler)

AWS Console → AWS Glue → Crawlers → Add crawler:

- Role: select your Glue IAM role
- Data source: S3 → windfarm-raw
- Database: windfarm_database
- Prefix: leave empty
- Create crawler → Crawl now

The crawler detects the schema and registers the tables in the Data Catalog.

## Step 7 — Run the ETL (JSON → Parquet)

AWS Console → AWS Glue → Jobs:

- Create a new ETL job (Spark 3.x)
- Source: the table from windfarm_database
- Target: S3 → windfarm-processed
- Format: Parquet | Compression: Snappy
- Start job

Parquet files will appear in windfarm-processed after a few minutes.

## Step 8 — Query in Athena

AWS Console → Athena → Query editor:

- Select database: windfarm_database
- Select the Parquet table from windfarm-processed
- Run your SQL queries to analyze turbine performance
