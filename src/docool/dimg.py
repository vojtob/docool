import os
import pathlib
import subprocess

from pathlib import PureWindowsPath, Path

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

def __process_images(source_directory, destination_directory, orig_extension, new_extension, command, verbose, debug):
    if verbose:
        print('convert {0}({1}) -> {2}({3})'.format(str(source_directory), orig_extension, str(destination_directory), new_extension))

    # walk over files in from directory
    for (dirpath, _, filenames) in os.walk(source_directory):
        # create destination directory
        d = Path(dirpath.replace(str(source_directory), str(destination_directory)))       
        d.mkdir(parents=True, exist_ok=True)

        # convert files with specific extension
        for f in [f for f in filenames if f.endswith(orig_extension)]:          
            ffrom = os.path.join(dirpath, f)
            # change directory and extension
            fto = ffrom.replace(str(source_directory), str(destination_directory)).replace(orig_extension, new_extension)
            cmd = command.format(srcfile=ffrom, destfile=fto)
            if debug:
                print(cmd)
            subprocess.run(cmd, shell=False)

def convert_svg(args):
    # convert svg files to png files
    __process_images(
        args.projectdir / 'temp' / 'img_exported_svg',
        args.projectdir / 'temp' / 'img_exported',
        '.svg', '.png',
        str(Path(os.environ['IM_HOME'], 'magick')) + ' -density 144 {srcfile} {destfile}',
        args.verbose, args.debug)

def doit(args):
    if args.archi or args.all:
        export_archi(args)
    if args.svg or args.all:
        convert_svg(args)