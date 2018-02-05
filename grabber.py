import dryscrape
from bs4 import BeautifulSoup
import re
import sys
import json
import time
if  sys.argv[1] == "?":
    print("python grabber.py URL STARTEPISODE ENDEPISODE HOST")
    sys.exit(0)
dryscrape.start_xvfb()
session = dryscrape.Session()
start =  int(sys.argv[2])
stop = int(sys.argv[3])+ 1


for i in range(start, stop):
    zahl = str(i)
    my_url = sys.argv[1] + "/" + zahl
    #print(my_url)
    session.visit(my_url)
    response = session.body()
    soup = BeautifulSoup(response)
    #print(soup)
    mirstr = str(soup.find_all('script'))
    mirstr = mirstr.split("var args = ",1)[1]
    mirstr = mirstr.split("] }",)[0]
    mirstr = mirstr + "] }"
    #print(str)
    mirstr = mirstr.replace("anime","\"anime\"")
    mirstr = mirstr.replace("mirrors","\"mirrors\"")
    mirstr = mirstr.replace("auto_update","\"auto_update\"")
    #print(mirstr)
    mirdic = json.loads(mirstr)
    #print(type(mirdic))
    embed_id = ""
    hostavail = ""
    prefhost = sys.argv[4]
    #print(prefhost)
    title = mirdic['anime']['info']['title']
    downurl = "Fehler"
    # for data in mirdic['anime']:
    #     #title = data['info']['title']
    #     print(data['title'])
    for data in mirdic['mirrors']:
        hostname = data['host']['name']
        #print(hostname)
        qual = data['quality']
        #print(qual)
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
    # if  downurl == "Fehler":
    #     for data in mirdic['mirrors']:
    #         hostname = data['host']['name']
    #         print(hostname)
    #         qual = data['quality']
    #         print(qual)
    #         if prefhost == "mp4":
    #             if  hostname == "MP4Upload" and qual == "720":
    #                 embed_id = data['embed_id']
    #                 print(embed_id)
    #                 hostavail = "EP " + str(i) + ": 720p MP4Upload available"
    #                 downurl = "https://mp4upload.com/" + str(embed_id)
    # print(hostavail)
    # print(downurl)
    #print (mirdic['mirrors']['embed_id'])
    #print(len(mirdic))
        # for i in range(0, len(my_string)):
        # if "\"host_id\":12" in my_string[i] and "\"quality\":1080" in my_string[i +2]:
        # k = i+1
        # break
        # print(my_string[k])
    text_file = open(title, "a")
    text_file.write(hostavail + "\n")
    text_file.write(downurl + "\n")
    text_file.close()
