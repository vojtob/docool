import shutil
import subprocess
from pathlib import Path

def getlocalpath(args):
    return args.projectdir / 'temp' / (args.name+'_local')

def getonepagepath(args):
    return args.projectdir / 'temp' / (args.name+'_onepage')

def build_site(args):
    if args.verbose:
        print('build site')

    localpath = getlocalpath(args)
    # clean
    if args.verbose:
        print('clean ', str(localpath))
    shutil.rmtree(localpath, ignore_errors=True)
    
    # create hugo site
    cmd = 'hugo new site {0}'.format(str(localpath))
    if args.debug:
        print(cmd)
    subprocess.run(cmd, shell=False)
    
    # setup themes
    if args.verbose:
        print('setup theme')
    with open(args.docoolpath / 'res' / 'themes' / 'config.toml', 'r', encoding='utf8') as fin:
        with open(localpath/'config.toml', 'w', encoding='utf8') as fout:
            for line in fin:
                if line.startswith('title'):
                    fout.write('title = "{0}"\n'.format(args.projectname))
                else:
                    fout.write(line)

def export_onepage(args):
    # create hugo site with one single page
    if args.verbose:
        print('create hugo site with one single page')
    onepagepath = getonepagepath(args)
    shutil.rmtree(onepagepath, ignore_errors=True)
    onepagepath.mkdir(parents=True, exist_ok=True)
    ''' hugo parameters 
        -D, --buildDrafts
        -s, --source string
        -d, --destination string
        -t, --theme strings
        -b, --baseURL string         hostname (and path) to the root
    '''
    cmd = 'hugo -D -s "{sourcepath}" -d "{destinationpath}" --themesDir {themespath} -t onePageHtml -b "{sitepath}"'.format(
        sourcepath=getlocalpath(args), destinationpath=onepagepath, themespath=str(args.docoolpath/'res'/'themes'), sitepath=onepagepath)
    if args.debug:
        print(cmd)
    subprocess.run(cmd, shell=False)