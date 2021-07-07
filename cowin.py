#!/usr/bin/env python
# coding: utf-8

# In[265]:


import requests
from tabulate import tabulate
from datetime import date
import time
import smtplib
from email.message import EmailMessage
import imaplib, email
from datetime import datetime


pin_code = input("Enter PINCODE (Eg - 110075) ")
if len(pin_code)!=6:
    raise KeyError("Please Enter a Valid Pin Code")

age_group = input("Enter Age (Default 18) ")
if age_group=="":
    age_group = "18"
age_group = int(age_group)
if age_group<45 and age_group>=18:
    age_group = 18
elif age_group>=45:
    age_group = 45
elif age_group<18:
    age_group = 17

to_email = input("Enter Email Id to recieve Slot Updates (Not Mandatory) ")
if to_email!="":
    at_rate = to_email.find("@")
    com = to_email.find("com")
    mail_port = to_email.find("gmail")
    if at_rate==-1 and com==-1 and mail_port==-1:
        raise KeyError("Email Incorrect")
    
hours_to_run = (input("Enter Number of Days you want the Script to run (Default = 2days)(Runs Twice a Day) "))
if hours_to_run==0:
    hours_to_run = (input("Enter Number of Days other than 0 "))
if hours_to_run=="":
    hours_to_run = "2"
hours_to_run = int(hours_to_run)
print()
                
                

for i in range(hours_to_run*2):
    
    today = date.today()
    date = today.strftime("%d-%m-%Y")

    api_by_pin = 'https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByPin?pincode='+ pin_code +'&date='+ date

    url = api_by_pin

    json_data = requests.get(url).json()


    formatted_data = json_data['centers']
    count=0
    li = []
    for i in range(len(formatted_data)):


        name_of_hospitals = json_data['centers'][i]['name']
        li.append(name_of_hospitals)

        available_capacity = json_data['centers'][i]['sessions']


        table = [['Dates','Slots_available', 'age_limit', "vaccine"]]

        for j in available_capacity:
            if j["available_capacity"]>0 and j["min_age_limit"]==age_group:
                table.append([j['date'], j["available_capacity"],j["min_age_limit"], j["vaccine"]])


        if len(table)!=1:
            li.append(table)

        else:
            li.append('No slots')


    s = ""
    for i in range(0,len(li),2):
        if li[i+1]=='No slots':
            continue
        else:
            s += li[i]
            s+='\n'
            s += tabulate(li[i+1])
            s+='\n\n'
    if s=="":
        print("No Slots Available Right now")
        print("Come back After 6 Hours")
    else:
        print(s)
        print()
        now = datetime.now()
        dt_string = now.strftime("%d %B %Y  %H:%M")
        print("Update As of "+ dt_string )
        print("Come back After 6 Hours")

    if to_email !="" and s!="":
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        sender_email = "cowintest123@gmail.com"
        sender_password = "Cowin_123"
        server.login(sender_email, sender_password)


        email = EmailMessage()
        email["From"]= sender_email
        email["To"] = to_email
        email["Subject"] = 'Cowin Available Slots'
        email_content = s
        email.set_content(email_content)
        server.send_message(email)

    time.sleep(21600)



        
    





# In[ ]:





# In[ ]:





# In[ ]:




