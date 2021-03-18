import shutil
import subprocess
from pathlib import Path

def build_site(args):
    # clean
    if args.verbose:
        print('clean ', str(args.localpath))
    shutil.rmtree(args.localpath, ignore_errors=True)
    
    # create hugo site
    cmd = 'hugo new site {0}'.format(str(args.localpath))
    if args.debug:
        print(cmd)
    subprocess.run(cmd, shell=False)
    
    # setup themes
    if args.verbose:
        print('setup theme')
    with open(args.docoolpath / 'res' / 'themes' / 'config.toml', 'r', encoding='utf8') as fin:
        with open(args.localpath/'config.toml', 'w', encoding='utf8') as fout:
            for line in fin:
                if line.startswith('title'):
                    fout.write('title = "{0}"\n'.format(args.projectname))
                else:
                    fout.write(line)

    with open(args.docoolpath / 'res' / 'themes' / 'hugo-theme-learn-master' / 'layouts' / 'partials' / 'logo.html', 'r', encoding='utf8') as fin:
        (args.localpath / 'layouts' / 'partials').mkdir(parents=True, exist_ok=True)
        with open(args.localpath / 'layouts' / 'partials' / 'logo.html', 'w', encoding='utf8') as fout:
            for line in fin:
                if line.startswith('SET NAME'):
                    fout.write('{0}\n'.format(args.projectname))
                else:
                    fout.write(line)

def export_onepage(args):
    # create hugo site with one single page
    if args.verbose:
        print('create hugo site with one single page')
    shutil.rmtree(args.onepagepath, ignore_errors=True)
    args.onepagepath.mkdir(parents=True, exist_ok=True)
    ''' hugo parameters 
        -D, --buildDrafts
        -s, --source string
        -d, --destination string
        -t, --theme strings
        -b, --baseURL string         hostname (and path) to the root
    '''
    cmd = 'hugo -D -s "{sourcepath}" -d "{destinationpath}" --themesDir {themespath} -t onePageHtml -b "{sitepath}"'.format(
        sourcepath=args.localpath, destinationpath=args.onepagepath, themespath=str(args.docoolpath/'res'/'themes'), sitepath=args.onepagepath)
    if args.debug:
        print(cmd)
    subprocess.run(cmd, shell=False)