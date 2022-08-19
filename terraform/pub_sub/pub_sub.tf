resource "google_pubsub_topic" "fraud-detection" {
  name = "transaction-topic"
  project = "ultra-palisade-339421"

  message_retention_duration = "86600s"
}

resource "google_pubsub_subscription" "fraud-detection" {
  name  = "transaction-pull-subscription"
  project = "ultra-palisade-339421"
  topic = google_pubsub_topic.fraud-detection.name
}

resource "google_pubsub_topic" "fraud-detection-status" {
  name = "fraud-status-topic"
  project = "ultra-palisade-339421"

  message_retention_duration = "86600s"
}

resource "google_pubsub_subscription" "fraud-detection-status" {
  name  = "fraud-status-pull-subscription"
  project = "ultra-palisade-339421"
  topic = google_pubsub_topic.fraud-detection-status.name
}

resource "google_pubsub_topic" "transaction-status" {
  name = "transaction-status-topic"
  project = "ultra-palisade-339421"

  message_retention_duration = "86600s"
}

resource "google_pubsub_subscription" "transaction-status" {
  name  = "transaction-status-pull-subscription"
  project = "ultra-palisade-339421"
  topic = google_pubsub_topic.transaction-status.name
}