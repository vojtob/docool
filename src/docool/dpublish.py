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
    imgspath.parent.mkdir(parents=True, exist_ok=True)
    # copy png images from src  
    # copy exported images
    mycopy(args.projectdir / 'temp' / 'img_exported', imgspath, args.debug)
    # overwrite them with images with icons
    mycopy(args.projectdir / 'temp' / 'img_icons', imgspath, args.debug)
    # copy areas images
    mycopy(args.projectdir / 'temp' / 'img_areas', imgspath, args.debug)

def publish_word_document(args):
    if args.verbose:
        print('publish word document')
    
    wordpath = args.projectdir/'temp'/'doc_word'
    shutil.rmtree(wordpath, ignore_errors=True)
    wordpath.mkdir(parents=True, exist_ok=True)
    releasepath = args.projectdir / 'release'
    releasepath.mkdir(parents=True, exist_ok=True)
    hugopath = args.projectdir / 'temp' / 'spec_local'
   
    # create hugo site with one sinlge page
    if args.debug:
        print('create hugo site with one sinlge page')
    cmd = 'hugo -D -s "{specpath}" -t onePageHtml -d "{wordpath}" -b "{wordpath}"'.format(specpath=hugopath, wordpath=wordpath)
    if args.debug:
        print(cmd)
    subprocess.run(cmd, shell=False)

    # generate word
    if args.debug:
        print('generate word document')
    # modelname = str(projectdir.stem)+'.archimate'
    cmd = 'pandoc {mainfile} -f html -t docx -o {outputname} --verbose'.format(
        mainfile=wordpath/'index.html', outputname=releasepath/(args.projectname+'.docx'))
    if args.debug:
        print(cmd)
    subprocess.run(cmd, shell=False)



def doit(args):
    if args.images:
        publish_images(args)
    if args.doc:
        publish_word_document(args)