from settings.client_connect import client


sheet = client.open('TO')
sheet = sheet.worksheet("car info")
val = sheet.cell(1, 2)
print(val)
print(val.value)
val = sheet.cell(1,1).value
print(val)
if val==None:
    print('pusto')