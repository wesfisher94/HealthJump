import requests
import requests_cache
import pandas as pd

#Starts a cache to pull from if same request is made within 5 minutes
requests_cache.install_cache('demo', backend='sqlite', expire_after=300)

#Function pulls down Bearer Token for authentication
def auth_token(auth_url,auth_payload):
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    response = requests.request("POST", auth_url, headers=headers, data=auth_payload)
    return response.json()

#Enter URL, Email and Password of desired destination to receive token
token = auth_token("https://api.healthjump.com/authenticate",'email=sandbox%40healthjump.com&password=R%2D%Sx%3FqP%%2BRN69CS')

#Function pulls down desired data of URL entered. Will tell you if request was retrieved from cache.
def get_data(url):
    payload={}
    files={}
    headers = {"Authorization": "Bearer {}".format(token['token']), 'Version':'3.0', 'secretkey':'yemj6bz8sskxi7wl4r2zk0ao77b2wdpvrceyoe6g'}
    response = requests.request("GET", url, headers=headers, data=payload, files=files)
    if response.from_cache:
        print('PLEASE NOTE: This Request was retrieved from cache')
    return response.json()

#Enter URL and parameters below for desired output. 
#In this case we are pulling back results that are less than Patient_D. This pulls back all Patient A,B,and C's.
data_response=get_data("https://api.healthjump.com/hjdw/SBOX02/demographic?first_name=lt~Patient_D")

#Function creates pandas dataframe from data_response and converts to a flat csv file.
def jsontocsv(filename):
    df=pd.DataFrame(data_response['data'])
    df.to_csv(filename, encoding='utf-8', index=False)

#Enter desired filename for flat csv output
jsontocsv('Demo_FirstName_A_B_C.csv')

input('Data has been pulled down and inserted into output file. Press enter to exit.')

#Wes Fisher
