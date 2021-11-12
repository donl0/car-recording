from settings.client_connect import client


sheet = client.open('TO')
sheet = sheet.worksheet("car info")
val = sheet.cell(1, 2)
val = sheet.cell(1,1).value
if val==None:
    print('pusto')