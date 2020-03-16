import shutil
import os
from pathlib import PureWindowsPath, Path
import subprocess

def mycopy(source_directory, destination_directory, debug=False):
    if debug:
        print('copy {0} -> {1}'.format(str(source_directory), str(destination_directory)))
    # walk over files in from directory
    for (dirpath, _, filenames) in os.walk(source_directory):
        # create destination directory
        d = Path(dirpath.replace(str(source_directory), str(destination_directory)))
        d.mkdir(parents=True, exist_ok=True)
        
        # convert files with specific extension
        for f in filenames:
            sourcefile = Path(dirpath, f)
            destfile = str(sourcefile).replace(str(source_directory), str(destination_directory))
            shutil.copy(str(sourcefile), destfile)

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

def create_specification(args):
    hugodir = args.projectdir / 'temp' / 'spec_local'
    
    # clean
    if args.verbose:
        print('clean ', str(hugodir))
    shutil.rmtree(hugodir, ignore_errors=True)
    
    # create hugo site
    cmd = 'hugo new site {0}'.format(str(hugodir))
    subprocess.run(cmd, shell=False)

    # copy content
    if args.verbose:
        print('copy content into spec')
    mycopy(args.projectdir/'src'/'specifikacia', hugodir/'content', args.debug)

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

def do_specification(args):
    if args.build:
        create_specification(args)
    if args.generate:
        generate_specification(args)
    
