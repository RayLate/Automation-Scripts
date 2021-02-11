import win32com.client as win32
import pandas as pd
import os
from pandas import DataFrame, Series
from datetime import datetime
import time

print("Starting Send Email Script")
time.sleep(5)

def mailSend(df):
    outlook = win32.Dispatch('Outlook.application')
    mail = outlook.CreateItem(0)

    if singtelACCNumDict[group][1] == "IMFS":
        mail.To = "munwei@micron.com;michaelwong@micron.com;"
        mail.CC = "f10itmobile@micron.com;rming@micron.com"

    if singtelACCNumDict[group][1] == "F10":
        
        mail.To = "danielkoh@micron.com;zhoutianchi@micron.com"
        mail.CC = "siewkian@micron.com;rming@micron.com;f10itmobile@micron.com;"

    if singtelACCNumDict[group][1] == "MSB":
        mail.To = "tanlihock@micron.com;suhaimi@micron.com"



    mail.Display()
    mail.Subject = f'Mobile Payroll Deduction for Billing {date.strftime("%b")} {date.year} Mobile Usage Excess (Singtel Account number {singtelACCNumDict[group][0]})'
    mail.HTMLbody =f'''
    <p style="font-size: 18px;>Hi,</p>
    <br>
    <p style="font-size: 18px;>Below table for {group} {date.strftime("%b")} {date.year} mobile usage excess deduction. Please review.</p>
    <body>
    <h3>{group} -{singtelACCNumDict[group][0]}</h3>
    {df.to_html()}
    </body>
    <p style="font-size: 18px;><br></p>
    <p style="font-size: 18px;>Thank you</p>
    '''

    mail.Send()
    
    
print('Running SendEmail Code')

singtelACCNumDict = {
    '5H7400' : [60565907,'F10'],
    'Assignees' : [60565907,'F10'],
    'Facilities' : [60440207,'F10'],
    'FINAlice' : [60392890,'F10'],
    'FINOPS' : [60403052,'F10'],
    'FINTAX' : [60399258,'F10'],
    'FIN Treasury' : [60392954,'F10'],
    'HR' : [60263220,'F10'],
    'IMFS' : [18175293,'IMFS'],
    'MSB' : [60662571,'MSB'],
    'Procurement' : [60201960,'F10'],
    'Quality' : [60266156,'F10'],
    'SSC' : [19513638,'F10'],
    'STC' : [30956166,'F10'],
    'TECH' : [30784198,'F10'],
    'WWOpsBB20701709' : [20701709,'F10'],
    'WWOpsMobile30404184' : [30404184,'F10'],
}


print(os.path.dirname(os.path.abspath(__file__)))
# Current Dir Path
path = os.path.dirname(os.path.abspath(__file__))
group = path.split('\\')[-2].split('_')[-1]

# Read Excel
df = pd.read_excel(f'{path}\VIP&DUTY&COMMON.xlsx',sheet_name=(-2))

# DataFrame
billdf = df[df['Bill Amount to be deducted'] > 0].copy()
billdf = billdf[billdf['Type'].isnull() == True]
billdf.drop(columns=['Type'],inplace=True)
billdf.sort_values(by=['Bill Amount to be deducted'],ascending=False,inplace=True)
billdf['Non Business Cost'].fillna(0,inplace=True)
billdf['Micron ID']=billdf['Micron ID'].astype(str)
billdf = billdf.append(billdf.sum(numeric_only=True), ignore_index=True)

# Bill Date
try:
    date = billdf['Bill Date'][0]
except:
    date = datetime.now()

print(billdf)


waiting = True
while waiting:
    userinput = str(input('Send Email y/n ? ').lower())
    if userinput == 'y':
        mailSend(billdf)
        break
    
    elif userinput == 'n':
        break
    
    else:
        print("Please input only y or n")
    

