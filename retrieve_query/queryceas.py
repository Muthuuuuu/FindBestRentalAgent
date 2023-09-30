
import requests
from bs4 import BeautifulSoup
import numpy as np

import re
import json
import numpy as np
import datetime
import pandas as pd
import csv
from pathlib import Path

RECLIMIT=15000

def listprevmth(period_inmth):                         
    prevmth_list=[]
    for prevmth in range(period_inmth):
        previous_date = datetime.datetime.today() - datetime.timedelta(days=prevmth*30)
        prevmth_list.append(previous_date.strftime("%b-%Y").upper())  

    return prevmth_list

class Town_to_district_lookup:
    def __init__(self,csvfname):

        #df=pd.read_csv(csvfname, header=None, index_col=0, squeeze = True) 
        df=pd.read_csv(csvfname, header=None, index_col=0)
        self.dict_towntodist=df.to_dict()[1]

    def find_district_for(self, keystr):    
        #print(self.dict_towntodist)
        for k, v in self.dict_towntodist.items():
            if keystr.upper() in k.upper():
               return v
        
class Ceastransrecords:
   def __init__(self,url,offset,dicttowntodist):
       self.url=url
       self.findallrecord(offset,dicttowntodist)
       return
       
   def findallrecord(self,offset,lut):
   	   
       #Only to find the total number of records in dbase
       page_info=requests.get(self.url)
       if page_info.status_code==200:
          soup_page=BeautifulSoup(page_info.content,"html.parser")
          scripttags=soup_page.find_all("records")
          #print(soup_page.prettify())

          y=json.loads(str(soup_page)) 
          self.lastrecordidx=int(y['result']['total'])
       
       #To pull all records with valid district number
       #self.numtopull=RECLIMIT
       #offset=self.lastrecordidx-self.numtopull
       self.numtopull=self.lastrecordidx-offset
       urlsearch=self.url+'&offset='+str(offset)+'&limit='+str(self.numtopull)
       page_info=requests.get(urlsearch)
       if page_info.status_code==200:
       	  soup_page=BeautifulSoup(page_info.content,"html.parser")
       	  #print(soup_page.prettify())

          self.records_all=json.loads(str(soup_page)) 
          self.len_records=len(self.records_all['result']['records']) 
          print(self.len_records)

          for countrec in range(self.len_records):
              if (self.records_all['result']['records'][countrec]['district']=='-'):
                 townstr=self.records_all['result']['records'][countrec]['town']
                 self.records_all['result']['records'][countrec]['district']=lut.find_district_for(townstr)
          #print(self.records_all)  

       return  

  
   def findallrecordsbydistrict(self,districtnum,offset):
       urlbydistrictnum=self.url+'&offset='+str(offset)+'&limit='+str(self.numtopull)+'&q='+str(districtnum)
       #print(urlbydistrictnum)
       page_info=requests.get(urlbydistrictnum)
       if page_info.status_code==200:
       	  soup_page=BeautifulSoup(page_info.content,"html.parser")
       	  scripttags=soup_page.find_all("records")
          #print(soup_page.prettify())

          recordsbydistrict=json.loads(str(soup_page))
          #print(len(recordsbydistrict))
       
       return recordsbydistrict 

   def bestagentforalldistricts(self, lutdic,period_inmth,agentbydistcsvfname):
       bestagentbydistrict=[]
       #print(type(lutdic))
       for k, v in lutdic.items():
           #print(f"District number {v}")
           bestagentinthisdistrict=self.findbestagentbydistrict(int(v),period_inmth)
           #print(f"{v} {bestagentinthisdistrict}")
           bestagentbydistrict.append(bestagentinthisdistrict)
       #print(bestagentbydistrict)
       with Path(agentbydistcsvfname).open('w',newline='') as f:
           csv_writer = csv.writer(f)
           csv_writer.writerows(bestagentbydistrict)
       return

   def findbestagentbydistrict(self,districtnum,period_inmth):
   
       #Finding mth/yr period to check best agent
       checkperiodlist=listprevmth(period_inmth)
       #print(checkperiodlist)


       agentlist=[]
       strdistrictnum=str(districtnum).zfill(2)
       for countrec in range(self.len_records):

           #print(self.records_all['result']['records'][countrec]['transaction_date'])
           #print(checkperiodlist)

           if (self.records_all['result']['records'][countrec]['district']==strdistrictnum)&\
              (self.records_all['result']['records'][countrec]['transaction_date'] in checkperiodlist)&\
              ('RENTAL' in self.records_all['result']['records'][countrec]['transaction_type']): 
             
              agentlist.append(self.records_all['result']['records'][countrec]['salesperson_name'])
       #print(agentlist)

       #print(len(agentlist))
       uniqueagentlist = list(set(agentlist))
       #print(len(uniqueagentlist))

       agenttrans_dict = {uniqueagentlist[i]: 0 for i in range(len(uniqueagentlist))}
       
       for i in range(len(uniqueagentlist)):
           if uniqueagentlist[i] not in agentlist:
              pass
           else :
              count = len([entry for entry in agentlist if entry==uniqueagentlist[i]])
              agenttrans_dict[uniqueagentlist[i]]=count


       maxtrans=0
       bestagent=[]
       if len(agenttrans_dict.values())>0:

          bestagent = [k for k, v in agenttrans_dict.items() if v == max(agenttrans_dict.values())]
          #print(max(agenttrans_dict.values()))
          maxtrans = max(agenttrans_dict.values())
       print(f"Best Agent in district {strdistrictnum} : {bestagent} transacted {maxtrans}")


       return bestagent   


   def finduniquedistrict(self): 
   	   district=np.zeros(self.len_records)
   	   for countrec in range(self.len_records):
   	   	   print(self.records_all[countrec]['_id'])
   	   	   district[countrec]=int(self.records_all[countrec]['_id'])
   	   return(unique(district))
       
       
       

