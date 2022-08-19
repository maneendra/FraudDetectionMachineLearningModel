'''
Created on 25 Jan 2022

@author: Maneendra Perera
'''
import unittest
unittest.TestLoader.sortTestMethodsUsing = None

from src.data.preprocessing import read_data_from_csv_file
from src.data.preprocessing import remove_single_value_columns
from src.data.preprocessing import check_missing_values_in_column
from src.data.preprocessing import remove_missing_value_rows
from src.data.preprocessing import find_columns_with_high_missing_values
from src.data.preprocessing import drop_columns_by_list
from src.data.preprocessing import find_duplicate_rows
from src.data.preprocessing import remove_duplicate_rows
from src.data.preprocessing import find_cloumns_with_single_value
from src.data.preprocessing import find_columns_with_categorical_data
from src.data.preprocessing import transform_categorical_columns_to_numerical
from src.data.preprocessing import impute_missing_values
from src.data.preprocessing import remove_outliers
from src.data.preprocessing  import find_correlations
from src.data.preprocessing import write_dataframe_to_csv
import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
from sklearn import datasets

class DataPreProcessingTests(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        
        #CSV files for tests
        cls.file_path_with_data = '../resources/application_data.csv';
        cls.file_path_without_data = '../resources/empty_application_data.csv';
        
        #Dataframes for missing value test cases
        list_without_empty_values =[[1, 0], [0, 0]];
        list_with_empty_values = [[1, np.nan],[1, 0]] ;
        cls.df_without_empty_values = pd.DataFrame((list_without_empty_values), columns =['A', 'B']); 
        cls.df_with_empty_values = pd.DataFrame((list_with_empty_values), columns =['A', 'B']);
        
        #Dataframes for duplicate rows test cases
        list_with_duplicate_rows = [[1, 0], [0, 0], [1,0], [1,1]];
        cls.df_with_duplicate_rows = pd.DataFrame((list_with_duplicate_rows), columns =['A', 'B']); 
        list_without_duplicate_rows = [[1, 0], [0, 0], [0,1], [1,1]];
        cls.df_without_duplicate_rows = pd.DataFrame((list_without_duplicate_rows), columns =['A', 'B']);
        
        #Dataframes for single value column test cases
        list_with_single_value_columns = [[1, 0], [2, 0], [3,0], [1,0]];
        cls.df_with_single_value_columns = pd.DataFrame((list_with_single_value_columns), columns =['A', 'B']); 
        list_without_single_value_columns = [[1, 0], [0, 0], [0,1], [1,1]];
        cls.df_without_single_value_columnss = pd.DataFrame((list_without_single_value_columns), columns =['A', 'B']);
        
        #Dataframes for categorical data column test cases
        list_with_categorical_data_columns = [['Good', 0], ['Bad', 0], ['Good',0], ['Bad',0]];
        cls.df_with_categorical_data_columns = pd.DataFrame((list_with_categorical_data_columns), columns =['A', 'B']); 
        list_without_categorical_data_columns = [[1, 0], [0, 0], [0,1], [1,1]];
        cls.df_without_categorical_data_columns = pd.DataFrame((list_without_categorical_data_columns), columns =['A', 'B']);
        
        #Dataframes for outlier removal
        list_without_outliers =[[1, 0], [0, 0]];
        list_with_outliers = [[1, 1],[1, 2],[1, 3],[1, 4],[1, 5],[1, 6],[1, 7],[1, 8],[1, 9],[1, 20]] ;
        cls.df_without_outliers = pd.DataFrame((list_without_outliers), columns =['A', 'B']); 
        cls.df_with_outliers = pd.DataFrame((list_with_outliers), columns =['A', 'B']);
        

    def test_reading_csv_file_with_data(self):
        """Test reading non empty csv file."""
        self.assertTrue(len(read_data_from_csv_file(self.file_path_with_data)) > 0);
    

    def test_reading_csv_file_without_data(self):
        """Test reading an empty csv file."""
        self.assertEqual('empty data', read_data_from_csv_file(self.file_path_without_data));
    

    def test_target_column_missing_values_without_missing_data(self):
        """Test target column has missing values. 
        scenario 1 : when there are no missing values in the target."""
        self.assertEqual(0, check_missing_values_in_column(self.df_without_empty_values, 'B'));
    
    
    def test_target_column_missing_values_with_missing_data(self):
        """Test target column has missing values. 
        scenario 2 : when there are missing values in the target."""
        self.assertEqual(1, check_missing_values_in_column(self.df_with_empty_values, 'B'));
    

    def test_remove_missing_values(self):
        """Test removing missing values from the target column."""
        df = remove_missing_value_rows(self.df_with_empty_values, 'B');
        self.assertTrue(len(df) == 1);


    def test_find_columns_with_high_missing_values(self):
        """Test columns with high missing values - 
        scenario 1 : when there are columns with high missing values """
        threashold = 50;
        self.assertTrue(len(find_columns_with_high_missing_values(self.df_with_empty_values, threashold)) >= 1); 


    def test_find_columns_with_high_missing_values_for_non_empty_df(self):
        """Test columns with high missing values - 
        scenario 1 : when there are no columns with high missing value """
        threashold = 50;
        self.assertTrue(len(find_columns_with_high_missing_values(self.df_without_empty_values, threashold)) == 0); 
        

    def test_drop_columns(self):
        """Test dropping columns when the list of column names are passed"""
        df = drop_columns_by_list(self.df_with_empty_values, 'B')
        self.assertTrue(len(df.columns) == 1);
    
    
    def test_find_duplicate_rows_with_duplicates(self):
        """Test finding duplicate rows
        scenario 1 : when there are duplicate rows"""
        self.assertTrue(find_duplicate_rows(self.df_with_duplicate_rows));
    
    
    def test_find_duplicate_rows_without_duplicates(self):
        """Test finding duplicate rows
        scenario 2 : when there are no duplicate rows"""
        self.assertFalse(find_duplicate_rows(self.df_without_duplicate_rows));
    
           
    def test_remove_duplicate_rows_with_duplicates(self):
        """Test removing duplicate rows
        scenario 1 : when there are duplicate rows"""
        df = remove_duplicate_rows(self.df_with_duplicate_rows);
        self.assertEqual(len(df), 3);
     
    
    def test_remove_duplicate_rows_without_duplicates(self):
        """Test removing duplicate rows
        scenario 2 : when there are no duplicate rows"""
        df = remove_duplicate_rows(self.df_without_duplicate_rows);
        self.assertEqual(len(df), 4);
  

    def test_find_columns_with_a_single_value(self):
        """Test finding columns with single value
        scenario 1 : when there columns with a single value"""
        nunique_threashold = 1;
        self.assertTrue(len(find_cloumns_with_single_value(self.df_with_single_value_columns, nunique_threashold)) == 1);
  
  
    def test_find_columns_without_a_single_value(self):
        """Test finding columns with single value
        scenario 2 : when there are no columns with a single value"""
        nunique_threashold = 1;
        self.assertTrue(len(find_cloumns_with_single_value(self.df_without_single_value_columnss, nunique_threashold)) == 0);
        
        
    def test_remove_columns_with_a_single_value(self):
        """Test removing columns with single value
        scenario 1 : when there columns with a single value"""
        df = remove_single_value_columns(self.df_with_single_value_columns, 'B');
        self.assertTrue(len(df.columns)==1);
     
     
    def test_find_categorical_data_colums_with_categorical_data(self):
        """Test finding columns with categorical data
        scenario 1 : when there are categorical data columns"""
        self.assertTrue(len(find_columns_with_categorical_data(self.df_with_categorical_data_columns)) == 1);
     
     
    def test_find_categorical_data_colums_without_categorical_data(self):
        """Test finding columns with categorical data
        scenario 2 : when there are no categorical data columns"""
        self.assertTrue(len(find_columns_with_categorical_data(self.df_without_categorical_data_columns)) == 0);
     
     
    def test_transform_categorical_column_to_numerical_column(self):
        """Test transforming columns with categorical data to numerical
        scenario 1 : when there are categorical data columns"""
        le = LabelEncoder()
        df = transform_categorical_columns_to_numerical(le, self.df_with_categorical_data_columns, 'A');
        self.assertFalse(df.all().dtypes == 'object')
       
       
    def test_impute_missing_values(self):
        """Test imputing missing values."""
        self.assertTrue(impute_missing_values(self.df_with_empty_values).any().isna().sum() == 0)
    
    
    def test_outlier_removal_with_outliers(self):
        """Test removing outliers by column
        scenario 1 - when there are columns with outliers"""
        before_shape = self.df_with_outliers.shape;
        df = remove_outliers(self.df_with_outliers, 'B');
        after_shape = df.shape;
        self.assertNotEqual(before_shape, after_shape);
       
       
    def test_outlier_removal_without_outliers(self):
        """Test removing outliers by column
        scenario 1 - when there are no columns with outliers"""
        before_shape = self.df_without_outliers.shape;
        df = remove_outliers(self.df_without_outliers, 'A');
        after_shape = df.shape;
        self.assertEqual(before_shape, after_shape);
        
     
    def test_find_correlations(self):
        """Test finding correlations with the target."""
        iris = datasets.load_iris();
        data1 = pd.DataFrame(data= np.c_[iris['data'], iris['target']],
                     columns= iris['feature_names'] + ['target'])
        self.assertTrue(find_correlations(data1, 'target').all() > 0.5);
        
        
    def test_write_dataframe_to_csv(self):
        """Test writing dataframe to csv"""
        path= 'C:/Users/49152/Documents/Thesis-TDD/git/TDD-FraudeDetection-GCP-Project/resources/processed_application_data.csv';
        #path = '../resources/processed_application_data.csv';
        self.assertTrue(write_dataframe_to_csv(self.df_without_empty_values, path));
        self.assertTrue(len(read_data_from_csv_file(path)) > 0)
      
        
if __name__ == '__main__':
    unittest.main()
        
        
        
        
        
    
    