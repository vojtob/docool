import os
from pathlib import Path
import re
import unidecode

import docool.model.model_processing as mp
import docool.doc.hugo as hugo
from docool.utils import mycopy

def generate_elements_map(args, processor):
    """ generate map between archi elements and files where are elements mentioned
    """

    if args.debug:
        print('generate elements map')

    source_directory = hugo.getlocalpath(args) / 'content'
    emap = {}
    # walk over files in from directory
    for (dirpath, _, filenames) in os.walk(source_directory):
        for f in filenames:
            if not f.endswith('.md'):
                continue
            with open(Path(dirpath, f), 'r', encoding='utf8') as fin:
                for line in fin:
                    epattern = re.compile(r'\{\{< archianchor ([a-zA-Z]+) "([^"]+)" >\}\}')
                    m = epattern.search(line)
                    if m:
                        etype = m.group(1)
                        ename = m.group(2)
                        if args.debug:
                            print('MATCH: type:{0}, name:"{1}"'.format(etype, ename))
                        e = processor.find_element(etype,ename)
                        if e:
                            if not etype in emap:
                                emap[etype] = {}
                            tmap = emap[etype]
                            p = dirpath[len(str(source_directory)):].replace('\\','/')
                            if not f == '_index.md':
                                p = p + '/' + f[:-3]
                            tmap[ename] = p
                        else:
                            # print('!!!!!!!!! PROBLEM: Element {0}:{1} not found {2}'.format(etype,ename, sourcepath))
                            args.problems.append('Element {0}:{1} mentioned in {2} not found'.format(etype,ename, Path(dirpath, f)))
    return emap

def __urlify(name):
    return unidecode.unidecode("".join([c for c in name if re.match(r'\w', c)]))
    # return unidecode.unidecode(name.replace('.','_').replace(' ','_'))

def __get_frontmatter(title, weight):
    return '---\ntitle: "{0}"\nweight: {1}\n---\n\n\n'.format(title, weight)

def __get_header(title, level):
    return '\n{0} {1}\n\n'.format(level*'#', title)

def __writerealization(args, fout, realization, element2path):
    # Realization by product type is used for general remarks, only realization relationship is displayed, no reference to element
    if realization.type == 'Product':
        fout.write(realization.realization_relationship.desc+'\n\n')
        return

    # Capability means only simple description is displayed, no reference to element
    if realization.type == 'Capability':
        fout.write('**{capability_name}**: {realization_description}\n\n'.format(
            capability_name=realization.name, 
            realization_description=realization.desc))
        return
    
    try:
        p = element2path[realization.type][realization.name]
        link = '{{{{< archilink  {0} "{1}" "{2}" >}}}}'.format(realization.type, realization.name, p)
    except Exception:
        args.problems.append('not found path for element {0}:{1}'.format(realization.type, realization.name))
        link = '{{{{< archilink  {0} "{1}" "/">}}}}'.format(realization.type, realization.name)
    fout.write('* **[{realization_name}]({link})** ({element_type})'.format(
        realization_name=realization.name,
        element_type=mp.Element.type2sk(realization.type),
        link=link)
    )    
    if realization.realization_relationship.desc is not None:
        # add specific description
        fout.write(': ' + realization.realization_relationship.desc)
    fout.write('\n')

def __writereq(args, fout, req, depth, element2path):
    # req header
    if args.debug:
        print('    process requirement', req.name)
    
    # requirement header
    fout.write(__get_header(req.name, depth))  
    # requirement realizations
    if len(req.realizations) == 0:
        # fout.write('<font color="red">XXXXXX TODO: Ziadna realizacia poziadavky</font>\n\n')
        fout.write('XXXXXX TODO: Ziadna realizacia poziadavky\n\n')
        return
    # sort realizations, product is the first, than capabilities, other last
    # for realization in req.realizations:      
    for realization in sorted(req.realizations, key = lambda x: x.weight()):
        __writerealization(args, fout, realization, element2path)

def __process_req_folder(args, processor, sectionfolder, weight, parentpath, depth, element2path, createFolder = True):
    if args.debug:
        print('process folder', sectionfolder, depth)
    sectionname = __urlify(sectionfolder)
    sectionpath = parentpath / sectionname

    # create folder and reqirements descriptions for the section
    if createFolder:
        sectionpath.mkdir(parents=True, exist_ok=True)
        reqs = processor.get_requirements(sectionfolder)
        indexpath =  sectionpath / '_index.md'       
        with open(indexpath, 'w', encoding='utf8') as fout:
            fout.write(__get_frontmatter(sectionfolder, weight))
            if len(reqs) < 1:
                # fout.write('{{% children  %}}\n')
                fout.write('Adresár neobsahuje žiadne požiadavky\n')
            else:
                # process requirements
                for r in reqs:
                    __writereq(args, fout, r, depth, element2path)

    # process subfolders
    for w, subfolder in enumerate(sorted(processor.get_folders(sectionfolder))):
        __process_req_folder(args, processor, subfolder, w+2, sectionpath, depth+1, element2path)
    

def generatereqs(args):
    processor = mp.ArchiFileProcessor(args.projectdir)

    # generate map of archilinks to pages
    emap = generate_elements_map(args, processor)
    # print(emap)

    # generate requirements
    reqpath = hugo.getlocalpath(args) / 'content'
    __process_req_folder(args, processor, 'Requirements', None, reqpath, 2, emap, False)