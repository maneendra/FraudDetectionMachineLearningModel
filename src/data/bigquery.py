'''
Created on 25 Jan 2022

@author: Maneendra Perera

https://github.com/GoogleCloudPlatform/python-docs-samples/blob/main/notebooks/rendered/getting-started-with-bigquery-ml.md


https://cloud.google.com/automl-tables/docs/features

https://cloud.google.com/automl-tables/docs/prepare


'''

from google.cloud import bigquery

def create_bigquery_connection(project_id):
    """Create the client connection to connect BigQuery ML."""
    
    client = bigquery.Client(project=project_id);
    # Perform the query.
    QUERY = (
        'SELECT * FROM `fraud_detection_dataset.fraud_data_table` '
        'LIMIT 1');
    query_job = client.query(QUERY);
    rows = query_job.result();
        
    if(rows.total_rows == 1):
        return True;