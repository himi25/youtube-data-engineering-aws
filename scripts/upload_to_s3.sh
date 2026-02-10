#!/bin/bash

# Replace this with your raw bucket name
RAW_BUCKET="s3://dataeng-on-youtube-raw-useast1-dev-2026"

# Copy all JSON reference data
aws s3 cp . $RAW_BUCKET/youtube/raw_statistics_reference_data/ \
  --recursive --exclude "*" --include "*.json"

# Copy all CSV data files using Hive-style partitioning
aws s3 cp CAvideos.csv $RAW_BUCKET/youtube/raw_statistics/region=ca/
aws s3 cp DEvideos.csv $RAW_BUCKET/youtube/raw_statistics/region=de/
aws s3 cp FRvideos.csv $RAW_BUCKET/youtube/raw_statistics/region=fr/
aws s3 cp GBvideos.csv $RAW_BUCKET/youtube/raw_statistics/region=gb/
aws s3 cp INvideos.csv $RAW_BUCKET/youtube/raw_statistics/region=in/
aws s3 cp JPvideos.csv $RAW_BUCKET/youtube/raw_statistics/region=jp/
aws s3 cp KRvideos.csv $RAW_BUCKET/youtube/raw_statistics/region=kr/
aws s3 cp MXvideos.csv $RAW_BUCKET/youtube/raw_statistics/region=mx/
aws s3 cp RUvideos.csv $RAW_BUCKET/youtube/raw_statistics/region=ru/
aws s3 cp USvideos.csv $RAW_BUCKET/youtube/raw_statistics/region=us/
