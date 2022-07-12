import datetime
from unicodedata import name
import logging
import salesforce as sf
import emailResults as email

logging.basicConfig(level=logging.INFO)


def get_search_date(): #
    today = datetime.date.today() #get current date
    search_date = today -datetime.timedelta(days=30) #get date 30 days ago
    date = str(search_date) + "T00:00:00.000Z" #convert date to string
    return date

query = "SELECT i360__Project_Number__c,supportworks__Install_Date__c,i360__Customer_Name__c,i360__Market_Segment__c,i360__Status__c FROM i360__Project__c WHERE supportworks__Install_Date__c >= "+get_search_date()+" AND i360__Status__c != 'Completed' ORDER BY supportworks__Install_Date__c ASC"

def __main__():
    data = sf.get_data(query)   
    data = sf.rename_columns(data)
    # data = sf.get_names(data)
    
    new_projects = sf.get_new_projects(data)
    new_projects.to_csv('new_projects.csv', index=False)
    
    changed_projects = sf.get_changed_projects(data)
    changed_projects.to_csv('changed_projects.csv', index=False)
    
    new_projects = sf.update_datetime(new_projects)
    changed_projects = sf.update_datetime(changed_projects)
    
    
    email.sendEmail('projectaudit@goterrafirma.com',new_projects,changed_projects)
    
    data.to_csv('data.csv')
    return 0

if __name__ == '__main__':
    __main__()





