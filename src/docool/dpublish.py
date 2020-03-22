import shutil
import os
from pathlib import PureWindowsPath, Path
import subprocess
from docool.utils import mycopy

def publish_images(args):
    if args.verbose:
        print('publish images')
    # publish images to release dir
    imgspath = args.projectdir / 'release' / 'img'
    imgspath.mkdir(parents=True, exist_ok=True)
    # copy png images from src  
    # copy exported images
    mycopy(args.projectdir / 'temp' / 'img_exported', imgspath, args)
    # overwrite them with images with icons
    mycopy(args.projectdir / 'temp' / 'img_icons', imgspath, args)
    # copy areas images
    mycopy(args.projectdir / 'temp' / 'img_areas', imgspath, args)

def publish_word_document(args):
    if args.verbose:
        print('publish word document')
    
    # create hugo site with one single page
    if args.debug:
        print('create hugo site with one single page')
    hugopath = args.projectdir / 'temp' / 'spec_local'
    onepagepath = args.projectdir/'temp'/'hugo_onepage'
    shutil.rmtree(onepagepath, ignore_errors=True)
    onepagepath.mkdir(parents=True, exist_ok=True)
    ''' hugo parameters 
        -D, --buildDrafts
        -s, --source string
        -d, --destination string
        -t, --theme strings
        -b, --baseURL string         hostname (and path) to the root
    '''
    cmd = 'hugo -D -s "{specpath}" -t onePageHtml -d "{onepagepath}" -b "{onepagepath}"'.format(specpath=hugopath, onepagepath=onepagepath)
    if args.debug:
        print(cmd)
    subprocess.run(cmd, shell=False)
  
    # generate word
    if args.debug:
        print('generate word document')
    onepagehtml = onepagepath / 'index.html'
    wordpath = args.projectdir / 'release' / (args.projectname+'.docx')
    wordpath.parent.mkdir(parents=True, exist_ok=True)
    cmd = 'pandoc {mainfile} -f html -t docx -o {outputname} --verbose'.format(
        mainfile=str(onepagehtml), outputname=str(wordpath))
    if args.debug:
        print(cmd)
    subprocess.run(cmd, shell=False)

def doit(args):
    if args.images:
        publish_images(args)
    if args.doc:
        publish_word_document(args)