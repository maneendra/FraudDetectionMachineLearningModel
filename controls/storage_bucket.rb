# Author - Maneendra Perera

title "Storage Bucket Tests"

gcp_project_id = input("gcp_project_id")

# Verify that the storage bucket exists.
control "storage-bucket-test-1" do
	impact 1.0                                                                  
	title "Test storage bucket exists and its name." 
	describe google_storage_buckets(project: 'ultra-palisade-339421') do
		its('count') { should be == 4}
		its('bucket_names'){ should include "fraud_detection_data_bucket" }
	end
end

# Verify that the dataset exists.
control "storage-bucket-test-2" do                                                    
	impact 1.0                                                                  
	title "Test fraud detection dataset exists and its name."  
	describe google_storage_bucket_object(bucket: 'fraud_detection_data_bucket',  object: 'fraud_detection_data.csv') do
		it { should exist }
		its('size') { should be > 0 }
		its('content_type') { should eq "text/plain; charset=utf-8" }
	end
end

# Verify that the dataset exists.
control "storage-bucket-test-3" do                                                    
	impact 1.0                                                                  
	title "Test bank note test dataset exists and its name."  
	describe google_storage_bucket_object(bucket: 'fraud_detection_data_bucket',  object: 'bank_note_test_data.csv') do
		it { should exist }
		its('size') { should be > 0 }
		its('content_type') { should eq "text/plain; charset=utf-8" }
	end
end

# Verify that the dataset exists.
control "storage-bucket-test-4" do                                                    
	impact 1.0                                                                  
	title "Test fraud detection processed dataset exists and its name."  
	describe google_storage_bucket_object(bucket: 'fraud_detection_data_bucket',  object: 'processed_fraud_data.csv') do
		it { should exist }
		its('size') { should be > 0 }
		its('content_type') { should eq "text/plain; charset=utf-8" }
	end
end

# Verify that the dataset exists.
control "storage-bucket-test-5" do                                                    
	impact 1.0                                                                  
	title "Test fraud detection processed dataset exists and its name."  
	describe google_storage_bucket_object(bucket: 'fraud_detection_data_bucket',  object: 'filtered_processed_fraud_data.csv') do
		it { should exist }
		its('size') { should be > 0 }
		its('content_type') { should eq "text/plain; charset=utf-8" }
	end
end
