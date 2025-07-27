# AWS Batch Pipeline - Serverless ETL

This project demonstrates a serverless ETL pipeline using AWS services such as S3, Lambda, Glue, Athena, and more.

## Architecture

### History-based ETL
![Architecture History](architecture_history.png)

### Incremental ETL
![Architecture Incremental](architecture_incremental.png)

## Components

- **S3**: Storage for raw and processed data.
- **Lambda**: Triggers to initiate Glue jobs or crawlers.
- **Glue**: ETL jobs and crawlers to process and catalog data.
- **Athena**: Querying processed data.
- **CloudWatch**: Logs and monitoring.

## How to Run

1. Upload raw data to S3.
2. Lambda triggers Glue crawler to update the catalog.
3. Lambda triggers Glue ETL job for transformation.
4. Transformed data is stored back in S3.
5. Athena queries can be executed on transformed data.

## Folder Structure

