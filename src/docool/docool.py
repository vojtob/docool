import os
import shutil
from pathlib import Path
import argparse
import subprocess

def log(args, function, message='start'):
    message_format = 'docool({args.projectname}): {message} {function}'
    if hasattr(args, 'file') and args.file is not None:
        message_format = message_format + ' for file {args.file}'
    print(message_format.format(args=args, message=message.upper(), function=function))

def add_project(args):
    if args.projectdir is None:
        args.projectdir = Path.cwd().parent
    else:
        args.projectdir = Path(args.project)
    args.projectname = args.projectdir.stem
    args.docoolpath = Path(__file__).parent.parent.parent

    if args.verbose:
        print('project dir: {0}'.format(args.projectdir))
        print('project name: {0}'.format(args.projectname))
        print('docool path: {0}'.format(args.docoolpath))

    return args

def documentation(args):
    pass
    
def configure_args():
    parser = argparse.ArgumentParser(description='Documentation tools')
    parser.add_argument('project', help='path to project')
    parser.add_argument('-v', '--verbose', help='to be more verbose', action='store_true')
    subparsers = parser.add_subparsers(title='commands', description='available commands')

    # spec
    parser_areas = subparsers.add_parser('doc', help='generate documentation')
    parser_areas.add_argument('-f', '--folder', help='process this folder', default='specification')
    parser_areas.add_argument('-u', '--update', help='update only', action='store_true')
    parser_areas.add_argument('--word', help='export to word', action='store_true')
    parser_areas.add_argument('--web', help='export for web', action='store_true')
    parser_areas.set_defaults(func=documentation)

    return parser

if __name__ == '__main__':
    parser = configure_args()
    args = parser.parse_args()
    args.project_name = os.path.split(args.project)[1].upper()
    # log(args)
    if hasattr(args, 'func'):
        args.func(args)
    log(args, 'done')
