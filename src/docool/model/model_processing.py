import os

import xml.etree.ElementTree as ET

class ArchiFileProcessor:
    ns = {'xsi': "http://www.w3.org/2001/XMLSchema-instance",
        'archimate': 'http://www.archimatetool.com/archimate'}

    def __init__(self, projectdir):
        modelname = projectdir.split('\\')[-1]
        modelpath = os.path.join(projectdir, 'src', 'model', modelname+'.archimate')
        self.tree = ET.parse(modelpath)
    
    def get_element(self, eid):
        return self.tree.getroot().find(".//element[@id='{0}']".format(eid), self.ns)

    def get_folder(self, foldername):
        return self.tree.getroot().find(".//folder[@name='{0}']".format(foldername), self.ns)

    def get_requirements(self, foldername):
        # get folder by name
        reqfolder = self.get_folder(foldername)
        # get all requirements by type converted to Requirement class
        requirements = []
        relationshipsfolder = self.get_folder('Relations')
        for r in reqfolder.findall("element[@xsi:type='archimate:Requirement']", self.ns):
            req = Requirement(r)
            requirements.append(req)
            # find realizations
            cond = ".//element[@xsi:type='archimate:RealizationRelationship'][@target='{0}']".format(req.eid)
            for realizationRelationship in relationshipsfolder.findall(cond, self.ns):
                e = self.get_element(realizationRelationship.attrib['source'])
                req.add_requirement(realizationRelationship, e)
        return requirements

    def get_folders(self, foldername):
        # get folder by name
        parentfolder = self.get_folder(foldername)
        # get all requirements by type converted to Requirement class
        return [Element.elementname(f) for f in parentfolder.findall("folder", self.ns)]

    @staticmethod
    def isproduct(elementtype):
        return elementtype == 'archimate:Product'
  

class Element:
    """ Element has a name and description """

    def __init__(self, element):
        # set ID
        self.eid = Element.elementid(element)
        # set name
        self.name = Element.elementname(element)
        # set desc
        self.desc = Element.elementdesc(element)
        # set type
        self.type = Element.elementtype(element)

    @staticmethod
    def elementid(element):
        return element.attrib['id']

    @staticmethod
    def elementname(element):
        return element.attrib['name']
        
    @staticmethod
    def elementtype(element):
        keyname = '{' + ArchiFileProcessor.ns['xsi'] + '}type'
        return element.attrib[keyname]
        
    @staticmethod
    def elementdesc(element):
        eDoc = element.find('documentation')
        if (eDoc == None):
            return '--'
        else:
            return eDoc.text.replace('\n', '').replace('<ul>\r', '<ul>').replace('</li>\r', '</li>').replace('\r', '<BR/>').replace(' ', '• ')


class Requirement(Element):
    """ Requirement is Element with description how it is realized. 
        It is list of pairs (Element, explanation), where Element is realizing element 
        and explanation is description how element realize requirement"""

    def __init__(self, element):
        super().__init__(element)
        self.realizations = []

    def add_requirement(self, realization_relationship, realization_element):
        e = Element(realization_element)
        if e.type == 'archimate:Product':
            self.realizations.insert(0, (e, Element.elementdesc(realization_relationship)))
        else:
            self.realizations.append((e, Element.elementdesc(realization_relationship)))


