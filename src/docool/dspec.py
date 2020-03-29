import shutil
import os
from pathlib import PureWindowsPath, Path
import subprocess
import re
import unidecode

import docool.model.model_processing as mp
from docool.utils import mycopy
import docool.model.anchors as anchors

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
    shutil.rmtree(args.projectdir / GENERATED_SPEC_PATH, ignore_errors=True)
    shutil.rmtree(hugodir, ignore_errors=True)
    # create hugo site
    cmd = 'hugo new site {0}'.format(str(hugodir))
    if args.debug:
        print(cmd)
    subprocess.run(cmd, shell=False)
    # setup themes
    if args.verbose:
        print('setup theme')
    with open(hugodir/'config.toml', 'w', encoding='utf8') as fout:
        fout.write('languageCode = "sk"\n')
        fout.write('DefaultContentLanguage = "sk"\n')
        fout.write('title = "{0}"\n'.format(args.projectname))
        fout.write('canonifyURLs = true\n')
        fout.write('\n')
        fout.write('[outputs]\n')
        fout.write('home = [ "HTML"]\n')
        # fout.write('\n')
        # fout.write('\n')
    # shutil.copy(args.projectdir/'src'/'res'/'hugo-config'/'configNoTheme.toml', hugodir/'config.toml')

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
    fout.write('\n{0} {1}\n\n'.format(level*'#', title))

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
                        realization_format_string = '* **[{realization_name}]({link})** ({element_type}): {realization_description}\n'
                        capabilty_realization_format_string = '\n**{realization_name}** ({element_type}): {realization_description}\n\n'
                        simple_realization_format_string = '* **[{realization_name}]({link})** ({element_type})\n'
                        product_format_string = '{realization_description}\n\n'
                        for realization in r.realizations:
                            if(mp.ArchiFileProcessor.isproduct(realization.type)):
                                fout.write(product_format_string.format(realization_description=realization.get_desc()))
                            elif realization.realization_relationship.desc is not None:
                                fout.write(
                                    realization_format_string.format(
                                        realization_name=realization.name, 
                                        realization_description=realization.realization_relationship.desc,
                                        element_type=mp.Element.type2sk(realization.type),
                                        link= anchors.getanchor(args, realization)))                          
                            elif realization.type == 'archimate:Capability':
                                fout.write(
                                    capabilty_realization_format_string.format(
                                        realization_name=realization.name, 
                                        realization_description=realization.desc,
                                        element_type=mp.Element.type2sk(realization.type),
                                        link= anchors.getanchor(args, realization)))                          
                            else:
                                fout.write(
                                    simple_realization_format_string.format(
                                        realization_name=realization.name, 
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

def publish_word_document(args):
    if args.verbose:
        print('publish word document')
    
    # create hugo site with one single page
    if args.debug:
        print('create hugo site with one single page')
    hugopath = args.projectdir / 'temp' / 'spec_local'
    onepagepath = args.projectdir/'temp'/'spec_onepage'
    shutil.rmtree(onepagepath, ignore_errors=True)
    onepagepath.mkdir(parents=True, exist_ok=True)
    ''' hugo parameters 
        -D, --buildDrafts
        -s, --source string
        -d, --destination string
        -t, --theme strings
        -b, --baseURL string         hostname (and path) to the root
    '''
    # cmd = 'hugo -D -s "{specpath}" -d "{onepagepath}" --themesDir C:\\Projects_src\\Work\\docool\\res\\themes\\ -t onePageHtml -b "{onepagepath}"'.format(specpath=hugopath, onepagepath=onepagepath)
    cmd = 'hugo -D -s "{specpath}" -d "{onepagepath}" --themesDir {themespath} -t onePageHtml -b "{onepagepath}"'.format(specpath=hugopath, onepagepath=onepagepath, themespath=str(args.docoolpath/'res'/'themes'))
    # cmd = ' -b "{onepagepath}"'.format(specpath=hugopath, onepagepath=onepagepath)
    if args.debug:
        print(cmd)
    subprocess.run(cmd, shell=False)
  
    # generate word
    if args.debug:
        print('generate word document')
    onepagehtml = onepagepath / 'index.html'
    wordpath = args.projectdir / 'release' / (args.projectname+'.docx')
    templatepath = args.docoolpath / 'res' / 'custom-reference.docx'
    wordpath.parent.mkdir(parents=True, exist_ok=True)
    cmd = 'pandoc {mainfile} -f html -t docx -o {outputname} --reference-doc={templatename} --verbose'.format(
        mainfile=str(onepagehtml), outputname=str(wordpath), templatename=str(templatepath))
    if args.debug:
        print(cmd)
    subprocess.run(cmd, shell=False)

def list_unsolved_requirements(args):
    processor = mp.ArchiFileProcessor(args.projectdir)
    c = 0
    reqs = processor.get_all_requirements()
    for r in sorted(reqs, key=lambda req: req.name):
        if len(r.realizations) < 1:
            print(r.name)
            c = c+1
    print('{0} requirements unsolved'.format(c))

def doit(args):
    if args.site or args.all:
        build_site(args)
    if args.build or args.all or args.update:
        if args.verbose:
            print('generate specification')
        # copy architecture description, insert element's description into text and generate anchors file
        enhance_spec(args)
        # generate requirements, use anchors file to create links
        generatereqs(args)
        copy_content(args)
    if args.doc or args.all:
        publish_word_document(args)
    if args.list:
        list_unsolved_requirements(args)