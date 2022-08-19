resource "google_storage_bucket" "fraud_detection_data_bucket" {
  name          = "fraud_detection_data_bucket"
  location      = "EU"
  force_destroy = true
}

resource "google_storage_bucket_object" "fraud_detection_data" {
  name   = "fraud_detection_data.csv"
  source = "application_data.csv"
  bucket = "fraud_detection_data_bucket"
}

resource "google_storage_bucket_object" "bank_note_test_data" {
  name   = "bank_note_test_data.csv"
  source = "bank_notes.csv"
  bucket = "fraud_detection_data_bucket"
}

resource "google_storage_bucket_object" "processed_fraud_detection_data" {
  name   = "processed_fraud_data.csv"
  source = "processed_fraud_data.csv"
  bucket = "fraud_detection_data_bucket"
}

resource "google_storage_bucket_object" "filtered_processed_fraud_detection_data" {
  name   = "filtered_processed_fraud_data.csv"
  source = "filtered_processed_fraud_data.csv"
  bucket = "fraud_detection_data_bucket"
}


