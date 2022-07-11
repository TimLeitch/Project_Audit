from simple_salesforce import Salesforce
from simple_salesforce import format_soql
import os
from dotenv import load_dotenv
import datetime
import logging
import pandas as pd
logging.basicConfig(level=logging.INFO)

load_dotenv() # Load .env file

sf=Salesforce(username=os.getenv('username'),password=os.getenv('password'),security_token=os.getenv('security_token')) # Create a Salesforce object

def get_data(soql):
    fetch_result = sf.query_all(soql) #get data from salesforce
    data = pd.DataFrame(fetch_result['records']) #convert data to dataframe
    data.drop(['attributes'], axis=1, inplace=True) #drop attributes column
    return data

def rename_columns(data):
    data.rename(columns={'i360__Project_Number__c':'Project Number','supportworks__Install_Date__c':'Install Date','i360__Customer_Name__c':'Customer Name','i360__Market_Segment__c':'Market Segment','i360__Status__c':'Status','LastModifiedById': 'Last Modified By'}, inplace=True)
    return data
    
def get_names(data):
    id = data['Last Modified By'].unique()
    for i in id:
        name = sf.query("SELECT Name FROM i360__Staff__c WHERE i360__User__c = '"+i+"'")
        data.loc[data['Last Modified By'] == i, 'Last Modified By'] = name['records'][0]['Name']
    
    return data
    



def get_new_projects(new):
    old_data = pd.read_csv('data.csv') #read data from csv
    for index, row in old_data.iterrows():
        if row['Project Number'] in new['Project Number'].values:
            new = new[new['Project Number'] != row['Project Number']]
    # new['Install Date'] = pd.to_datetime(new['Install Date']).dt.strftime('%m-%d-%y:%H:%M') #convert install date to datetim
    return new

def get_changed_projects(new):
    old_data = pd.read_csv('data.csv') #read data from csv
    old_data.drop(['Unnamed: 0'], axis=1, inplace=True) #drop unnamed column
    
    new_projects = pd.read_csv('new_projects.csv') #read data from csv
        
    changed = pd.concat([old_data, new], sort=False).drop_duplicates(keep=False) #concatenate old and new data
    changed = changed.drop_duplicates(subset=['Project Number'], keep='last') #drop duplicates
    changed = pd.concat([changed, new_projects], sort=False).drop_duplicates(keep=False) #concatenate old and new data    
    return changed
            
def update_datetime(data):
    data['Install Date'] = pd.to_datetime(data['Install Date']).dt.strftime('%m-%d-%y : %H:%M') #convert install date to datetime
    return data
    

