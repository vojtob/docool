import os
import pathlib
import subprocess
import json
from pathlib import PureWindowsPath, Path
from docool.images import img_processing

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

def convert_svg(args):
    # convert svg files to png files
    img_processing.process_images(
        args.projectdir / 'temp' / 'img_exported_svg',
        args.projectdir / 'temp' / 'img_exported',
        '.svg', '.png',
        str(Path(os.environ['IM_HOME'], 'magick')) + ' -density 144 {srcfile} {destfile}',
        args.verbose, args.debug)

def add_icons(args):
    if args.verbose:
        print('add icons')
    # read images icons definitions   
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
    with open(args.projectdir / 'src' / 'img' / 'img_focus.json') as imagesFile:
        imagedefs = json.load(imagesFile)
    for imgdef in imagedefs:
        if args.file is not None and (imgdef['fileName'] != args.file):
            # we want to process a specific file, but not this
            continue
        img_processing.areas2image(imgdef, args)

def doit(args):
    if args.archi or args.all:
        export_archi(args)
    if args.svg or args.all:
        convert_svg(args)
    if args.icons or args.all:
        add_icons(args)
    if args.areas or args.all:
        add_areas(args)
