#curl -H "X-Api-Key: f4b47fba-aea0-44a7-8881-8c6faeb5775b" "https://us.api.insight.rapid7.com/opendata/studies/sonar.ssl/"


#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 27 01:04:19 2018

@author: diogo
"""
import requests
import json
#import re
headers = {
    'X-Api-Key': 'f4b47fba-aea0-44a7-8881-8c6faeb5775b'
}
url = 'https://us.api.insight.rapid7.com/opendata/studies/'

durl = 'https://us.api.insight.rapid7.com/opendata/studies/sonar.ssl/'
r1 = requests.get(durl, headers=headers)
r2 = json.loads(r1.text)["sonarfile_set"]
print(type(r2))

arq = open('links.txt', "a")
for f in r2:
    arq.write(f+'\n')

arq.close()

#arq = open('links.txt', "r")
#arq = open('links_names.txt', "r")
#arq = open('links_certs.txt', "r")


#regex1 = ".*_names.gz$"
#regex2 = ".*_certs.gz$"
    
#for link in arq:
    #durl = 'https://us.api.insight.rapid7.com/opendata/studies/sonar.ssl/'
    #r1 = requests.get(durl, headers=headers)
    #print(type(r1))
    #url1 = './Names/'+str(link.strip().split("/")[len(link.strip().split("/"))-1])
    #url2 = './Certs/'+str(link.strip().split("/")[len(link.strip().split("/"))-1])
    #with open(url1,'wb') as f:
    #with open(url2,'wb') as f:
        #f.write(r2.content)
        #f.close()
