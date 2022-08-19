'''
Created on 11 Feb 2022

@author: Maneendra Perera
'''
from google.cloud import automl_v1beta1 as automl
from google.cloud.automl_v1.types.model_evaluation import ModelEvaluation



def create_automl_table_client(project_id, compute_region):
    """Create the client connection to connect AutoML Tables."""
    
    client_options = {'api_endpoint': 'eu-automl.googleapis.com:443'}
    client = automl.TablesClient(project=project_id, region=compute_region, client_options=client_options);
    #print(client.list_datasets());
    return client;


def create_automl_dataset(client, dataset_display_name):
    """Create the dataset to be used in the model."""
    
    dataset = client.create_dataset(dataset_display_name);
    print("Dataset name: {}".format(dataset.name));
    print("Dataset id: {}".format(dataset.name.split("/")[-1]));
    print("Dataset display name: {}".format(dataset.display_name));
    return dataset;
    
    
def import_data_to_automl_dataset(client, dataset_path, dataset_display_name):
    """Import the data to dataset, either from bigquery table or cloud storage bucket."""
    
    response = None
    if dataset_path.startswith("bq"):
        response = client.import_data(
        dataset_display_name=dataset_display_name, bigquery_input_uri=dataset_path
    );
    else:
    # Get the multiple Google Cloud Storage URIs.
        input_uris = dataset_path.split(",")
        response = client.import_data(
            dataset_display_name=dataset_display_name,
            gcs_input_uris=input_uris,
    );
    print("Processing import...");
    print("Data imported. {}".format(response.result()));
    return response;


def create_automl_model(client, dataset_display_name, target_column, model_display_name, train_budget_milli_node_hours, include_column_spec_names, exclude_column_spec_names):
    """Create the machine learning model."""
    
    response = client.create_model(model_display_name,
        train_budget_milli_node_hours=train_budget_milli_node_hours,
        dataset_display_name=dataset_display_name,
        include_column_spec_names=include_column_spec_names,
        exclude_column_spec_names=exclude_column_spec_names);

    print("Training model...");
    print("Training operation name: {}".format(response.operation.name));
    print("Training completed: {}".format(response.result()));
    return response;


def get_automl_long_running_operation_status(client, operation_full_id):
    """Get the model creation operation status.
       operation status done will return true once the model is created.
    """
    op = client.auto_ml_client._transport.operations_client.get_operation(operation_full_id);
    print("Operation status: {}".format(op));
    return op;


def get_automl_model(client, model_display_name):
    """Get the model details."""
    
    model = client.get_model(model_display_name=model_display_name);
    # Display the model information.
    print("Model name: {}".format(model.name));
    print("Model id: {}".format(model.name.split("/")[-1]));
    print("Model display name: {}".format(model.display_name));
    print("Model deployment state: {}".format(model.deployment_state));
    return model;


def get_automl_model_evaluations(client, model_display_name, filter):
    """Get the model evaluation results like Precision, Recall, F1 Score, AUPRC, AUROC, log loss."""
    response = client.list_model_evaluations(model_display_name=model_display_name, filter=filter);
    for evaluation in response:
        if evaluation.display_name == '':
            #For the overall evaluation, the display name is empty
            model_evaluation_name = evaluation.name
            break
    
    model_evaluation = client.get_model_evaluation(model_evaluation_name=model_evaluation_name);
    classification_metrics = model_evaluation.classification_evaluation_metrics;
    if str(classification_metrics):
        confidence_metrics = classification_metrics.confidence_metrics_entry;

        # Showing model score based on threshold of 0.5
        print("Model classification metrics (threshold at 0.5):")
        for confidence_metrics_entry in confidence_metrics:
            if confidence_metrics_entry.confidence_threshold == 0.5:
                print('confidence metric : ' , confidence_metrics_entry);
                print("Model Precision: {}%".format(round(confidence_metrics_entry.precision * 100, 2)));
                print("Model Recall: {}%".format(round(confidence_metrics_entry.recall * 100, 2)));
                print("Model F1 score: {}%".format(round(confidence_metrics_entry.f1_score * 100, 2)));
                print("Model AUPRC: {}".format(classification_metrics.au_prc));
                print("Model AUROC: {}".format(classification_metrics.au_roc));
                print("Model log loss: {}".format(classification_metrics.log_loss));
                return classification_metrics.au_roc;
            
            
def deploy_automl_model(client, model_display_name):
    response = client.deploy_model(model_display_name=model_display_name);
    print("Model deployed. {}".format(response.result()));
    return response;
            
            
def get_automl_model_online_prediction(client, model_display_name, inputs):
    """Get the online prediction."""
    response = client.predict(model_display_name=model_display_name, inputs=inputs);
    print("Prediction results:");
    result_0 = 0;
    result_0_value = 0;
    for result in response.payload:
        print("Predicted class name: {}".format(result));
        print("Predicted class name: {}".format(result.tables.value));
        print("Predicted class score: {}".format(result.tables.score));
        if(result.tables.score > result_0 ):
            result_0 = result.tables.score;
            result_0_value = result.tables.value;
    return result_0_value;


def undeploy_automl_model(client, model_display_name):
    response = client.undeploy_model(model_display_name=model_display_name)
    print("Model undeployed. {}".format(response.result()));
    return response;
    

if __name__ == "__main__":
    
    """Create the connection"""
    project_id = 'ultra-palisade-339421';
    compute_region = 'eu';
    client = create_automl_table_client(project_id, compute_region);
    model_display_name = 'filtered_fraud_detection_model_2';
    
    isModelCreated = True;
    if(not isModelCreated):
        
        fraud_dataset_display_name = 'filtered_fraud_dataset_2';
        create_automl_dataset(client, fraud_dataset_display_name);
        
        dataset_path = 'gs://fraud_detection_data_bucket/filtered_processed_fraud_data.csv';
        import_data_to_automl_dataset(client, dataset_path, fraud_dataset_display_name);
        
        train_budget_milli_node_hours = 1000;
        include_column_spec_names=None;
        target_column = 'is_fraud';
        exclude_column_spec_names=['is_fraud', 'data_split'];
        splitting_column='data_split';
        
        client.set_target_column(dataset_display_name=fraud_dataset_display_name,column_spec_display_name=target_column);
        client.set_test_train_column(dataset_display_name=fraud_dataset_display_name, column_spec_display_name=splitting_column);
        create_automl_model(client, fraud_dataset_display_name, target_column, model_display_name, train_budget_milli_node_hours, None, exclude_column_spec_names);
        
        
    isModelDeployed = True;
    
    operation_full_id = 'projects/221186022478/locations/eu/operations/TBL5196232579241476096';
    if(not isModelDeployed):
        operation_status = get_automl_long_running_operation_status(client, operation_full_id);
        if(operation_status.done == True):
            deploy_automl_model(client, model_display_name);
            
            
    input_for_zero_target = {'amt': 15.56, 'category': 'entertainment', 'cc_num': '30263540414123', 'lat': 36.841266, 'long':-111.69076499999998, 'trans_date_trans_time':'2020-06-21 12:12:08'};
    prediction = get_automl_model_online_prediction(client, model_display_name, input_for_zero_target);
    print(prediction)
    
    
            