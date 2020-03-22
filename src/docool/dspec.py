import shutil
import os
from pathlib import PureWindowsPath, Path
import subprocess
import re
import unidecode

import docool.model.model_processing as mp
from docool.utils import mycopy
import docool.model.anchors as anchors
import docool.model.process_requirements_pages as proc_req

processor = None
HUGO_PATH = Path('temp', 'spec_local')
GENERATED_SPEC_PATH = Path('temp', 'spec_generated')

def build_site(args):
    if args.verbose:
        print('build specification')

    hugodir = args.projectdir / HUGO_PATH
    
    # clean
    if args.verbose:
        print('clean ', str(hugodir))
    shutil.rmtree(hugodir, ignore_errors=True)
   
    # create hugo site
    cmd = 'hugo new site {0}'.format(str(hugodir))
    subprocess.run(cmd, shell=False)

    # setup themes
    if args.verbose:
        print('setup theme')
    # theme = 'hugo-theme-docdock'
    # themedir = hugodir/'themes'/theme
    # themedir.mkdir(parents=True, exist_ok=True)
    # mycopy(args.docoolpath/'res'/'themes'/theme, themedir, args)
    # theme = 'onePageHtml'
    # themedir = hugodir/'themes'/theme
    # themedir.mkdir(parents=True, exist_ok=True)
    # mycopy(args.docoolpath/'res'/'themes'/theme, themedir, args)
    shutil.copy(args.projectdir/'src'/'res'/'hugo-config'/'configNoTheme.toml', hugodir/'config.toml')


def enhance_spec(args):
    """ copy architecture description, insert element's description into text and generate anchors file
    """

    if args.verbose:
        print('copy specification and insert element\'s descriptions')
    global processor
    processor = mp.ArchiFileProcessor(args.projectdir)
    source_directory = args.projectdir/'src'/'specifikacia'
    destination_directory = args.projectdir / GENERATED_SPEC_PATH

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
            copy_and_add_elements_description(sourcefile, Path(destfile), relativepath, args)


def copy_and_add_elements_description(sourcepath, destpath, relativepath, args):
    global processor
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
                        print('!!!!!!!!! PROBLEM: Element {0}:{1} not found'.format(etype,ename))
                    fout.write(line[m.end():])
                else:
                    fout.write(line)

def write_frontmatter(fout, title, weight):
    fout.write('---\ntitle: "{0}"\nweight: {1}\n---\n\n\n'.format(title, weight))

def write_header(fout, title, level):
    fout.write('\n{0} {1}\n'.format(level*'#', title))

def get_mdname(name):
    return unidecode.unidecode('{0}.md'.format(name.replace('.','-').replace(' ','-')))

def generatereqs(args):
    processor = mp.ArchiFileProcessor(args.projectdir)
    foldername = 'Requirements'
    generated_spec_path = args.projectdir / GENERATED_SPEC_PATH
    weight = 1
    for sectionfolder in sorted(processor.get_folders(foldername)):
        weight = weight+1
        # create folder for a section
        if args.debug:
            print('create section', sectionfolder)
        sectionname = get_mdname(sectionfolder)
        sectionpath =  generated_spec_path / '10-Requirements' / sectionname
        sectionpath.mkdir(parents=True, exist_ok=True)
        indexpath =  sectionpath / '_index.md'
        with open(indexpath, 'w', encoding='utf8') as fout:
            write_frontmatter(fout, sectionfolder, weight)
            fout.write('{{% children  %}}\n')
        # process subfolder for chapter
        subweight = 1
        for chapterfolder in sorted(processor.get_folders(sectionfolder)):
            # create page for folder
            if args.debug:
                print('  create chapter', chapterfolder)
            subweight = subweight+1
            chaptername = get_mdname(chapterfolder)
            chapterpath =  sectionpath / chaptername
            with open(chapterpath, 'w', encoding='utf8') as fout:
                write_frontmatter(fout, chapterfolder, subweight)
                # process requirements
                for r in processor.get_requirements(chapterfolder):
                    # req header
                    if args.debug:
                        print('    process requirement', r.name)
                    # requirement header
                    write_header(fout, r.name, 4)
                    # requirement realization
                    if len(r.realizations) == 0:
                        fout.write('<font color="red">XXXXXX TODO: Ziadna realizacia poziadavky</font>\n\n')
                    else:
                        realization_format_string = '**[{realization_name}]({link})** ({element_type}): {realization_description}\n\n'
                        product_format_string = '{realization_description}\n\n'
                        for realization in r.realizations:
                            if(mp.ArchiFileProcessor.isproduct(realization.type)):
                                fout.write(product_format_string.format(realization_description=realization.get_desc()))
                            else:
                                fout.write(
                                    realization_format_string.format(
                                        realization_name=realization.name, 
                                        realization_description=realization.get_desc(),
                                        element_type=mp.Element.type2sk(realization.type),
                                        link= anchors.getanchor(args, realization)))                          

def copy_content(args):
    global processor
    processor = mp.ArchiFileProcessor(args.projectdir)
    anchors.deleteanchors(args)
    hugodir = args.projectdir / HUGO_PATH
    
    # copy content
    if args.verbose:
        print('copy content into spec')
    mycopy(args.projectdir/GENERATED_SPEC_PATH, hugodir/'content', args)

    # copy images
    if args.verbose:
        print('copy images')
    # copy exported images
    mycopy(args.projectdir / 'temp' / 'img_exported', hugodir/'static'/'img', args)
    # overwrite them with images with icons
    mycopy(args.projectdir / 'temp' / 'img_icons', hugodir/'static'/'img', args)
    # copy areas images
    mycopy(args.projectdir / 'temp' / 'img_areas', hugodir/'static'/'img', args)

def doit(args):
    if args.site or args.all:
        build_site(args)
    if args.generate or args.all:
        if args.verbose:
            print('generate specification')
        # copy architecture description, insert element's description into text and generate anchors file
        enhance_spec(args)
        # generate requirements, use anchors file to create links
        proc_req.generatereqs(args)
    if args.build or args.all:
        copy_content(args)
    
