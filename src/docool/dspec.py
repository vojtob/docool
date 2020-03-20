import shutil
import os
from pathlib import PureWindowsPath, Path
import subprocess
import re

import docool.model.model_processing as mp
from docool.utils import mycopy
import docool.model.anchors as anchors
import docool.model.process_requirements_pages as proc_req

processor = None

def build_specification(args):
    if args.verbose:
        print('build specification')

    hugodir = args.projectdir / 'temp' / 'spec_local'
    
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
    theme = 'hugo-theme-docdock'
    themedir = hugodir/'themes'/theme
    themedir.mkdir(parents=True, exist_ok=True)
    mycopy(args.docoolpath/'res'/'themes'/theme, themedir, args)
    theme = 'onePageHtml'
    themedir = hugodir/'themes'/theme
    themedir.mkdir(parents=True, exist_ok=True)
    mycopy(args.docoolpath/'res'/'themes'/theme, themedir, args)
    shutil.copy(args.projectdir/'src'/'res'/'hugo-config'/'configNoTheme.toml', hugodir/'config.toml')

def copy_and_add_elements_description(sourcepath, destpath, relativepath, args):
    global processor
    with open(sourcepath, 'r', encoding='utf8') as fin:
        with open(destpath, 'w', encoding='utf8') as fout:
            for line in fin:
                epattern = re.compile(r'@(INSERT|TINSERT) ([a-zA-Z]+) (((\b\w+\b)?\s*[/&-,]?\s*)+)\1@')
                # iterator = epattern.finditer(line)
                # for m in iterator:
                #     print('MATCH: |{0}|'.format(m.group()))
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
                                # t = t + '<BR/>'

                        # add anchor
                        # relativepath = relativepath[:-3]
                        # if relativepath.endswith('_index'):
                        #     relativepath = relativepath[:-len('_index')]
                        t = anchors.saveanchor(args, e, relativepath) + t
                        fout.write(t)
                    else:
                        print('!!! Element {0}:{1} not found'.format(etype,ename))
                    fout.write(line[m.end():])
                else:
                    fout.write(line)

def copy_content(args):
    global processor
    processor = mp.ArchiFileProcessor(args.projectdir)
    anchors.deleteanchors(args)
    hugodir = args.projectdir / 'temp' / 'spec_local'
    # copy content
    if args.verbose:
        print('copy content into spec')
    mycopy(args.projectdir/'src'/'specifikacia', hugodir/'content', args, onfile=copy_and_add_elements_description)
    # copy images
    if args.verbose:
        print('copy images')
    imgspath = hugodir/'static'/'img'
    # copy exported images
    mycopy(args.projectdir / 'temp' / 'img_exported', imgspath, args)
    # overwrite them with images with icons
    mycopy(args.projectdir / 'temp' / 'img_icons', imgspath, args)
    # copy areas images
    mycopy(args.projectdir / 'temp' / 'img_areas', imgspath, args)

def generate_specification(args):
    if args.verbose:
        print('generate specification')
    proc_req.generatereqs(args)

def doit(args):
    if args.build or args.all:
        build_specification(args)
    if args.content or args.all:
        copy_content(args)
    if args.requirements or args.all:
        generate_specification(args)
    
