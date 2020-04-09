import shutil
import os
from pathlib import PureWindowsPath, Path
import subprocess
import re
import unidecode

import docool.model.model_processing as mp
from docool.utils import mycopy
import docool.doc.hugo as hugo
import docool.doc.generator as docgen
                      
def generate_word_document(args):
    if args.verbose:
        print('generate word document')
    onepagehtml = hugo.getonepagepath(args) / 'index.html'
    templatepath = args.docoolpath / 'res' / 'custom-reference.docx'

    wordpath = args.projectdir / 'release' / (args.projectname + '_' + args.name + '.docx')
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
        if args.verbose:
            print('build site')
        hugo.build_site(args)
    if args.images or args.all or args.update:
        if args.verbose:
            print('copy images')
        dest_content = hugo.getlocalpath(args)
        mycopy(args.projectdir / 'temp' / 'img_exported', dest_content / 'static' / 'img', args)
        # overwrite them with images with icons
        mycopy(args.projectdir / 'temp' / 'img_icons', dest_content / 'static' / 'img', args)
        # copy areas images
        mycopy(args.projectdir / 'temp' / 'img_areas', dest_content / 'static' / 'img', args)
    if args.content or args.all or args.update:
        if args.verbose:
            print('copy content')
        mycopy(args.projectdir / 'src' / 'doc' / args.name, hugo.getlocalpath(args) / 'content', args)
    if args.requirements or args.all or args.update:
        if args.verbose:
            print('generate requirements pages')
        docgen.generatereqs(args)
    if args.doc or args.all:
        if args.verbose:
            print('publish word document')
        hugo.export_onepage(args)
        generate_word_document(args)
    # if args.web or args.all:
    #     publish_web(args)
    if args.list:
        list_unsolved_requirements(args)