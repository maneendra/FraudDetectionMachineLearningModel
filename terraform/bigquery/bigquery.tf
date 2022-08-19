resource "google_bigquery_dataset" "dataset" {
  dataset_id                  = "fraud_detection_dataset"
  friendly_name               = "fraud_detection_dataset"
  location                    = "EU"
}

resource "google_bigquery_table" "fraud_data" {
  dataset_id = "fraud_detection_dataset"
  table_id   = "fraud_data_table"
  description = "fraud_data_table"

  external_data_configuration {
    autodetect    = true
    source_format = "CSV"

    source_uris = [
      "gs://fraud_detection_data_bucket/fraud_detection_data.csv",
    ]
  }
}

resource "google_bigquery_table" "transaction_fraud_status_data" {
  dataset_id = "fraud_detection_dataset"
  table_id   = "transaction_fraud_status_data_table"
  description = "transaction_fraud_status_data_table"
	schema = <<EOF
	[
	  {
		"name": "amount",
		"type": "NUMERIC",
		"mode": "REQUIRED",
		"description": "amount"
	  },
	  {
		"name": "category",
		"type": "STRING",
		"mode": "REQUIRED",
		"description": "category"
	  },
	  	  {
		"name": "longitude",
		"type": "NUMERIC",
		"mode": "REQUIRED",
		"description": "longitude"
	  },
	  	  {
		"name": "latitude",
		"type": "NUMERIC",
		"mode": "REQUIRED",
		"description": "latitude"
	  },
	  	  {
		"name": "cc_number",
		"type": "STRING",
		"mode": "REQUIRED",
		"description": "credit card number"
	  },
	  {
		"name": "trans_date_and_time",
		"type": "STRING",
		"mode": "REQUIRED",
		"description": "transaction date and time"
	  },
	  {
		"name": "ml_fraud_status",
		"type": "INT64",
		"mode": "REQUIRED",
		"description": "fraud status from ml model"
	  },
	  {
		"name": "rule_fraud_status",
		"type": "INT64",
		"mode": "REQUIRED",
		"description": "fraud status from rule engine"
	  }
	]
	EOF

}

