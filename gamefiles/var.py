class Config:
    stopThreads = False
    
    def stopThreads_setter(status):
        Config.stopThreads = status

    @property
    def stopThreads():
        return Config.stopThreads
