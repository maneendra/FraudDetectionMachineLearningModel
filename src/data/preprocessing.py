'''
Created on 25 Jan 2022

@author: Maneendra Perera

https://machinelearningmastery.com/basic-data-cleaning-for-machine-learning/

https://scikit-learn.org/stable/modules/impute.html

https://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.LabelEncoder.html

https://www.kaggle.com/nareshbhat/fraud-detection-feature-selection-over-sampling

https://www.geeksforgeeks.org/detect-and-remove-the-outliers-using-python/

https://www.upgrad.com/blog/data-preprocessing-in-machine-learning/

https://towardsdatascience.com/feature-selection-with-pandas-e3690ad8504b

'''
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.impute import SimpleImputer
import numpy as np

def read_data_from_csv_file(path):
    """Read data from csv files."""
    
    try:
        fraud_data = pd.read_csv(path);
        return fraud_data;
    except:
        return 'empty data';


def check_missing_values_in_column(df, target_column_name):
    """Check missing values in the column."""
    
    missing_value_count = df[target_column_name].isna().sum();
    return missing_value_count;


def remove_missing_value_rows(df, target_column_name):
    """Remove rows that has missing values."""
    
    df = df.dropna(subset=[target_column_name]);
    return df;
    
    
def find_columns_with_high_missing_values(df, threashold):
    """Find columns with high missing values."""
    
    missing_count = df.isna().sum().sort_values(ascending = False);
    missing_count = missing_count[missing_count>0];
    print('Missing count : {}'.format(missing_count));
    missing_percentage = (missing_count/len(df))*100
    missing_percentage = missing_percentage[missing_percentage>=threashold]
    print('Missing percentage : {} ', missing_percentage)
    df_percentage = pd.DataFrame({'target_column_name':missing_percentage.index, 'percentage':missing_percentage.values})
    df_percentage = df_percentage.iloc[:, 0]
    df_percentage_list = df_percentage.tolist();
    print('Column count : {} ', len(df_percentage))
    return df_percentage_list;


def drop_columns_by_list(df, column_list):
    """Drop columns."""
    
    df = df.drop(columns=column_list);
    return df;


def find_duplicate_rows(df):
    """Find duplicate rows."""
    
    duplicates = df.duplicated();
    return duplicates.any();


def remove_duplicate_rows(df):
    """Remove duplicate rows."""
    
    df = df.drop_duplicates();
    return df;


def find_cloumns_with_single_value(df, nunique_threashold):
    """Find columns that have only a single column."""
    
    df_nunique = df.nunique();
    print('No of unique values : {} '.format(df_nunique));
    df_nunique = df_nunique[df_nunique == nunique_threashold];
    df_nunique = pd.DataFrame({'target_column_name':df_nunique.index, 'nunique_values':df_nunique.values});
    df_nunique = df_nunique.iloc[:, 0];
    columns_with_a_single_value = df_nunique.tolist();
    print('Columns with a single value : {} '.format(columns_with_a_single_value));
    return columns_with_a_single_value;


def remove_single_value_columns(df, nunique_cloumn_list):
    """Remove columns that have only a single column."""
    
    df = df.drop(columns=nunique_cloumn_list);
    return df;


def find_columns_with_categorical_data(df):
    """Find categorical columns."""
    
    obj_columns = (df.dtypes == 'object');
    obj_columns = list(obj_columns[obj_columns].index);
    print('Object columns : {} '.format(obj_columns));
    return obj_columns;


def transform_categorical_columns_to_numerical(lEncoder, df, target_column_name):
    """Transform categorical columns to numerical."""
    
    df[target_column_name] = lEncoder.fit_transform(df[target_column_name]);
    return df;


def impute_missing_values(df):
    """Impute missing values."""
    
    imp = SimpleImputer(missing_values=np.nan, strategy='mean');
    imp.fit(df);
    df_transformed = imp.transform(df);
    df = pd.DataFrame(df_transformed, columns = df.columns);
    #print('Imputed df : ', df)
    return df


def remove_outliers(df, target_column_name):
    """Remove outliers using Inter Quartile Range."""
    
    Q1=df[target_column_name].quantile(0.25);
    Q3=df[target_column_name].quantile(0.75);
    IQR=Q3-Q1;
    lower=Q1 - 1.5 * IQR;
    upper=Q3 + 1.5 * IQR;
    print(lower,upper);
    new_df = df[(df[target_column_name] > lower) & (df[target_column_name] < upper)];
    print('Dataframe after removing outliers : {}'.format(new_df));
    return new_df;


