AWS Setup – YouTube Data Engineering Pipeline
1. Project Overview

-> This project implements an end-to-end data engineering pipeline on AWS using the YouTube Trending dataset from Kaggle
-> The objective is to ingest raw data, transform it into an analytics-friendly format, and enable SQL-based analysis using serverless AWS services
-> The pipeline uses Amazon S3 as a data lake, AWS Lambda for ETL, AWS Glue for metadata management, and Amazon Athena for querying

2. Data Source

-> Downloaded the YouTube Trending dataset from Kaggle
-> The dataset contains:
-> CSV files for video statistics by region
-> JSON files for category reference data
-> These files serve as the raw input to the data pipeline

3. AWS CLI and Access Setup

-> Created an IAM user and generated Access Key and Secret Key for programmatic access
-> Installed and configured AWS CLI locally using the IAM credentials
-> Verified CLI access by listing S3 buckets and testing basic AWS CLI commands

4. Amazon S3 Raw Data Lake Setup

-> Created an S3 bucket for raw data storage:
-> dataeng-on-youtube-raw-useast1-dev-2026
-> Uploaded Kaggle dataset to S3 using AWS CLI
-> Organized the data using a Hive-style folder structure for partitioning

Raw data structure in S3:

youtube/
-> raw_statistics_reference_data/ (contains JSON category reference files)
-> raw_statistics/
-> region=ca/
-> region=de/
-> region=fr/
-> region=gb/
-> region=in/
-> region=jp/
-> region=kr/
-> region=mx/
-> region=ru/
-> region=us/

-> Used the following AWS CLI commands to upload the data:

-> Copied JSON reference data to S3 using a recursive copy command
-> Copied CSV files into region-based folders to follow Hive-style partitioning

-> This folder structure enables partition-based processing and efficient querying later in Athena

5. Initial AWS Glue Crawler Attempt

-> Created an AWS Glue database for raw data
-> Configured an AWS Glue Crawler to scan the raw S3 bucket
-> The crawler failed due to JSON format issues (multi-line / nested JSON structure)
-> Identified the need to transform raw data into a structured, columnar format before cataloging

6. AWS Lambda ETL Setup

-> Created an AWS Lambda function using Python runtime
-> Created and attached an IAM execution role with permissions to:
-> Read data from the raw S3 bucket
-> Write data to the cleansed S3 bucket
-> Interact with AWS Glue
-> Added a Lambda Layer to include required libraries:
-> pandas
-> awswrangler
-> pyarrow
-> Configured Lambda memory and timeout to support data processing

The Lambda ETL process performs the following steps:

-> Reads raw JSON and CSV data from the raw S3 bucket
-> Normalizes and flattens nested JSON structures
-> Cleans and standardizes the dataset
-> Converts the data into Parquet format
-> Writes the processed data to the cleansed S3 bucket

7. Amazon S3 Cleansed Data Lake Setup

-> Created a second S3 bucket for processed data storage:
-> dataeng-on-youtube-cleansed-useast1-dev-2026
-> Configured the Lambda function to write Parquet files into this bucket
-> Verified that the transformed Parquet files are successfully generated after Lambda execution

8. AWS Glue Catalog for Cleansed Data

-> Created a Glue database for cleaned data:
-> db_youtube_cleaned
-> Configured a Glue Crawler to scan the cleansed S3 bucket
-> Ran the crawler to automatically discover schema from Parquet files
-> Verified that tables are created successfully in the Glue Data Catalog

9. Amazon Athena Query Setup

-> Configured Athena query result location in Amazon S3
-> Connected Athena to the Glue Data Catalog
-> Queried the cleaned Parquet tables from the database db_youtube_cleaned
-> Performed analytical queries such as:
-> Video count by region
-> Analysis of views, likes, and categories
-> Observed improved query performance due to Parquet format and partitioned data layout

10. End-to-End Pipeline Flow

-> Downloaded dataset from Kaggle
-> Uploaded raw data to S3 using AWS CLI with partitioned folder structure
-> Attempted to crawl raw data using Glue and identified format issues
-> Built Lambda-based ETL to transform raw data into Parquet
-> Stored cleansed data in a separate S3 bucket
-> Crawled cleansed data using AWS Glue to create catalog tables
-> Queried the data using Amazon Athena for analytics

11. Security and Best Practices

-> Used IAM users and roles instead of root account for daily work
-> Managed access using IAM roles and policies
-> Did not store any AWS credentials in the GitHub repository
-> Followed least-privilege access principle for all services

12. Summary

-> Implemented a complete serverless data engineering pipeline on AWS
-> Built a scalable and cost-efficient ETL process using AWS Lambda
-> Designed a partitioned S3 data lake for raw and cleansed data
-> Enabled SQL-based analytics using AWS Glue and Amazon Athena
-> This project demonstrates practical, real-world data engineering workflows on AWS