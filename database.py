##PyHSS Database Library
##Features classes for different DB backends normalised to each return the same data
##Data is always provided by the function as a Dictionary of the Subscriber's data
import yaml
import logging
import threading
import os
import sys
sys.path.append(os.path.realpath('lib'))
import S6a_crypt

with open("config.yaml", 'r') as stream:
    yaml_config = (yaml.safe_load(stream))

import logtool

logtool.setup_logger('DBLogger', yaml_config['logging']['logfiles']['database_logging_file'], level=yaml_config['logging']['level'])
DBLogger = logging.getLogger('DBLogger')


DBLogger.info("DB Log Initialised.")

##Data Output Format
###Get Subscriber Info
#Outputs a dictionary with the format:
#subscriber_details = {'K': '465B5CE8B199B49FAA5F0A2EE238A6BC', 'OPc': 'E8ED289DEBA952E4283B54E88E6183CA', 'AMF': '8000', 'RAND': '', 'SQN': 22, \
# 'APN_list': 'internet', 'pdn': [{'apn': 'internet', '_id': ObjectId('5fe2815ce601d905f8c597b3'), 'pcc_rule': [], 'qos': {'qci': 9, 'arp': {'priority_level': 8, 'pre_emption_vulnerability': 1, 'pre_emption_capability': 1}}, 'type': 2}]}


class MySQL:
    import mysql.connector
    def __init__(self):
        DBLogger.info("Configured to use MySQL server: " + str(yaml_config['database']['mysql']['server']))
        self.server = yaml_config['database']['mysql']
        self.mydb = self.mysql.connector.connect(
          host=self.server['server'],
          user=self.server['username'],
          password=self.server['password'],
          database=self.server['database'],auth_plugin='mysql_native_password'
        )
        self.mydb.autocommit = True
        self.mydb.SQL_QUERYTIMEOUT = 3
        cursor = self.mydb.cursor(dictionary=True)
        self.cursor = cursor
        
    def GetSubscriberInfo(self, imsi):
        DBLogger.debug("Getting subscriber info from MySQL for IMSI " + str(imsi))
        self.cursor.execute("select * from subscribers left join subscriber_apns on subscribers.imsi = subscriber_apns.imsi left join apns on subscriber_apns.apn_id = apns.apn_id where subscribers.imsi = " + str(imsi))
        subscriber_details = self.cursor.fetchall()
        return subscriber_details

    def UpdateSubscriber(self, imsi, sqn, rand, *args, **kwargs):
        DBLogger.debug("Updating SQN for imsi " + str(imsi) + " to " + str(sqn))
        query = 'update subscribers set sqn = ' + str(sqn) + ' where imsi = ' + str(imsi)
        DBLogger.debug(query)
        self.cursor.execute(query)
        
            
#Load DB functions based on Config
for db_option in yaml_config['database']:
    DBLogger.debug("Selected DB backend " + str(db_option))
    break


if db_option == "mysql":
    DB = MySQL()
else:
    DBLogger.fatal("Failed to find any compatible database backends. Please ensure the database type you have in the config.yaml file corresponds to a database type defined in database.py Exiting.")
    sys.exit()

def GetSubscriberInfo(imsi):
    return DB.GetSubscriberInfo(imsi)

def UpdateSubscriber(imsi, sqn, rand, *args, **kwargs):
    if 'origin_host' in kwargs:
        DBLogger.debug("UpdateSubscriber called with origin_host present")
        origin_host = kwargs.get('origin_host', None)
        DBLogger.debug("Origin Host: " + str(origin_host))
        return DB.UpdateSubscriber(imsi, sqn, rand, origin_host=str(origin_host))
    else:
        return DB.UpdateSubscriber(imsi, sqn, rand)

def GetSubscriberLocation(imsi, input):
    #Input can be either MSISDN or IMSI
    return DB.GetSubscriberLocation(imsi='input')

#Unit test if file called directly (instead of imported)
if __name__ == "__main__":
    DB.GetSubscriberInfo('208310001859912')
    DB.UpdateSubscriber('208310001859912', 998, '', origin_host='mme01.epc.mnc001.mcc01.3gppnetwork.org')
    DB.GetSubscriberLocation(imsi='208310001859912')
