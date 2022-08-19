# copyright: 2018, The Authors

title "PubSub Tests"

gcp_project_id = input("gcp_project_id")

# Verifiy the transaction topic exists.
control "pubsub-test-1" do                                                   
	impact 1.0                                                                  
	title "Test pub sub transaction topic exists."  
	describe google_pubsub_topic(project: gcp_project_id, name: 'transaction-topic') do
	  it { should exist }
	end
end


# Verifiy the subscription for the transaction topic exists.
control "pubsub-test-2" do                                                   
	impact 1.0                                                                  
	title "Test pub sub subscription exists for the transaction topic."  
	describe google_pubsub_subscription(project: gcp_project_id, name: 'transaction-pull-subscription') do
	  it { should exist }
	end
end


#Verifiy the fraud status topic exists.
control "pubsub-test-3" do                                                   
	impact 1.0                                                                  
	title "Test pub sub fraud topic exists."  
	describe google_pubsub_topic(project: gcp_project_id, name: 'fraud-status-topic') do
	  it { should exist }
	end
end


#Verifiy the subscription for the fraud status topic exists.
control "pubsub-test-4" do                                                   
	impact 1.0                                                                  
	title "Test pub sub subscription exists for the fraud topic."  
	describe google_pubsub_subscription(project: gcp_project_id, name: 'fraud-status-pull-subscription') do
	  it { should exist }
	end
end


#Verifiy the transaction status topic exists.
control "pubsub-test-5" do                                                   
	impact 1.0                                                                  
	title "Test pub sub transaction status topic exists."  
	describe google_pubsub_topic(project: gcp_project_id, name: 'transaction-status-topic') do
	  it { should exist }
	end
end


#Verifiy the subscription for the transaction status topic exists.
control "pubsub-test-6" do                                                   
	impact 1.0                                                                  
	title "Test pub sub subscription exists for the transaction status topic."  
	describe google_pubsub_subscription(project: gcp_project_id, name: 'transaction-status-pull-subscription') do
	  it { should exist }
	end
end