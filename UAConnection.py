
import configparser
import os
import sys
import webbrowser
import requests
import json
import time


UA = 'UA'
NONE = 'None'


class UAConnection:
    def __init__(self,inifilename):
        self.__config = configparser.ConfigParser()
        self.__config.read(inifilename)
               
        self.CLIENT_ID = self.__config[UA]['client_id']
        self.CLIENT_SECRET =  self.__config[UA]['client_secret']
        self.USER_ID = self.__config[UA]['user_id']
        self.AUTHORIZATION_TOKEN = self.__config[UA]['authorization_token']
        self.ACCESS_TOKEN = self.__config[UA]['access_token']
        
    def __str__(self, ):
        return 'id: {}, secret: {}, user: {}, authorization: {}, access: {}'.format( self.CLIENT_ID,self.CLIENT_SECRET, self.USER_ID,self.AUTHORIZATION_TOKEN,self.ACCESS_TOKEN)
        
    
    def get_workouts(self):
        workouts_url = 'https://oauth2-api.mapmyapi.com/v7.0/workout/?user=%s&order_by=-start_datetime' % self.USER_ID
        response = requests.get(url=workouts_url, verify=False,
                            headers={'api-key': self.CLIENT_ID, 'authorization': 'Bearer %s' % self.ACCESS_TOKEN})
    
        data = response.json()
        
        
        return data
    
    def get_one_workout(self):
        pass
    
    
    def get_user(self):
        user_url = 'https://oauth2-api.mapmyapi.com/v7.1/user/self/'
        response = requests.get(url=user_url, verify=False,
                            headers={'api-key': self.CLIENT_ID, 'authorization': 'Bearer %s' % self.ACCESS_TOKEN})
        data = response.json()
    
        return data
    
class UAWorkout:
    def __init__(self,d):
        self.date = d['start_datetime']
        self.distance_total = d['aggregates']['distance_total']/1609.0
        self.elapsed_time_total = d['aggregates']['elapsed_time_total']
        try:
            self.metabolic_energy_total = d['aggregates']['metabolic_energy_total']/1000.0
        except:
            self.metabolic_energy_total = 0.0
            
    def __str__(self):
        elapsed_str = time.strftime('%H:%M:%S',time.gmtime(self.elapsed_time_total))
        return 'Date: {}, Distance: {}, Time: {}, Calories burned: {}'.format(self.date,self.distance_total,elapsed_str,self.metabolic_energy_total)
    
class UAUser:
    def __init__(self,d):
        self.display_name = d['display_name']
        
    def __str__(self):
        return self.display_name
        
if __name__ == '__main__':
    print('UAConnection Test')
    
    ua = UAConnection('providers.ini')
    
    
    user = ua.get_user()
    #print (json.dumps(user,sort_keys=True,indent=2))
    
    workouts = ua.get_workouts()['_embedded']['workouts']
    print('workouts length=',len(workouts))
    
    for i in range(len(workouts)):
        w = UAWorkout(workouts[i])
        print(w)
    
    print(ua)
    exit(0)