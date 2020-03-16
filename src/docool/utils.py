from pathlib import Path
import argparse

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