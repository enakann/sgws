import os
import re
import csv
import math
from settings import MODELS_PATH
from libs.sizer_msg import Msg

class SGDAO:
    def __init__(self,msg,inputData):
        self.msg=msg
        self.inputData=inputData
        self.msg.applianceModelFull=inputData['applianceModelFull']
        self.msg.storageNeededInTb=inputData['storageNeededInTb']
        self.msg.avgObjectSize=inputData['avgObjectSize']
        self.msg.smallObjectIngestRateObjps=inputData['smallObjectIngestRateObjps']
        self.msg.largeObjectIngestThrouhputInMbps=inputData['largeObjectIngestThrouhputInMbps']
        self.msg.hwLevelDataProtection=inputData['hwLevelDataProtection']
        self.msg.iLMRuleApplied=inputData['iLMRuleApplied']

        self.applianceFile=os.path.join(MODELS_PATH,"appliances_data.csv")
        self.rpSitesFile=os.path.join(MODELS_PATH,"rp_sites_data.csv")
        self.performanceFile=os.path.join(MODELS_PATH,"performance_data.csv")
        self.ecSitesFile=os.path.join(MODELS_PATH,"ec_site_ecscheme.csv")


    def loadData(self):
        self.getAppliance()
        self.get_rp_sites()
        self.get_performance_data(self.msg.applianceModel)

    def getAppliance(self):
        appliance_pattern=re.compile(r"(^SG\d+)\s\((\d\d)x(\d\d?)TB\s\w+\)") #SG6060 (58x10TB FIPS)
        ls = re.search(appliance_pattern, self.msg.applianceModelFull)
        self.msg.applianceModel,max_drive_no,self.msg.diskType=ls.groups()
        with open(self.applianceFile,'r') as fh:
            output=csv.DictReader(fh)
            for item in output:
                if item['model']== self.msg.applianceModel and item['disk_type']== self.msg.diskType and item['hwp']==self.msg.hwLevelDataProtection:
                    self.msg.usableStoragePerNode,self.msg.storageOverHeadHW,self.msg.rawStorage=item['usable_object_storage'],item['storage_overhead'],item['raw_storage']

    def get_rp_sites(self):
        selected_site=None
        site_pattern=re.compile(r'(\d)-site:\s(\d)\sreplicas')
        ls=re.search(site_pattern,self.msg.iLMRuleApplied)
        self.msg.numberOfSites,self.msg.numberOfReplicas=ls.groups()
        #import pdb;pdb.set_trace()
        with open(self.rpSitesFile,'r') as fh:
            output=csv.DictReader(fh)
            for item in output:
                if item['total_no_sites']==str(self.msg.numberOfSites) and item['total_no_replicas']==str(self.msg.numberOfReplicas):
                    self.msg.numberOfReplicasPerSite=item['no_replica_per_site']
                    print("success")


    def get_performance_data(self,model):
        """
        self.smallObjectPUTObjps=None
        self.smallObjectGETObjps=None
        self.largeObjectPUTMBps=None
        self.largeObjectGETMBps=None
        :param model:
        :return:
        """
        model=model[-4:]
        with open(self.performanceFile,'r') as fh:
            output=csv.DictReader(fh)
            for item in output:
                print(item)
                if item["model"]==model+'S':
                    #import pdb;pdb.set_trace()
                    self.msg.smallObjectGETObjps=item['get_per_sn']
                    self.msg.smallObjectPUTObjps=item['put_per_sn']
                if item["model"]==model+'L':
                    self.msg.largeObjectGETMBps=item['get_per_sn']
                    self.msg.largeObjectPUTMBps=item['put_per_sn']


