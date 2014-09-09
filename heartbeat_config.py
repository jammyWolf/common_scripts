# coding=utf8
#!/usr/bin/python

import ConfigParser

class ConfigHandler(object):

    def __init__(self):
        self.configFile = "xx.conf"
        self.cf =  ConfigParser.ConfigParser()
        self.cf.read(self.configFile)
        self.sections = self._getSections()

    def _getSections(self):
        """ means the name of each heartbeat."""

        sections = self.cf.sections()
        return sections

    def _getOptions(self, sectionName):    
        """ options means the attributes of certain SECTION."""

        if sectionName in self.sections:
            attri_list = self.cf.options(sectionName)
            return attri_list
        else:
            return None

    def getConfig(self, sectionName):
        if sectionName in self.sections:
            optionList = self._getOptions(sectionName)
            itemDict = {}
            for option_key in optionList:
                itemDict.update({option_key.upper():self.cf.get(sectionName, option_key)})
            return itemDict

if __name__ == "__main__":
    cf = ConfigHandler()
    print cf.getConfig(sectionName = "xx")

