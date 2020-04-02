import shutil
import os
from pathlib import PureWindowsPath, Path
import subprocess
import re
import unidecode

import docool.model.model_processing as mp
from docool.utils import mycopy
import docool.model.anchors as anchors
import docool.doc.hugo as hugo
import docool.doc.generator as docgen
                      
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
        hugo.build_site(args)
    if args.content or args.all:
        if args.verbose:
            print('generate specification')
        # copy architecture description, insert element's description into text and generate anchors file
        docgen.insert_model_elements(args)
        # generate requirements, use anchors file to create links
        docgen.generatereqs(args)
        docgen.copy_content(args)
    if args.doc or args.all:
        publish_word_document(args)
    # if args.web or args.all:
    #     publish_word_document(args)
    if args.list:
        list_unsolved_requirements(args)