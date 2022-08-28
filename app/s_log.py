class LogProviderInterface():
    def info(self, tag, msg):
        pass
    def debug(self, tag, msg, state=None):
        pass
    def error(self, tag, msg):
        pass
    def fatal(self, tag, msg):
        pass

class LogService():
    def __init__(self, logProvider: LogProviderInterface):
        self.logProvider = logProvider

    def info(self, tag, msg):
        self.logProvider.info(tag, msg)
    def debug(self, tag, msg, state=None):
        self.logProvider.debug(tag, msg, state)
    def error(self, tag, msg):
        self.logProvider.error(tag, msg)                
    def fatal(self, tag, msg):
        self.logProvider.fatal(tag, msg)        