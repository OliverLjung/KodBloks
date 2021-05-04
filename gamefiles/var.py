class Config:
    """
    Class: Config, made to carry data between many intertwined modules/files.
    """
    stopThreads = False
    
    def stopThreads_setter(status):
        """
        Function: args status (Bool), sets stopThreads to status.
        """
        Config.stopThreads = status

    @property
    def stopThreads():
        """
        Function: stopThreads getter.
        """
        return Config.stopThreads
