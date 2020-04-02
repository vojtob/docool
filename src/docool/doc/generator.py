import os
from pathlib import Path
import re
import unidecode

import docool.model.model_processing as mp
import docool.doc.hugo as hugo
import docool.model.anchors as anchors
from docool.utils import mycopy

def insert_model_elements(args):
    """ copy architecture description, insert element's description into text and generate anchors file
    """

    if args.verbose:
        print('copy specification and insert element\'s descriptions')

    processor = mp.ArchiFileProcessor(args.projectdir)
    source_directory = args.projectdir / 'src' / 'doc' / args.name
    destination_directory = hugo.get_generated_path(args)

    # walk over files in from directory
    for (dirpath, dirnames, filenames) in os.walk(source_directory):
        # ignore hidden directories
        if Path(dirpath).name.startswith('.'):
            dirnames.clear()
            continue

        # create destination directory
        d = Path(dirpath.replace(str(source_directory), str(destination_directory)))
        d.mkdir(parents=True, exist_ok=True)
        
        for f in filenames:
            sourcefile = Path(dirpath, f)
            destfile = str(sourcefile).replace(str(source_directory), str(destination_directory))
            relativepath = str(sourcefile).replace(str(source_directory), '')
            __copy_and_add_elements_description(sourcefile, Path(destfile), relativepath, args, processor)

def __copy_and_add_elements_description(sourcepath, destpath, relativepath, args, processor):
    with open(sourcepath, 'r', encoding='utf8') as fin:
        with open(destpath, 'w', encoding='utf8') as fout:
            for line in fin:
                epattern = re.compile(r'@(INSERT|TINSERT) ([a-zA-Z]+) (((\b\w+\b)?\s*[/&-,]?\s*)+)\1@')
                m = epattern.search(line)
                if m:
                    fout.write(line[:m.start()])
                    command = m.group(1)
                    etype = m.group(2)
                    ename = m.group(3)[:-1]
                    if args.debug:
                        print('MATCH: type:{0}, name:"{1}", command:{2}'.format(etype, ename, command))
                    e = processor.find_element(etype,ename)
                    if e:
                        t = e.desc.replace("\r", " ")
                        if command=='TINSERT':
                            tls = t.split('\n')
                            t = ''
                            for tl in tls:
                                if tl.startswith('*') and (tl.find('*', 1)==-1):
                                    t = t + '<li>' + tl[1:-1] + '</li>'
                                else:
                                    t = t + tl[:-1] + '<BR/>'
                        t = anchors.saveanchor(args, e, relativepath) + t
                        fout.write(t)
                    else:
                        print('!!!!!!!!! PROBLEM: Element {0}:{1} not found {2}'.format(etype,ename, sourcepath))
                    fout.write(line[m.end():])
                else:
                    fout.write(line)

def __urlify(name):
    return unidecode.unidecode("".join([c for c in name if re.match(r'\w', c)]))
    # return unidecode.unidecode(name.replace('.','_').replace(' ','_'))

def __get_frontmatter(title, weight):
    return '---\ntitle: "{0}"\nweight: {1}\n---\n\n\n'.format(title, weight)

def __get_header(title, level):
    return '\n{0} {1}\n\n'.format(level*'#', title)

def __writerealization(args, fout, realization):
    # Realization by product type is used for general remarks, only realization relationship is displayed, no reference to element
    if mp.ArchiFileProcessor.isproduct(realization.type):
        fout.write(realization.realization_relationship.desc+'\n\n')
        return

    # Capability means only simple description is displayed, no reference to element
    if realization.type == 'archimate:Capability':
        fout.write('**{capability_name}**: {realization_description}\n\n'.format(
            capability_name=realization.name, 
            realization_description=realization.desc))
        return
    
    fout.write('* **[{realization_name}]({link})** ({element_type})'.format(
        realization_name=realization.name,
        element_type=mp.Element.type2sk(realization.type),
        link= anchors.getanchor(args, realization))
    )
    if realization.realization_relationship.desc is not None:
        # add specific description
        fout.write(': ' + realization.realization_relationship.desc)
    fout.write('\n')

def __writereq(args, fout, req, depth):
    # req header
    if args.debug:
        print('    process requirement', req.name)
    
    # requirement header
    fout.write(__get_header(req.name, depth))  
    # requirement realizations
    if len(req.realizations) == 0:
        fout.write('<font color="red">XXXXXX TODO: Ziadna realizacia poziadavky</font>\n\n')
        return
    # sort realizations, product is the first, than capabilities, other last
    # for realization in req.realizations:      
    for realization in sorted(req.realizations, key = lambda x: x.weight()):
        __writerealization(args, fout, realization)

def __process_req_folder(args, processor, sectionfolder, weight, parentpath, depth, createFolder = True):
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
                fout.write('{{% children  %}}\n')
            else:
                # process requirements
                for r in reqs:
                    __writereq(args, fout, r, depth)
                    
    else:
        print('do not create folder')

    # process subfolders
    for w, subfolder in enumerate(sorted(processor.get_folders(sectionfolder))):
        __process_req_folder(args, processor, subfolder, w+2, sectionpath, depth+1)
    

def generatereqs(args):
    processor = mp.ArchiFileProcessor(args.projectdir)
    reqpath = hugo.get_generated_path(args)
    __process_req_folder(args, processor, 'Requirements', None, reqpath, 2, False)

def copy_content(args):
    dest_content = hugo.get_local_path(args)   
    # copy content
    if args.verbose:
        print('copy content into spec')
    mycopy(hugo.get_generated_path(args), dest_content / 'content', args)
    # copy images
    if args.verbose:
        print('copy images')
    # copy exported images
    mycopy(args.projectdir / 'temp' / 'img_exported', dest_content / 'static' / 'img', args)
    # overwrite them with images with icons
    mycopy(args.projectdir / 'temp' / 'img_icons', dest_content / 'static' / 'img', args)
    # copy areas images
    mycopy(args.projectdir / 'temp' / 'img_areas', dest_content / 'static' / 'img', args)
