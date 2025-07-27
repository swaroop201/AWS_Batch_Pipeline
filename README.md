# Data Engineering
## Project: Serverless ETL

## Project Overview
The National Stock Exchange of India Limited (NSE) is the leading stock exchange of India, located in Mumbai. NSE was established in 1992 as the first dematerialized electronic exchange in the country. NSE was the first exchange in the country to provide a modern, fully automated screen-based electronic trading system which offered easy trading facility to the investors spread across the length and breadth of the country.

Historical data spanning close to 20 years has been sourced in CSV format. This is broken down into chunks of one month each. Going forward, data would be sourced monthly. 

Ask is to:
- Build a serverless ETL to transform source data into compressed columnar format to support analytics. 
- Source and transformed data to be hosted on S3. 
- Source data to be archived periodically.
- ETL process to have an alerting mechanism. 
- Data Sourcing not in scope.

### Architecture

#### Incremental Load
- ![Process Flow](architecture_incremental.png)

- Ingestion
	- Data sourced monthly in CSV format and uploaded into a S3 bucket
	- S3 event trigger enabled to invoke Lambda Function on upload of object
	- Lifecycle rule enable to archive objects every 3 days into S3 Glacier

- Transformation
	- Lambda Function #1
		- Invoked on upload of source file. Functionality:
		- Sends out feed arrival alert
		- Triggers Glue job
	- Glue Job
		- Transforms stock data into columnar Parquet format, partitioned by year & month
		- Bookmark feature to be enabled to process only new feeds
		- Transforms company data into columnar Parquet format
	- CloudWatch Event
		- Event Rule setup to trigger Lambda function on state change of Glue Job 
	- Lambda Function #2
		- Invoked by CloudWatch event rule
		- Sends out feed processing status
		- Invokes Glue Crawler
	- Glue Crawler
		- Invoked by Lambda function
		- Crawler updates Data Catalog
	- Athena
		- Setup to reference Glue's Data Catalog and leveraged for analytics

#### History Load
- ![Process Flow](architecture_history.png)

- Incremental load's setup can be leverged with some tweaks:
	- S3 event trigger to be disabled
	- Lambda Function #1 not required
	- Glue job to be manually triggered
	- Additional on-demand Glue job to load date dimension

### Pre-requisites

An Amazon Web Services [AWS] account with access to following services: 

- [AWS Lambda](https://aws.amazon.com/lambda/)
- [AWS Glue](https://aws.amazon.com/glue/)
- [AWS SES](https://aws.amazon.com/ses/)
- [AWS CloudWatch](https://aws.amazon.com/cloudwatch/)
- [AWS IAM](https://aws.amazon.com/iam/)
- [Amazon S3](https://aws.amazon.com/s3/)
- [Amazon Athena](https://aws.amazon.com/athena/)

Note: Code base is on **Python 3.7**.

### Code

Three Python files:

- `lambda-trigger-glue-job.py`: Lambda function to trigger Glue Job and send out notifications.
- `lambda-trigger-glue-crawler.py`: Lambda function to trigger Glue Crawler and send out notifications.
- `glue-etl.py`: Glue ETL to transform CSV into partitioned Parquets.


### Data
Historical source data in CSV format is in the form of multiple files - each stock file has records for a single stock from 2000 onwards. There are 1386 files in all. Additionally, there is one static file mapping the stock symbol to the company.

Dataset has been obtained from Kaggle (https://www.kaggle.com/abhishekyana/nse-listed-1384-companies-data).

Dataset contains two categories of data:

1. **Stock Data**: 1386 files in CSV format which contains stock prices for 1364 NSE stocks from 2000 onwards. One record/stock for each trading day. In all, there are 3,758,123 records. Columns include Date, Open, Close, High, Low and Volume.
   - `File Count: 1386`

2. **Company Data**: 1 file in CSV format which maps the Stock Symbol to the Company. Contains 1384 records.
   - `File Count: 1`

### Schema for NSE Stocks
Star Schema made up of one fact and two dimensions would be built. Details:

#### Fact Table
1. **stocks** - stock prices
   - id, symbol, open, high, low, close, adj_close, volume

#### Dimension Tables
2. **date** - date dimension
   - date, year, quarter, month, week, day
3. **companies** - companies to stock mapping
   - id, symbol, company
