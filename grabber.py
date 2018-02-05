import dryscrape
from bs4 import BeautifulSoup
import re
import sys
import json
import time

if  sys.argv[1] == "?" or sys.argv[1] == "" :			# Show scheme if no parameters are given
	print("python grabber.py URL STARTEPISODE ENDEPISODE HOST")
	sys.exit(0)
dryscrape.start_xvfb()									# Start dryscrape session
session = dryscrape.Session()
start =  int(sys.argv[2])
stop = int(sys.argv[3])+ 1


for i in range(start, stop):							# Create URL for each Episode
    zahl = str(i)
    my_url = sys.argv[1] + "/" + zahl
    session.visit(my_url)								# Visit the URL and make it into a Soup
    response = session.body()
    soup = BeautifulSoup(response)
    mirstr = str(soup.find_all('script'))				# Find the part where the download URL is located 
    mirstr = mirstr.split("var args = ",1)[1]
    mirstr = mirstr.split("] }",)[0]
    mirstr = mirstr + "] }"
    mirstr = mirstr.replace("anime","\"anime\"")
    mirstr = mirstr.replace("mirrors","\"mirrors\"")
    mirstr = mirstr.replace("auto_update","\"auto_update\"")
    mirdic = json.loads(mirstr)							# Decode the JSON string into somethin more readable
    embed_id = ""
    hostavail = ""
    prefhost = sys.argv[4]
    title = mirdic['anime']['info']['title']
    downurl = "Fehler"
    for data in mirdic['mirrors']:
        hostname = data['host']['name']
        qual = data['quality']
        if prefhost == "google" or prefhost == "Google":
            if  hostname == "Drive.g" and qual == 1080:
                embed_id = data['embed_id']
                hostavail = "EP " + str(i) + ": 1080p Google available"
                downurl = "https://docs.google.com/file/d/" + str(embed_id)
                break
            if  hostname == "Drive.g" and qual == 720:
                embed_id = data['embed_id']
                hostavail = "EP " + str(i) + ": 720p Google available"
                downurl = "https://docs.google.com/file/d/" + str(embed_id)
                break
        elif prefhost == "vid" or "Vidstreaming":
            if  hostname == "Vidstreaming" and qual == 1080:
                embed_id = data['embed_id']
                hostavail = "EP " + str(i) + ": 1080p Vidstreaming available"
                downurl = "https://vidstreaming.io/download?id=" + str(embed_id)
                break
            if  hostname == "Vidstreaming" and qual == 720:
                embed_id = data['embed_id']
                hostavail = "EP " + str(i) + ": 720p Vidstreaming available"
                downurl = "https://vidstreaming.io/download?id=" + str(embed_id)
                break
        if prefhost == "mp4" or prefhost == "Google":
            if  hostname == "MP4Upload" and qual == 1080:
                embed_id = data['embed_id']
                hostavail = "EP " + str(i) + ": 1080p MP4Upload available"
                downurl = "https://mp4upload.com/" + str(embed_id)
                break
            if  hostname == "MP4Upload" and qual == 720:
                embed_id = data['embed_id']
                hostavail = "EP " + str(i) + ": 720p MP4Upload available"
                downurl = "https://mp4upload.com/" + str(embed_id)
                break
    str(title)
    title = title.replace(" ", "")
    print title
    title = title+"_" + str(start) +"-"+ str(stop) + ".txt"
    print(i)
    text_file = open(title, "a")						# Write all the download links into a .txt file
    text_file.write(hostavail + "\n")
    text_file.write(downurl + "\n")
    text_file.close()
