import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from awsgluedq.transforms import EvaluateDataQuality

args = getResolvedOptions(sys.argv, ['JOB_NAME'])
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

# Default ruleset used by all target nodes with data quality enabled
DEFAULT_DATA_QUALITY_RULESET = """
    Rules = [
        ColumnCount > 0
    ]
"""

# Script generated for node AWS Glue Data Catalog
AWSGlueDataCatalog_node1792445590602 = glueContext.create_dynamic_frame.from_catalog(database="windfarm_database", table_name="windfarm_table", transformation_ctx="AWSGlueDataCatalog_node1792445590602")

# Script generated for node Amazon S3
EvaluateDataQuality().process_rows(frame=AWSGlueDataCatalog_node1792445590602, ruleset=DEFAULT_DATA_QUALITY_RULESET, publishing_options={"dataQualityEvaluationContext": "EvaluateDataQuality_node1792445534325", "enableDataQualityResultsPublishing": True}, additional_options={"dataQualityResultsPublishing.strategy": "BEST_EFFORT", "observations.scope": "ALL"})
AmazonS3_node1792445609313 = glueContext.write_dynamic_frame.from_options(frame=AWSGlueDataCatalog_node1792445590602, connection_type="s3", format="glueparquet", connection_options={"path": "s3://datalake-windfarm-arth", "partitionKeys": []}, format_options={"compression": "snappy"}, transformation_ctx="AmazonS3_node1792445609313")

job.commit()