def find_correlations(df, target_variable):
    """Find correlations."""
    
    correlations = df.corr();
    print('Correlations : {} '.format(correlations));
    cor_target = abs(correlations[target_variable]);
    print('with target : {} '.format(cor_target));
    relevant_features = cor_target[cor_target>0.5];
    print('Relevant features : {} '.format(relevant_features));
    return relevant_features


def write_dataframe_to_csv(df, path):
    """Write pre processed data to a CSV file."""
    
    df.to_csv(path, index = False, header=True);
    return True;


if __name__ == "__main__":
    
    path = r'C:\Users\49152\Documents\Thesis-TDD\data\withsplit\combined_csv_with_labels.csv';
    df = read_data_from_csv_file(path);
    print(df.head(5));
    
    target_column_name = 'is_fraud';
    missing_count = check_missing_values_in_column(df, target_column_name);
    print('Missing value count for TARGET: ', missing_count);
    
    if missing_count > 0:
        df = remove_missing_value_rows(df, target_column_name);
        
    threashold = 50;
    df_missing_column_list = find_columns_with_high_missing_values(df, threashold);
    print('Columns with missing values: ', missing_count);
    df = drop_columns_by_list(df, df_missing_column_list);
    print(df.head(5))
    
    """Find and remove duplicate rows"""
    found = find_duplicate_rows(df);
    if found:
        df = remove_duplicate_rows(df);
        
    """Find and remove columns with a single value. When all the data are distinct it does not
    add value to the machine learning model.Example : ids column"""
    nunique_threashold = 100;
    nunique_list = find_cloumns_with_single_value(df, nunique_threashold);
    print('Column list with unique values: ', missing_count);
    if len(nunique_list) > 0:
        df = remove_single_value_columns(df, nunique_list)
    
    """This will not needed to AutoML tables,as it automatically handles the categorical data."""
    findCategoricalData = False;
    if findCategoricalData:
        """Find and transform categorical data columns"""
        print('Transforming categorical data to numerical')
        obj_colums = find_columns_with_categorical_data(df);
        lEncoder = LabelEncoder();
        print('Before transformation : ', df[['NAME_CONTRACT_TYPE', 'CODE_GENDER']])
        for i in obj_colums:
            df = transform_categorical_columns_to_numerical(lEncoder, df, i)
        print('After transformation : ', df[['NAME_CONTRACT_TYPE', 'CODE_GENDER']])
        
        
        """Impute missing values"""
        df = impute_missing_values(df);
        print(df)
    
    """Remove columns"""
    df = drop_columns_by_list(df, 'Unnamed: 0')
    print(df)
    
    df = drop_columns_by_list(df, 'gender')
    print(df)
    
    df = drop_columns_by_list(df, 'unix_time')
    print(df)
    
    df = drop_columns_by_list(df, 'zip')
    print(df)
    
    df = drop_columns_by_list(df, 'trans_num')
    print(df)
    
    """Since we are having longitude and latitude, removing the duplicate data"""
    df = drop_columns_by_list(df, 'street')
    print(df)
    
    df = drop_columns_by_list(df, 'state')
    print(df)
    
    df = drop_columns_by_list(df, 'merchant')
    print(df)
    
    df = drop_columns_by_list(df, 'merch_long')
    print(df)
    
    df = drop_columns_by_list(df, 'merch_lat')
    print(df)
    
    df = drop_columns_by_list(df, 'last')
    print(df)
    
    df = drop_columns_by_list(df, 'job')
    print(df)
    
    df = drop_columns_by_list(df, 'first')
    print(df)
    
    df = drop_columns_by_list(df, 'dob')
    print(df)
    
    df = drop_columns_by_list(df, 'city_pop')
    print(df)
    
    df = drop_columns_by_list(df, 'city')
    print(df)
    
    removeOutliers = False;
    if(removeOutliers):
        df = remove_outliers(df, 'EXT_SOURCE_3');
    
    find_correlations(df, 'is_fraud');
    
    path = 'filtered_processed_fraud_data.csv';
    write_dataframe_to_csv(df, path);
    print('Writing data to csv is finished')
    
    
        
    
    