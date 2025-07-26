import os
import sys
import boto3

from awsglue.job import Job
from awsglue.transforms import *
from awsglue.context import GlueContext
from awsglue.utils import getResolvedOptions

import pyspark.sql.functions as F
from pyspark.sql import Row, Window, SparkSession
from pyspark.sql.types import *
from pyspark.conf import SparkConf
from pyspark.context import SparkContext


args = getResolvedOptions(sys.argv, ['JOB_NAME'])

sc = SparkContext()
glueContext = GlueContext(sc)
#spark = glueContext.spark_session
spark = SparkSession.builder.config("spark.sql.broadcastTimeout", "600").getOrCreate()
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

spark._jsc.hadoopConfiguration().set("mapreduce.fileoutputcommitter.marksuccessfuljobs", "false")
spark._jsc.hadoopConfiguration().set("parquet.enable.summary-metadata", "false")

### Main data processing
input_dir = "s3://nse-stock-data-landing"
output_dir = "s3://nse-stock-data/aws-glue/output-parquet/"

## Read source Amazon review dataset
stock_prices = spark.read.csv(input_dir, header=True, inferSchema=True)

stock_prices.printSchema()

## Add new columns to dataframe
df = stock_prices \
  .withColumn('year', stock_prices['Date'].substr(1, 4)) \
  .withColumn('month', stock_prices['Date'].substr(6, 2))

## Write out result set to S3 in Parquet format
df.write.partitionBy('year','month').mode('overwrite').parquet(output_dir)

job.commit()
