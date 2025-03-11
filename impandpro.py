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

database = mysql.connector.connect(user='grant', password='5564177',
                                 host='127.0.0.1',
                                 database='cardstorage')

cursor = database.cursor()



def insert(item, quantity, price):
    cursor.execute("INSERT INTO sets (set_code, set_name, release_date) VALUES (%s, %s, %s)", (item, quantity, price))
    database.commit()
    #database.close()


#Debug use ONLY
debug = True

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

#Setlist update
setlistupate = False
setupd = ""
setnamupd = ""
setrelupd = ""

#Paths
setlist = "data/setlist.json"
debugimg = "images/debug.jpg"
captureimg = "images/capture.png"
idblock = "images/idblock.png"

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

            print(setupd)
            print(setnamupd)
            print(setrelupd)

            insert(setupd, setnamupd, setrelupd)
            

            loop += 1


    setlistupate = False
else:
    with open(setlist) as f:
        data = json.load(f)
        length = len(data['data'])
#Capture image




#DEBUG IMPORT ONLY
if debug == True:
	im = Image.open(debugimg)
	im.save(captureimg)

#Process OCR

image = cv2.imread(captureimg)

clone = image.copy()

crop_img = clone[top:bottom, left:right]

cv2.imwrite(idblock, crop_img)

img = cv2.imread(idblock)

carddetails = pytesseract.image_to_string(img)

#print(carddetails) #Remove after debugging complete

os.remove(idblock)
os.remove(captureimg)


#Process the string to an array

#print(carddetails[0])

#Define if it is a recognised card type and determine the rarity
if cardtypes.find(carddetails[0]) >= 0:
	#print("It's a card")
	currtypetemp = carddetails[0]
if cardtypes.find(carddetails[0]) == -1:
	print("It's not a card")

loop = 0
check = ""


#Determine the set
while loop < length:
	check = data['data'][loop]['code'].upper()
	if carddetails.count(check) > 0:
		currsetcode = check
		currset = data['data'][loop]['name']
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


p = '[\d]+' #Regex to find the card number

if re.search(p, carddetails) is not None:
    for catch in re.finditer(p, carddetails):
        cardnumber = catch[0] # catch is a match object
	
else:
	print("No card number found")






#print(currtype)
#print(currset)
#print(cardnumber)


#Get card details
resp1 = requests.get('https://api.scryfall.com/cards/search?q=e:'+currsetcode+'+r:'+currtype+'+cn:'+cardnumber)
data1 = resp1.json()
print("")
print('ID: '+data1['data'][0]["id"])
print('Name: '+data1['data'][0]["name"])
print('Set: '+data1['data'][0]["set_name"])
print('Type: '+data1['data'][0]["type_line"])
print('Rarity: '+data1['data'][0]["rarity"])
print('Full art: '+str(data1['data'][0]["full_art"]))
print('Price: $'+str(data1['data'][0]["prices"]["usd"]))
print('Price foil: $'+str(data1['data'][0]["prices"]["usd_foil"]))