import shutil
import argparse

import docool

def clean(args):
    for dirname in ['release', 'temp']:
        p = args.projectdir / dirname
        if p.exists():
            shutil.rmtree(p)
            if args.verbose:
                print('delete', p)

def parse_args():
    parser = argparse.ArgumentParser(description='Documentation tools - clean all generated files and folders')
    parser.add_argument('-v', '--verbose', help='to be more verbose', action='store_true')
    parser.add_argument('-pd', '--projectdir', help='set project explicitly')

    args = parser.parse_args()
    args = docool.add_project(args)

    return args

if __name__ == '__main__':
    args = parse_args()
    docool.log(args, 'clean')
    clean(args)
    docool.log(args, 'clean', 'done')
