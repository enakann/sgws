from etc import constants

class Msg:
    def __init__(self):
        self.applianceModelFull = None
        self._storageNeededInTb = None
        self._avgObjectSize = None
        self._smallObjectIngestRateObjps = None
        self._largeObjectIngestThrouhputInMbps = None
        self.hwLevelDataProtection = None
        self.iLMRuleApplied = None

        self.applianceModel = None
        self.diskType = None
        self._numberOfSites = 0
        self._numberOfReplicas = 0
        self._numberOfReplicasPerSite = 0
        self._storageRequiredAtEachSite = 0

        self._usableStoragePerNode = 0
        self._storageOverHead = 0
        self._storageOverHeadHW=0
        self._rawStorage = 0

        self._numberOfApplianceAtEachSite = 0
        self.usableStoragePerSite = 0
        self.totalAppliances = 0
        self.totalStorage = 0
        self.totalStorageWithoutDataProtection = 0
        self.totalStorageOverRequired = 0

        # No of objects
        self.numberOfObjectsToBeStored = 0
        self._additionalNodesToMeetIngestRate = 0
        self._additionalNodesToMeetIngestThrouhput = 0
        self.numberOfObjectsSupported = 0
        self.maxNoOfObjectPerSN = constants.MAX_OBJECTS_PER_SN

        # ObjectPerfData
        self._smallObjectPUTObjps = 0
        self._smallObjectGETObjps = 0
        self._largeObjectPUTMBps = 0
        self._largeObjectGETMBps = 0




        # Ec sepcific
        self.ec_sizing_type = None
        self.ec_scheme = None

    @property
    def storageNeededInTb(self):
        return self._storageNeededInTb

    @storageNeededInTb.setter
    def storageNeededInTb(self, val):
        self._storageNeededInTb = int(val)

    # avgObjectSize
    @property
    def avgObjectSize(self):
        return self._avgObjectSize

    @avgObjectSize.setter
    def avgObjectSize(self, val):
        self._avgObjectSize = int(val)

    #smallObjectIngestRateObjps
    @property
    def smallObjectIngestRateObjps(self):
        return self._smallObjectIngestRateObjps

    @smallObjectIngestRateObjps.setter
    def smallObjectIngestRateObjps(self, val):
        self._smallObjectIngestRateObjps = int(val)

    #largeObjectIngestThrouhputInMbps
    @property
    def largeObjectIngestThrouhputInMbps(self):
        return self._largeObjectIngestThrouhputInMbps

    @largeObjectIngestThrouhputInMbps.setter
    def largeObjectIngestThrouhputInMbps(self, val):
        self._largeObjectIngestThrouhputInMbps = int(val)




    # site
    @property
    def numberOfSites(self):
        return self._numberOfSites

    @numberOfSites.setter
    def numberOfSites(self, val):
        self._numberOfSites = int(val)

    # replica
    @property
    def numberOfReplicas(self):
        return self._numberOfReplicas

    @numberOfReplicas.setter
    def numberOfReplicas(self, val):
        self._numberOfReplicas = int(val)

    # NoOfreplicaPerSite
    # replica
    @property
    def numberOfReplicasPerSite(self):
        return self._numberOfReplicasPerSite

    @numberOfReplicasPerSite.setter
    def numberOfReplicasPerSite(self, val):
        self._numberOfReplicasPerSite = int(val)

    #storageRequiredAtEachSite
    @property
    def storageRequiredAtEachSite(self):
        return self._storageRequiredAtEachSite

    @storageRequiredAtEachSite.setter
    def storageRequiredAtEachSite(self, val):
        self._storageRequiredAtEachSite = float(val)

    #self._usableStoragePerNode
    @property
    def usableStoragePerNode(self):
        return self._usableStoragePerNode

    @usableStoragePerNode.setter
    def usableStoragePerNode(self, val):
        self._usableStoragePerNode = float(val)

    # self._usableStoragePerNode

    @property
    def numberOfApplianceAtEachSite(self):
        return self._numberOfApplianceAtEachSite

    @numberOfApplianceAtEachSite.setter
    def numberOfApplianceAtEachSite(self, val):
        self._numberOfApplianceAtEachSite = int(val)

    #self._smallObjectPUTObjps

    @property
    def smallObjectPUTObjps(self):
        return self._smallObjectPUTObjps

    @smallObjectPUTObjps.setter
    def smallObjectPUTObjps(self, val):
        self._smallObjectPUTObjps = int(val)

    #self._largeObjectPUTMBps

    @property
    def largeObjectPUTMBps(self):
        return self._largeObjectPUTMBps

    @largeObjectPUTMBps.setter
    def largeObjectPUTMBps(self, val):
        self._largeObjectPUTMBps = int(val)

    #storageOverhead

    @property
    def storageOverHeadHW(self):
        return self._storageOverHeadHW

    @storageOverHeadHW.setter
    def storageOverHeadHW(self, val):
        self._storageOverHeadHW = float(val)

    @property
    def storageOverHead(self):
        return self._storageOverHead

    @storageOverHead.setter
    def storageOverHead(self, val):
        self._storageOverHead = float(val)

    #rawStorage
    @property
    def rawStorage(self):
        return self._rawStorage

    @rawStorage.setter
    def rawStorage(self, val):
        self._rawStorage = int(val)

    def __str__(self):
        return str(self.__dict__)
