import smtplib #import smtplib
from email.mime.text import MIMEText #import MIMEText
from email.mime.multipart import MIMEMultipart #import MIMEMultipart
from email.mime.application import MIMEApplication #import MIMEApplication
import datetime
from dotenv import load_dotenv
import os
load_dotenv()

# Function to send email with attachment to the user
def sendEmail(email,new_project,changed_project):
    # Create the message
    msg = MIMEMultipart()
    msg['From'] = os.getenv('from_email')
    
    # Add the email address of the recipient
    msg['To'] = email

    # Add the subject
    msg['Subject'] = datetime.datetime.now().strftime("%m-%d-%Y") + ' - Project Audit'

    html = ''
    if new_project.size > 0:
        html = '<html><body><p>Hi,</p><p>The following projects have been <b>added</b> to the project audit:</p>'
        html += new_project.to_html(index=False, header=True, classes='table table-striped table-hover', justify='center')
        
    else:
        html += '<html><body><p>Hi,</p><p>No new projects <b>added</b> </p>'

    if changed_project.size > 0:
        html += '<p>The following projects have been <b>changed</b> in the project audit:</p><p>'
        html += changed_project.to_html(index=False, header=True, classes='table table-striped table-hover',justify='center')
        
    else:
        html += '<p>No projects <b>changed</b> </p>'
    
    html += '</body></html>'
    msg.attach(MIMEText(html, 'html'))
    
    s = smtplib.SMTP('smtp.office365.com', 587) #set smtp server
    s.starttls() #starttls
    s.login(os.getenv('email_username'), os.getenv('email_password')) #login to smtp server
    s.sendmail(msg['From'],msg['To'], msg.as_string()) #send email
    s.quit() #quit smtp server
    
    
    


        

