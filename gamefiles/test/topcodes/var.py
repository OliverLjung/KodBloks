class Config:
    stopThreads = False
    
    def stopThreadsSetter(status):
        Config.stopThreads = status

    @property
    def stopThreads():
        return Config.stopThreads
