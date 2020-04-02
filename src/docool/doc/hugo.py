import shutil
import subprocess
from pathlib import Path

def get_generated_path(args):
    return args.projectdir / 'temp' / (args.name+'_generated')

# def get_content_path(args):
#     return args.projectdir / 'temp' / (args.name+'_content')

def get_local_path(args):
    return args.projectdir / 'temp' / (args.name+'_local')

def build_site(args):
    if args.verbose:
        print('build specification')

    pgenerated = get_generated_path(args)
    plocal = get_local_path(args)

    # clean
    if args.verbose:
        print('clean ', str(plocal))
    shutil.rmtree(pgenerated, ignore_errors=True)
    shutil.rmtree(plocal, ignore_errors=True)
    
    # create hugo site
    cmd = 'hugo new site {0}'.format(str(plocal))
    if args.debug:
        print(cmd)
    subprocess.run(cmd, shell=False)
    
    # setup themes
    if args.verbose:
        print('setup theme')
    with open(args.docoolpath / 'res' / 'themes' / 'config.toml', 'r', encoding='utf8') as fin:
        with open(plocal/'config.toml', 'w', encoding='utf8') as fout:
            for line in fin:
                if line.startswith('title'):
                    fout.write('title = "{0}"\n'.format(args.projectname))
                else:
                    fout.write(line)
    # shutil.copy(args.projectdir/'src'/'res'/'hugo-config'/'configNoTheme.toml', hugodir/'config.toml')

