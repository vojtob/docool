import shutil
import os
from pathlib import PureWindowsPath, Path
import subprocess
from docool.utils import mycopy
import docool.model.process_requirements_pages as proc_req

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
    mycopy(args.docoolpath/'res'/'themes'/theme, themedir, args.debug)
    theme = 'onePageHtml'
    themedir = hugodir/'themes'/theme
    themedir.mkdir(parents=True, exist_ok=True)
    mycopy(args.docoolpath/'res'/'themes'/theme, themedir, args.debug)
    shutil.copy(args.projectdir/'src'/'res'/'hugo-config'/'configNoTheme.toml', hugodir/'config.toml')

def update_content(args):
    hugodir = args.projectdir / 'temp' / 'spec_local'
    # copy content
    if args.verbose:
        print('copy content into spec')
    mycopy(args.projectdir/'src'/'specifikacia', hugodir/'content', args.debug)

    # copy images
    if args.verbose:
        print('copy images')
    imgspath = hugodir/'static'/'img'
    # copy exported images
    mycopy(args.projectdir / 'temp' / 'img_exported', imgspath, args.debug)
    # overwrite them with images with icons
    mycopy(args.projectdir / 'temp' / 'img_icons', imgspath, args.debug)
    # copy areas images
    mycopy(args.projectdir / 'temp' / 'img_areas', imgspath, args.debug)

def generate_specification(args):
    if args.verbose:
        print('generate specification')
    proc_req.generatereqs(args)

def doit(args):
    if args.build or args.all:
        build_specification(args)
        update_content(args)
    if args.update:
        update_content(args)
    if args.requirements or args.all:
        generate_specification(args)
    
