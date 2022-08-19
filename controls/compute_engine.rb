# Author - Maneendra Perera

title "Compute Engine Tests"

gcp_project_id = input("gcp_project_id")

# Verify the rule engine virtual machine exsists.
control "compute_engine-test-1" do                                                    
	impact 1.0                                                                  
	title "Test compute engine instance exists."  
	describe google_compute_instance(project: gcp_project_id, zone: 'us-central1-a', name: 'rule-engine-instance') do
		it { should exist }
		its('machine_type') { should match 'e2-micro' }
	end
end

#controls for firewalls