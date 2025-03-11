import os
import cv2
import json
import pytesseract
import numpy as np
import requests
import re
from datetime import date, datetime, timedelta
import mysql.connector
from PIL import Image

#Paths
setlist = "data/setlist.json"
debugimg = "images/debug.jpg"
captureimg = "images/capture.png"
idblock = "images/idblock.png"
creds = '.secret/sql.cnf'


database = mysql.connector.connect(option_files = '.secret/sql.cnf')

cursor = database.cursor()

#Create new user
#CREATE TABLE 'mtgsort'.'testuser' ('id' varchar(40) NOT NULL, 'name' varchar(150) DEFAULT NULL, 'setname' varchar(100) DEFAULT NULL, 'imageuri' varchar(200) DEFAULT NULL, 'amount' bigint DEFAULT NULL, PRIMARY KEY ('id'));


#Variables
cardtypes = "LCURM"
top = 635
bottom = 680
left = 0
right = 270
loop = 0
check = ""
currset = ""
currtype = ""
cardnumber = 0
activeuser = ""

#Setlist update
setlistupate = False
setupd = ""
setnamupd = ""
setrelupd = ""



#DEBUG FUNCTIONS
debug = True
if debug == True:
    im = Image.open(debugimg)
    im.save(captureimg)
    activeuser = "testuser"
    



#Setlist Update
def insert(setcode, setname, releasedate):
    cursor.execute("INSERT INTO sets (set_code, set_name, release_date) VALUES (%s, %s, %s)on DUPLICATE KEY Update set_code = set_code", (setupd, setnamupd, setrelupd))
    database.commit()

#Refresh Setlist - Need to seperate and update the file intermittently.
if setlistupate == True:
    resp = requests.get('https://api.scryfall.com/sets', 'data')
    data = resp.json()
    length = len(data['data'])

    for info in data['data'][loop]:

        while loop < length:
            setupd = data['data'][loop]['code']
            setnamupd = data['data'][loop]['name']
            setrelupd = data['data'][loop]['released_at']

            if debug == True:
                print(setupd)
                print(setnamupd)
                print(setrelupd)

            cursor.execute("INSERT INTO sets (set_code, set_name, release_date) VALUES (%s, %s, %s)on DUPLICATE KEY Update set_code = set_code", (setupd, setnamupd, setrelupd))
            #database.commit()
            
            loop += 1
            
    database.commit()

cursor.execute("SELECT set_code, set_name, release_date FROM sets")
data = cursor.fetchall()
length = len(data)

#Capture image

print(length)



#Process OCR

image = cv2.imread(captureimg)

clone = image.copy()

crop_img = clone[top:bottom, left:right]

cv2.imwrite(idblock, crop_img)

img = cv2.imread(idblock)

carddetails = pytesseract.image_to_string(img)



os.remove(idblock)
os.remove(captureimg)


#Process the string to an array

if(debug == True):
    print(carddetails[0])
    print(carddetails)

#Define if it is a recognised card type and determine the rarity
if cardtypes.find(carddetails[0]) >= 0:
	currtypetemp = carddetails[0]
	if(debug == True):
		print("It's a card")

if cardtypes.find(carddetails[0]) == -1:
	if(debug == True):
		print("It's not a card")

loop = 0
check = ""


#Determine the set
while loop < length:
	check = data[loop][0].upper()
	if carddetails.count(check) > 0:
		currsetcode = check
		currset = data[loop][0]
	loop += 1

match currtypetemp:
	case "L":
		currtype = "Common"
	case "C":
		currtype = "Common"
	case "U":
		currtype = "Uncommon"
	case "R":
		currtype = "Rare"
	case "M":
		currtype = "Mythic"


p = r'[\d]+' #Regex to find the card number

if re.search(p, carddetails) is not None:
    for catch in re.finditer(p, carddetails):
        cardnumber = catch[0] # catch is a match object
	
else:
	print("No card number found")


#Get card details
resp1 = requests.get('https://api.scryfall.com/cards/search?q=e:'+currsetcode+'+r:'+currtype+'+cn:'+cardnumber)
data1 = resp1.json()

if debug == True:
    print("")
    print('ID: '+data1['data'][0]["id"])
    print('Name: '+data1['data'][0]["name"])
    print('Set: '+data1['data'][0]["set_name"])
    print('Type: '+data1['data'][0]["type_line"])
    print('Rarity: '+data1['data'][0]["rarity"])
    print('Full art: '+str(data1['data'][0]["full_art"]))
    print('Price: $'+str(data1['data'][0]["prices"]["usd"]))
    print('Price foil: $'+str(data1['data'][0]["prices"]["usd_foil"]))
    print('Image: '+data1['data'][0]["image_uris"]["normal"])


#Insert into database  


cursor.execute('INSERT INTO '+activeuser+' (id, name, setname, imageuri, amount) VALUES (%s, %s, %s, %s, 1) on DUPLICATE KEY Update amount = amount + 1', (data1['data'][0]["id"],data1['data'][0]["name"],data1['data'][0]["set_name"],data1['data'][0]["image_uris"]["normal"],))
database.commit()