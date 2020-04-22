import xml.etree.ElementTree as ET

class ArchiFileProcessor:
    ns = {'xsi': "http://www.w3.org/2001/XMLSchema-instance",
        'archimate': 'http://www.archimatetool.com/archimate'}

    def __init__(self, projectdir):
        # modelname = projectdir.split('\\')[-1]
        # modelname = str(projectdir.stem)+'.archimate'
        modelpath = projectdir / 'src_doc' / 'model' / (str(projectdir.stem)+'.archimate')
        self.tree = ET.parse(modelpath)
    
    def get_element(self, eid):
        return self.tree.getroot().find(".//element[@id='{0}']".format(eid), self.ns)

    def find_element(self, etype, ename):
        e = self.tree.getroot().find(".//element[@xsi:type='archimate:{0}'][@name='{1}']".format(etype,ename), self.ns)
        if e:
            return Element(e)
        return None

    def get_folder(self, foldername):
        return self.tree.getroot().find(".//folder[@name='{0}']".format(foldername), self.ns)

    def __create_requirements(self, requirements):
        # get all requirements by type converted to Requirement class
        req_elements = []
        relationshipsfolder = self.get_folder('Relations')
        for r in requirements:
            req_element = Requirement(r)
            req_elements.append(req_element)
            # find realizations
            cond = ".//element[@xsi:type='archimate:RealizationRelationship'][@target='{0}']".format(req_element.eid)
            for realizationRelationship in relationshipsfolder.findall(cond, self.ns):
                e = self.get_element(realizationRelationship.attrib['source'])
                req_element.add_realization(realizationRelationship, e)
        return req_elements

    def get_all_requirements(self):
        requirements = self.tree.getroot().findall(".//element[@xsi:type='archimate:Requirement']", self.ns)
        return self.__create_requirements(requirements)

    def get_requirements(self, foldername):
        # get folder by name
        requirements = self.get_folder(foldername).findall("element[@xsi:type='archimate:Requirement']", self.ns)
        return self.__create_requirements(requirements)

    def get_folders(self, foldername):
        # get folder by name
        parentfolder = self.get_folder(foldername)
        if not parentfolder:
            return []
        # get all requirements by type converted to Requirement class
        return [Element.elementname(f) for f in parentfolder.findall("folder", self.ns)]


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
        if 'name' in element.attrib:
            return element.attrib['name']
        else:
            return None
        
    @staticmethod
    def elementtype(element):
        keyname = '{' + ArchiFileProcessor.ns['xsi'] + '}type'
        return element.attrib[keyname][len('archimate:'):]
        
    @staticmethod
    def elementdesc(element):
        eDoc = element.find('documentation')
        if (eDoc == None):
            return None
        else:
            return eDoc.text
            # return eDoc.text.replace('\n', '').replace('<ul>\r', '<ul>').replace('</li>\r', '</li>').replace('\r', '<BR/>').replace(' ', '• ')

    @staticmethod
    def type2sk(type):
        conversion = {
            'BusinessActor':'Biznis Aktér',
            'BusinessRole':'Biznis Rola',
            'BusinessService':'Biznis služba',
            'BusinessInterface':'Biznis rozhranie, komunikačný kanál',
            'BusinessFunction':'Biznis funkcia',
            'BusinessProcess':'Biznis proces',
            'ApplicationComponent':'Aplikačný komponent, modul',
            'ApplicationFunction':'Aplikačná funkcia',
            'ApplicationService':'Aplikačná služba',
            'ApplicationInterface':'Aplikačné rozhranie',
            'ApplicationProcess':'Aplikačný proces',
            'SystemSoftware':'Softvér',
            'Artifact':'Technologický Artefakt',
            'Capability':'Schopnosť, prístup'
        }
        
        # return conversion[type.split(':')[1]]
        return conversion[type]


class Requirement(Element):
    """ Requirement is Element with description how it is realized. 
        It is list of pairs (Element, explanation), where Element is realizing element 
        and explanation is description how element realize requirement"""

    def __init__(self, element):
        super().__init__(element)
        self.realizations = []

    def add_realization(self, realization_relationship, realization_element):
        self.realizations.append(Realization(realization_element, realization_relationship))
    
class Realization(Element):
    """special class for realization of requirements. It has two parts:
        1. realization element - it is core element that realize requirement
        2. realization relation description - it is used when there description of core element is not suitable for this requirement
    """

    def __init__(self, element, relation):
        # create as element
        super().__init__(element)
        self.realization_relationship = Element(relation)

    def weight(self):
        if self.type == 'Product':
            return '000000' + self.name
        if self.type == 'Capability':
            return '000001' + self.name
        return '999999' + self.name
        