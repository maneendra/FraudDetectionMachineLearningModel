resource "google_project" "my_project" {
  name       = "Fraud Detection Project"
  project_id = "ultra-palisade-339421"
}


resource "google_app_engine_application" "app" {
  project     = google_project.my_project.project_id
  location_id = "us-central"
}