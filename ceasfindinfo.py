
from retrieve_query.queryceas import Ceastransrecords, Town_to_district_lookup
import os
import yaml

def main():

    configfname='D:\\OneDrive\\Annamalai\\380_Project\\data_csv\\config.yml'
    
    #offset=351263

    #offset=720000

    #offset=0
    with open(configfname, 'r') as file:
       configinfo = yaml.load(file, Loader=yaml.FullLoader)
    districtlut=Town_to_district_lookup(configinfo['csvtowntodist'])
    #print(districtlut.find_district_for('toa payoh'))
    
    transcurrent=Ceastransrecords(configinfo['url_ceas'],configinfo['offset'],districtlut)
 
    transcurrent.bestagentforalldistricts(districtlut.dict_towntodist,configinfo['period_inmth'],configinfo['agentbydistcsvfname'])

    #districtnum=12
    #transcurrent.findbestagentbydistrict(districtnum,period_inmth)



if __name__ == '__main__':
	main()
