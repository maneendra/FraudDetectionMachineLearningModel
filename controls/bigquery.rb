# Author - Maneendra Perera

title "Bigquery Tests"

gcp_project_id = input("gcp_project_id")

# Verify fraud detection dataset exists.
control "bigquery-test-1" do                                                   
	impact 1.0                                                                  
	title "Test fraud detection dataset exists."  
	describe google_bigquery_datasets(project: gcp_project_id) do
		its('count') { should be == 1 }
	end
end

# Verify fraud detection dataset name.
control "bigquery-test-2" do                                                    
	impact 1.0                                                                  
	title "Test fraud detection dataset name."  
	describe google_bigquery_datasets(project: gcp_project_id) do
		its('friendly_names') { should include 'fraud_detection_dataset' }
	end
end

# Verify fraud detection table exists.
control "bigquery-test-3" do                                                    
	impact 1.0                                                                  
	title "Test fraud detection table exists."  
	describe google_bigquery_table(project: gcp_project_id, dataset: 'fraud_detection_dataset', name: 'fraud_data_table') do
		it { should exist }
		its('description') { should eq 'fraud_data_table' }
	end
end

# Verify trasaction fraud data table exists.
control "bigquery-test-4" do                                                    
	impact 1.0                                                                  
	title "Test transaction fraud data table exists."  
	describe google_bigquery_table(project: gcp_project_id, dataset: 'fraud_detection_dataset', name: 'transaction_fraud_status_data_table') do
		it { should exist }
		its('description') { should eq 'transaction_fraud_status_data_table' }
	end
end
