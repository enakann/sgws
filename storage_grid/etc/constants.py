METADATA_RESERVATION = 3 #TB
STORAGE_NODE_COUNT_MIN = 3
STORAGE_NODE_COUNT_MAX=195

MAX_LUNS_PER_SN=16
DATABASE_SIZE=10,00,00,00,00,000 # 1TB
SYSTEM_METADATA_PER_OBJECT=1,400 # (BYTE) 3 REPLICA
USER_METADATA_PER_OBJECT= 200 # (BYTE) Change this 400 (B) for use with the NAS Bridge.  If the client application uses custom metadata, specify the value here.  Maximum value is 2000 B.
TOTAL_METADATA_PER_OBJECT=2000 #(BYTE)
FILE_TO_OBJECT_RATION = 1  # Default is 1. Change this to 2 for use with the NAS Bridge.
MAX_OBJECTS_PER_SN=50_00_00_000  #Maximum number of objects per database is 500M.


SN_APPLIANCE_TYPE=['SG5712','SG5760','SG6060']
DRIVE_TYPE=[4,8,10,12]
HW_PROTECTION_TYPE=['DDP8','DDP16','RAID6']

