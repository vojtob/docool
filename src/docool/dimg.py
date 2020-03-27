import os
import pathlib
import subprocess
import json
import time
from pathlib import PureWindowsPath, Path
import shutil

from docool.images import img_processing
from docool.utils import mycopy

movefiles = []

def __img_walk(args, source_path, destination_path, orig_extension, new_extension, onfile):
    if args.verbose:
        print('convert {0}({1}) -> {2}({3})'.format(str(source_path), orig_extension, str(destination_path), new_extension))
    # walk over files in from directory
    for (dirpath, _, filenames) in os.walk(source_path):
        # create destination directory
        d = Path(dirpath.replace(str(source_path), str(destination_path)))       
        d.mkdir(parents=True, exist_ok=True)
        # convert files with specific extension
        for f in [f for f in filenames if f.endswith(orig_extension)]:          
            # ffrom is original full name with path and orig extension
            ffrom = os.path.join(dirpath, f)
            # fto is destination full name with path and new extension
            fto = ffrom.replace(str(source_path), str(destination_path)).replace(orig_extension, new_extension)
            onfile(args, ffrom, fto, orig_extension, new_extension)

def export_archi(args):
    if args.verbose:
        print('export images from archi - OPEN ARCHI!')
    # export images from archi
    cmd = '"{autoit_path}" {script_path} {project_path}'.format(
        autoit_path= PureWindowsPath('C:/Program Files (x86)/AutoIt3/AutoIt3_x64.exe'), 
        script_path=args.docoolpath / 'src' / 'autoit' / 'exportImages.au3', 
        project_path=args.projectdir)
    if args.debug:
        print(cmd)
    subprocess.run(cmd, shell=False)

def convert_svg(args, fromfile, tofile, orig_extension, new_extension):
    svg_command = str(Path(os.environ['IM_HOME'], 'magick')) + ' -density 144 {srcfile} {destfile}'
    cmd = svg_command.format(srcfile=fromfile, destfile=tofile)
    if args.debug:
        print(cmd)
    subprocess.run(cmd, shell=False)

def convert_uml(args, fromfile, tofile, orig_extension, new_extension):
    global movefiles
    uxf_command = str(Path('C:/', 'prg', 'Umlet', 'Umlet')) + ' -action=convert -format=png -filename="{srcfile}"'
    cmd = uxf_command.format(srcfile=fromfile)
    if args.debug:
        print(cmd)
    subprocess.run(cmd, shell=False)
    x = fromfile.replace(orig_extension, new_extension)
    movefiles.append((x, tofile))
   
def convert_mmd(args, fromfile, tofile, orig_extension, new_extension):
    mmPath = os.path.join('C:/', 'prg', 'mermaid', 'node_modules', 'mermaid.cli', 'index.bundle.js')
    mmd_command = 'node {mmpath} -w 1400 -i {srcfile} -o {destfile}'
    cmd = mmd_command.format(srcfile=fromfile, destfile=tofile, mmpath=mmPath)
    if args.debug:
        print(cmd)
    subprocess.run(cmd, shell=False)
        
def copy_png(args, fromfile, tofile, orig_extension, new_extension):
    if args.debug:
        print('copy {0}->{1}'.format(fromfile, tofile))
    shutil.copyfile(fromfile, tofile)
        
def add_icons(args):
    if args.verbose:
        print('add icons')
    # read images icons definitions   
    if not (args.projectdir / 'src' / 'img' / 'images.json').exists():
        if args.verbose:
            print('no icons, skipp it')
        return
    with open(args.projectdir / 'src' / 'img' / 'images.json') as imagesFile:
        imagedefs = json.load(imagesFile)
    for imgdef in imagedefs:
        if args.file is not None and (imgdef['fileName'] != args.file):
            # we want to process a specific file, but not this
            continue
        img_processing.icons2image(imgdef, args)

def add_areas(args):
    if args.verbose:
        print('add areas')
    # read images icons definitions   
    if not (args.projectdir / 'src' / 'img' / 'img_focus.json').exists():
        if args.verbose:
            print('no areas, skipp it')
        return
    with open(args.projectdir / 'src' / 'img' / 'img_focus.json') as imagesFile:
        imagedefs = json.load(imagesFile)
    for imgdef in imagedefs:
        if args.file is not None and (imgdef['fileName'] != args.file):
            # we want to process a specific file, but not this
            continue
        img_processing.areas2image(imgdef, args)

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


def doit(args):
    global movefiles

    if args.archi or args.all:
        export_archi(args)

    if args.svg or args.all:
        # convert svg files to png files
        __img_walk(args, 
            args.projectdir / 'temp' / 'img_exported_svg', 
            args.projectdir / 'temp' / 'img_exported', 
            '.svg', '.png', convert_svg)

    if args.umlet or args.all:
        # convert uxf files to png files
        movefiles = []
        __img_walk(args, 
            args.projectdir / 'src' / 'img',
            args.projectdir / 'temp' / 'img_exported', 
            '.uxf', '.png', convert_uml)
        # move files
        if len(movefiles) < 1:
            if args.verbose:
                print('no uxf files generated')
            return
        for (fromFile, toFile) in movefiles:
            if args.debug:
                print('move file {0} -> {1}'.format(fromFile, toFile))
            while True:
                try:
                    os.replace(fromFile, toFile)
                    break
                except (PermissionError, FileNotFoundError):
                    pass

    if args.mermaid or args.all:
        # convert mm files to png files
        __img_walk(args, 
            args.projectdir / 'src' / 'img',
            args.projectdir / 'temp' / 'img_exported', 
            '.mmd', '.png', convert_mmd)

    if args.png or args.all:
        # copy png file
        __img_walk(args, 
            args.projectdir / 'src' / 'img',
            args.projectdir / 'temp' / 'img_exported', 
            '.png', '.png', copy_png)

    if args.icons or args.all:
        add_icons(args)

    if args.areas or args.all:
        add_areas(args)

    if args.publish or args.all:
        publish_images(args)
