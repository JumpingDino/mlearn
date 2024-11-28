# %%
import pandas as pd

# Load the data
# Index(['Notes offered by Prospectus (https://www.lendingclub.com/info/prospectus.action)'], dtype='object')
data = pd.read_csv('lending_club_2017q1.csv')
print(data.columns)

train_filter = ['Jan-2017', 'Feb-2017']
test_filter = ['Mar-2017']

train = data[train_filter]
test = data[test_filter]

# take the train data and do cross-validation training

# 
# %%
import pandas as pd
import numpy as np

def load_data(filename):
    """Loads the data from a CSV file.

    Args:
        filename: The name of the CSV file.

    Returns:
        A pandas DataFrame containing the data.
    """
    data = pd.read_csv(filename)
    return data

def preprocess_data(data):
    """Preprocesses the data for use in a machine learning model.

    Args:
        data: A pandas DataFrame containing the data.

    Returns:
        A pandas DataFrame containing the preprocessed data.
    """
    # Drop irrelevant columns
    data = data.drop(['Notes offered by Prospectus (https://www.lendingclub.com/info/prospectus.action)'], axis=1)

    # Convert categorical features to numerical features
    data = pd.get_dummies(data, columns=['term', 'grade', 'sub_grade', 'emp_length', 'home_ownership', 'verification_status', 'issue_d', 'loan_status', 'purpose', 'addr_state', 'initial_list_status', 'application_type'])

    # Fill missing values
    data = data.fillna(data.mean())

    return data

def split_data(data, test_size=0.2):
    """Splits the data into training and testing sets.

    Args:
        data: A pandas DataFrame containing the data.
        test_size: The proportion of the data to use for testing.

    Returns:
        A tuple containing the training and testing sets.
    """
    from sklearn.model_selection import train_test_split
    X = data.drop(['loan_status'], axis=1)
    y = data['loan_status']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=42)
    return X_train, X_test, y_train, y_test

def evaluate_model(model, X_test, y_test):
    """Evaluates the performance of a machine learning model.

    Args:
        model: The machine learning model to evaluate.
        X_test: The testing data.
        y_test