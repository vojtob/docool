import os
import shutil
import subprocess
from pathlib import Path

def mycopy(source_directory, destination_directory, args, ingore_dot_folders=True, onfile=None):
    """ copy files from source to destination

    optional parameter onfile is special handling function. If it is not specified (default), then file is
    copied from source to destination directory. If specified, it called for each file with argumentes sourcefilepath,
    destfilepath, debug and must handle copying file or generating or replacing or ...
    """

    if args.debug:
        print('copy {0} -> {1}'.format(str(source_directory), str(destination_directory)))
    # walk over files in from directory
    for (dirpath, dirnames, filenames) in os.walk(source_directory):
        # if debug:
        #     print('copy dirpath:', dirpath, Path(dirpath).name)
        if Path(dirpath).name.startswith('.'):
            # if debug:
            #     print('ignore')
            dirnames.clear()
            continue
        # create destination directory
        d = Path(dirpath.replace(str(source_directory), str(destination_directory)))
        d.mkdir(parents=True, exist_ok=True)
        
        # convert files with specific extension
        for f in filenames:
            sourcefile = Path(dirpath, f)
            destfile = str(sourcefile).replace(str(source_directory), str(destination_directory))
            relativepath = str(sourcefile).replace(str(source_directory), '')
            if onfile is not None:
                onfile(sourcefile, Path(destfile), relativepath, args)
            else:
                shutil.copy(str(sourcefile), destfile)

def generate_word_document(args):
    if args.verbose:
        print('generate word document')
    onepagehtml = args.onepagepath / 'index.html'
    templatepath = args.docoolpath / 'res' / 'custom-reference.docx'

    wordpath = args.projectdir / 'temp' / (args.projectname + '_' + args.name + '.docx')
    wordpath.parent.mkdir(parents=True, exist_ok=True)
    cmd = 'pandoc {mainfile} -f html -t docx -o {outputname} --reference-doc={templatename} --verbose'.format(
        mainfile=str(onepagehtml), outputname=str(wordpath), templatename=str(templatepath))
    if args.debug:
        print(cmd)
    subprocess.run(cmd, shell=False) 
