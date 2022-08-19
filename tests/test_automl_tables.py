'''
Created on 11 Feb 2022

@author: Maneendra Perera
'''
from src.data.automl_tables import create_automl_table_client
from src.data.automl_tables import create_automl_dataset
from src.data.automl_tables import import_data_to_automl_dataset
from src.data.automl_tables import create_automl_model;
from src.data.automl_tables import get_automl_long_running_operation_status;
from src.data.automl_tables import get_automl_model;
from src.data.automl_tables import get_automl_model_evaluations;
from src.data.automl_tables import get_automl_model_online_prediction;
from src.data.automl_tables import deploy_automl_model;
from src.data.automl_tables import undeploy_automl_model;

import io
import unittest
unittest.TestLoader.sortTestMethodsUsing = lambda self, a, b: (a < b) - (a > b)

import sys

class AutomlTableTests(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        cls.project_id = 'ultra-palisade-339421';
        cls.compute_region = 'eu';
        cls.dataset_display_name = 'test_dataset';
        cls.dataset_path = 'gs://fraud_detection_data_bucket/bank_note_test_data.csv';
        
        cls.model_display_name = 'test_model';
        cls.train_budget_milli_node_hours = 1000;
        cls.include_column_spec_names=None;
        cls.target_column = 'Target';
        cls.exclude_column_spec_names='Target';
        
        cls.operation_full_id = 'projects/221186022478/locations/eu/operations/TBL2619856933036752896';

        cls.input_for_zero_target = {'variance': 1, 'skewness': 3.1329, 'curtosis': 1, 'entropy': 2};
        cls.input_for_one_target = {'variance': -0.8471, 'skewness': 3.1329, 'curtosis': -3.0112, 'entropy': -2.9388};
        
        
    def test_automl_table_client(self):
        """Test creating Auto ML table client connection."""
        capturedOutput = io.StringIO();
        sys.stdout = capturedOutput 
        create_automl_table_client(self.project_id, self.compute_region);
        sys.stdout = sys.__stdout__
        self.assertIn('ListDatasetsPager', capturedOutput.getvalue());
       
         
    def test_automl_dataset(self):
        """Test creating dataset in AutoMl."""
        client = create_automl_table_client(self.project_id, self.compute_region);
        dataset = create_automl_dataset(client, self.dataset_display_name);
        dataset_name = format(dataset.display_name);
        print("Dataset display name: {}".format(dataset.display_name));
        self.assertEqual(self.dataset_display_name, dataset_name);
    
    
    #This can be run once. If we run the import dataset twice for the same dataset it will throw
    #the error - As Currently, we only support one import per dataset. Please create another dataset to import.   
    def test_automl_import_data_to_dataset(self):
        """Test importing data to the dataset in AutoMl.
        scenario 1 : run for the first time"""
        client = create_automl_table_client(self.project_id, self.compute_region);
        response = import_data_to_automl_dataset(client, self.dataset_path, self.dataset_display_name);
        self.assertIn('', format(response.result()));
    
    
    def automl_import_data_to_dataset_multiple_times(self):
        """Test importing data to the dataset in AutoMl.
        scenario 1 : run for the second time"""
        client = create_automl_table_client(self.project_id, self.compute_region);
        response = import_data_to_automl_dataset(client, self.dataset_path, self.dataset_display_name);
        self.assertIn('we only support one import per dataset', format(response.result()));
    
    
    def test_automl_create_model(self):
        """Test creating model in AutoMl."""
        client = create_automl_table_client(self.project_id, self.compute_region);
        client.set_target_column(
            dataset_display_name=self.dataset_display_name,
            column_spec_display_name=self.target_column
        );
        response = create_automl_model(client, self.dataset_display_name, self.target_column, 
                                       self.model_display_name, self.train_budget_milli_node_hours, 
                                       None, None);
        print('Operation id : ', response.operation.id);
        self.assertTrue(len(response.operation.id)>0);
                
             
    def test_get_automl_long_running_operation_status(self):
        """Test retrieving operational status."""
        client = create_automl_table_client(self.project_id, self.compute_region);
        operation_status = get_automl_long_running_operation_status(client, self.operation_full_id);
        self.assertEqual(self.operation_full_id, operation_status.name);
        self.assertEqual('type.googleapis.com/google.cloud.automl.v1beta1.OperationMetadata', operation_status.metadata.type_url);
        self.assertEqual('True', operation_status.done);
    
    
    #Before deploying the model, the deployment state will be deployment_status=undeployed.       
    def test_get_automl_model(self):
        """Test retrieving model deployment status."""
        client = create_automl_table_client(self.project_id, self.compute_region);
        model = get_automl_model(client, self.model_display_name);
        self.assertEqual('TBL3696210646908534784', model.name.split("/")[-1]);
        self.assertEqual('2', format(model.deployment_state));
        
            
    def test_get_automl_model_evaluations(self):
        """Test retrieving model evaluations."""
        client = create_automl_table_client(self.project_id, self.compute_region);
        evaluations = get_automl_model_evaluations(client, self.model_display_name, None);
        self.assertTrue(evaluations>0.8);
    
    
    #Deploy model does not return success
    def test_deploy_automl_model(self):
        """Test deploying AutoML model."""
        client = create_automl_table_client(self.project_id, self.compute_region);
        response = deploy_automl_model(client, self.model_display_name);
        self.assertEqual('', response);
    
    
    #After deploying the model, the deployment state will be deployment_status=deployed.
    def test_deploy_automl_model_status_after_deployed(self):
        """Test retrieving model deployment status after deploying the model."""
        client = create_automl_table_client(self.project_id, self.compute_region);
        model = get_automl_model(client, self.model_display_name);
        self.assertEqual('1', format(model.deployment_state));
        
           
    def test_get_automl_model_online_prediction_for_zero_target(self):
        """Test retrieving online model prediction
        scenario 1 - result is 0."""
        client = create_automl_table_client(self.project_id, self.compute_region);
        prediction = get_automl_model_online_prediction(client, self.model_display_name, self.input_for_zero_target);
        self.assertEqual(0, prediction);
    
      
    def test_get_automl_model_online_prediction_for_one_target(self):
        """Test retrieving online model prediction
        scenario 1 - result is 1."""
        client = create_automl_table_client(self.project_id, self.compute_region);
        prediction = get_automl_model_online_prediction(client, self.model_display_name, self.input_for_one_target);
        self.assertEqual('1', prediction);
        
         
    def test_undeploy_automl_model(self):
        """Test undeploying AutoML model."""
        client = create_automl_table_client(self.project_id, self.compute_region);
        response = undeploy_automl_model(client, self.model_display_name);
        print(response);
        self.assertContains('google.api_core.operation.Operation', response);
        
        
    #After undeploying the model, the deployment state will be deployment_status=undeployed.
    def test_deploy_automl_model_status_after_undeployed(self):
        """Test retrieving model deployment status after undeploying the model."""
        client = create_automl_table_client(self.project_id, self.compute_region);
        model = get_automl_model(client, self.model_display_name);
        self.assertEqual('2', format(model.deployment_state));
    
    
if __name__ == '__main__':
    unittest.main()
        
        
        

    