class Sizer:
    def __init__(self,input):
        self.input=input
        self.msg = Msg()
        self.sgdao=SGDAO(self.msg,self.input)

    ####static calc
    def loadData(self):
        self.sgdao.loadData()

    def calcStorageRequiredAtEachSite(self):
        #import pdb;pdb.set_trace()
        self.msg.storageRequiredAtEachSite= self.msg.storageNeededInTb * self.msg.numberOfReplicasPerSite

    def calc_no_of_objects_to_be_stored(self):
        self.msg.numberOfObjectsToBeStored = self.msg.storageNeededInTb * math.pow(10,6) / self.msg.avgObjectSize
    #####


    def calculateNoOfApplianceAtEachSite(self):
        #import pdb;pdb.set_trace()
        self.msg.numberOfApplianceAtEachSite = round(self.msg.storageRequiredAtEachSite / self.msg.usableStoragePerNode)
        return self.msg.numberOfApplianceAtEachSite

    #### recalulate
    def calculateUsableStoragePerSite(self):
        self.msg.usableStoragePerSite = self.msg.numberOfApplianceAtEachSite * self.msg.usableStoragePerNode

    def calculateTotalAppliances(self):
        self.msg.totalAppliances = self.msg.numberOfSites * self.msg.numberOfApplianceAtEachSite

    def calculateTotalStorage(self):
        self.msg.totalStorage = self.msg.numberOfSites * self.msg.usableStoragePerSite

    def calculateTotalStorageOverRequired(self):
        self.msg.totalStorageOverRequired = self.msg.totalStorage - (self.msg.numberOfSites * self.msg.storageRequiredAtEachSite)

    def recalculate(self):
        self.calculateUsableStoragePerSite()
        self.calculateTotalAppliances()
        self.calculateTotalStorage()
        self.calculateTotalStorageOverRequired()
    ######


    def calc_no_of_appliance_at_each_site_for_object_sizing(self):
        if self.msg.numberOfObjectsToBeStored/self.msg.maxNoOfObjectPerSN > self.msg.numberOfApplianceAtEachSite:
            self.msg.numberOfApplianceAtEachSite=round(self.msg.numberOfObjectsToBeStored/self.msg.maxNoOfObjectPerSN)
        self.recalculate()

    def calc_no_of_appliance_at_each_site_for_perforamce(self):
        #import pdb;pdb.set_trace()
        if (self.msg.numberOfApplianceAtEachSite * self.msg.smallObjectPUTObjps) < self.msg.smallObjectIngestRateObjps:
            self.msg._additionalNodesToMeetIngestRate = round(self.msg.smallObjectIngestRateObjps/self.msg.smallObjectPUTObjps) - self.msg.numberOfApplianceAtEachSite
        if (self.msg.numberOfApplianceAtEachSite * self.msg.largeObjectPUTMBps) < self.msg.largeObjectIngestThrouhputInMbps:
            self.msg._additionalNodesToMeetIngestThrouhput = round(self.msg.largeObjectIngestThrouhputInMbps/self.msg.largeObjectPUTMBps) -self.msg.numberOfApplianceAtEachSite
        _max_of_additional_nodes=max(self.msg._additionalNodesToMeetIngestRate,self.msg._additionalNodesToMeetIngestThrouhput)
        if _max_of_additional_nodes:
            self.msg.numberOfApplianceAtEachSite += _max_of_additional_nodes
            self.recalculate()

    def cal_no_of_objects_supported(self):
        self.msg.numberOfObjectsSupported = self.msg.numberOfApplianceAtEachSite * self.msg.maxNoOfObjectPerSN

    def calc_storage_overhead(self):
        self.msg.storageOverHead = self.msg.numberOfReplicasPerSite * self.msg.numberOfSites * self.msg.storageOverHeadHW

    def calc_usable_capacity_without_data_protection(self):
        self.msg.totalStorageWithoutDataProtection = self.msg.totalStorage / (self.msg.numberOfReplicasPerSite * self.msg.numberOfSites)


    def get_storage_overhead(self):
        return {
                'softwareProtectionOverhead':self.msg.numberOfReplicasPerSite * self.msg.numberOfSites,
                'diskProtectionOverhead':self.msg.storageOverHeadHW,
                'totalOverHead':self.msg.storageOverHead
                }

    def get_sizing_result(self):
        return {
            "sizing":{
                "numberOfSites":self.msg.numberOfSites,
                "numberOfReplicas":self.msg.numberOfReplicas,
                "storageNodePerSite":self.msg.numberOfApplianceAtEachSite,
                "usableStoragePerSite":self.msg.usableStoragePerSite,
                "totalStorageNodes":self.msg.totalAppliances,
                "usableCapacity":self.msg.totalStorage,
                "usableCapacityWithoutDataProtection":self.msg.totalStorageWithoutDataProtection,
                "numberOfObjectsSupported":self.msg.numberOfObjectsSupported},
            "efficiency":{
                "softwareProtectionOverhead":self.msg.numberOfReplicasPerSite * self.msg.numberOfSites,
                "diskProtectionOverhead":self.msg.storageOverHeadHW,
                "totalOverHead":self.msg.storageOverHead
            }
        }

    def size(self):
        self.loadData()
        self.calcStorageRequiredAtEachSite()
        self.calculateNoOfApplianceAtEachSite()
        self.calc_no_of_objects_to_be_stored()
        self.calc_no_of_appliance_at_each_site_for_object_sizing()
        self.calc_no_of_appliance_at_each_site_for_perforamce()
        self.cal_no_of_objects_supported()
        self.recalculate()
        self.calc_storage_overhead()
        self.calc_usable_capacity_without_data_protection()
        return self.get_sizing_result()







if __name__ == '__main__':
    input={
        "applianceModelFull":"SG6060 (58x10TB FIPS)",
        "storageNeededInTb":5000,
        "avgObjectSize":4,
        "smallObjectIngestRateObjps":1800,
        "largeObjectIngestThrouhputInMbps":900,
        "hwLevelDataProtection":"DDP8",
        "iLMRuleApplied":"2-site: 2 replicas"
    }
    sizer=Sizer(input)
    sizer.size()
    print("\n\n\n")
    import pprint
    pprint.pprint(sizer.get_sizing_result())
    #import pdb;pdb.set_trace()






