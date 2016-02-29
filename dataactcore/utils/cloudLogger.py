import logging
import logstash
import os
import inspect

class CloudLogger(object):
    """ Singleton Logging object """
    LOGGER = None

    @staticmethod
    def getValueFromConfig(value):
        """ Retrieve specified value from config file """
        path = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
        loggingConfig = open(path+"/logging.json","r").read()
        bucketDict = json.loads(loggingConfig)
        return bucketDict[value]

    @staticmethod
    def getLogger():
        """gets current logger"""
        if(CloudLogger.LOGGER == None):
            CloudLogger.LOGGER = logging.getLogger('python-logstash-logger')
            CloudLogger.LOGGER.setLevel(logging.INFO)
            CloudLogger.LOGGER.addHandler(logstash.LogstashHandler(CloudLogger.getValueFromConfig("host"), CloudLogger.getValueFromConfig("port"), version=1))
        return CloudLogger.LOGGER
