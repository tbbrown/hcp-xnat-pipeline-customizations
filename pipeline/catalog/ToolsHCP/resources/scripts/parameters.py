'''
Created on 2013-12-13

@author: Mohana Ramaratnam (mohanakannan9@gmail.com)
'''

import sys
import os
import xml.etree.ElementTree as ET

#===============================================================================
# CLASSES
#===============================================================================


#===============================================================================
# XML Handling
#===============================================================================
class XNATPipelineParameters(object):
    """HCP Param XML Class"""
    def __init__(self):
        super(XNATPipelineParameters,self).__init__()        
        self.ParameterStrXML = '<pip:Parameters xmlns:pip="http://nrg.wustl.edu/pipeline"></pip:Parameters>'
        self.ParametersRootElement = ET.fromstring(self.ParameterStrXML)
        ET.register_namespace('pip', 'http://nrg.wustl.edu/pipeline')

    def addUniqueParameter(self, parameterName, parameterUniqueValue):
        parameterElement=ET.SubElement(self.ParametersRootElement,'pip:parameter')
        childStr='<pip:name xmlns:pip="http://nrg.wustl.edu/pipeline">%s</pip:name>' % (parameterName)
        parameterElement.append((ET.fromstring(childStr)))
        childStr='<pip:values xmlns:pip="http://nrg.wustl.edu/pipeline"><pip:unique xmlns:pip="http://nrg.wustl.edu/pipeline">%s</pip:unique></pip:values>' % (parameterUniqueValue)
        parameterElement.append((ET.fromstring(childStr)))
        
    
    def addListParameters(self, parameterName, parameterValueList):     
        parameterElement=ET.SubElement(self.ParametersRootElement,'pip:parameter')
        childStr='<pip:name xmlns:pip="http://nrg.wustl.edu/pipeline">%s</pip:name>' % (parameterName)
        parameterElement.append((ET.fromstring(childStr)))
        valuesStr='<pip:values xmlns:pip="http://nrg.wustl.edu/pipeline">'
        for i in xrange(0, len(parameterValueList)):
            valuesStr+='<pip:list xmlns:pip="http://nrg.wustl.edu/pipeline">%s</pip:list>' % (parameterValueList[i])
        valuesStr+='</pip:values>'
        parameterElement.append((ET.fromstring(valuesStr)))
    
    def saveParameters(self,pathToParamsFile):
        self.indent(self.ParametersRootElement)
        basedir = os.path.dirname(pathToParamsFile)
        if not os.path.exists(basedir):
            os.makedirs(basedir)
        ET.ElementTree(self.ParametersRootElement).write(pathToParamsFile)
#        parameterDataStr=ET.tostring(self.ParametersRootElement)
#        with open(pathToParamsFile, 'wb') as outputFileObj:
#            outputFileObj.write(parameterDataStr)
        print 'Parameter File saved to %s' % (pathToParamsFile)   


    def indent(self,elem, level=0):
    #copy and paste from http://effbot.org/zone/element-lib.htm#prettyprint
    #it basically walks your tree and adds spaces and newlines so the tree is
    #printed in a nice way

      i = "\n" + level*"  "
      if len(elem):
        if not elem.text or not elem.text.strip():
          elem.text = i + "  "
        if not elem.tail or not elem.tail.strip():
          elem.tail = i
        for elem in elem:
            self.indent(elem, level+1)
        if not elem.tail or not elem.tail.strip():
          elem.tail = i
      else:
        if level and (not elem.tail or not elem.tail.strip()):
          elem.tail = i

#===============================================================================
# END CLASS DEFs
#===============================================================================
    
if __name__ == "__main__":
    XNATPipelineParameters()
