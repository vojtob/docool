import os
import pathlib
import argparse
import subprocess

from pathlib import PureWindowsPath, Path
import docool

def export_archi(args):
    # export images from archi
    # autoit_path = os.path.normpath('C:/Program Files (x86)/AutoIt3/AutoIt3_x64.exe')
    # script_path = args.docoolpaht / 'src' / 'autoit' / 'exportImages.au3'
    cmd = '"{autoit_path}" {script_path} {project_path}'.format(
        autoit_path= PureWindowsPath('C:/Program Files (x86)/AutoIt3/AutoIt3_x64.exe'), 
        script_path=args.docoolpath / 'src' / 'autoit' / 'exportImages.au3', 
        project_path=args.projectdir)
    if args.verbose:
        print(cmd)
    subprocess.run(cmd, shell=False)

def __process_images(source_directory, destination_directory, orig_extension, new_extension, command, verbose):
    # walk over files in from directory
    for (dirpath, _, filenames) in os.walk(source_directory):
        # create destination directory
        d = Path(dirpath.replace(str(source_directory), str(destination_directory)))
        
        if not d.exists():
            if verbose:
                print('create directory', d)
            d.mkdir()
            # os.makedirs(d)

        # convert files with specific extension
        for f in [f for f in filenames if f.endswith(orig_extension)]:          
            ffrom = os.path.join(dirpath, f)
            # change directory and extension
            fto = ffrom.replace(str(source_directory), str(destination_directory)).replace(orig_extension, new_extension)
            cmd = command.format(srcfile=ffrom, destfile=fto)
            if verbose:
                print(cmd)
            subprocess.run(cmd, shell=False)

def convert_svg(args):
    # convert svg files to png files
    if args.svg:
        __process_images(
            args.projectdir / 'temp' / 'img_exported_svg',
            args.projectdir / 'temp' / 'img_exported',
            '.svg', '.png',
            str(Path(os.environ['IM_HOME'], 'magick')) + ' -density 144 {srcfile} {destfile}',
            args.verbose)

def parse_args():
    parser = argparse.ArgumentParser(description='Documentation tools - export & convert images')
    parser.add_argument('-v', '--verbose', help='to be more verbose', action='store_true')
    parser.add_argument('-pd', '--projectdir', help='set project explicitly')
    parser.add_argument('--archi', help='export images from archimate tool', action='store_true')
    parser.add_argument('--svg', help='svg -> png', action='store_true')
    parser.add_argument('--umlet', help='umlet -> png', action='store_true')
    parser.add_argument('--mm', help='mermaid -> png', action='store_true')

    args = parser.parse_args()
    args = docool.add_project(args)

    return args

if __name__ == '__main__':
    args = parse_args()
    if args.archi:
        docool.log(args, 'archi')
        export_archi(args)
        docool.log(args, 'archi', 'done')
    if args.svg:
        docool.log(args, 'svg')
        convert_svg(args)
        docool.log(args, 'svg', 'done')
