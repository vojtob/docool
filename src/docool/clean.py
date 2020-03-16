import shutil
import argparse

def doit(args):
    for dirname in ['release', 'temp']:
        p = args.projectdir / dirname
        if p.exists():
            shutil.rmtree(p)
            if args.verbose:
                print('delete', p)