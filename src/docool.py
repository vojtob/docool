import argparse
from pathlib import Path

from docool import clean, dimg, decorate, dpublish, dspec

def log(args, message='start'):
    message_format = '{args.projectname}: {message} {args.command}'
    if hasattr(args, 'file') and args.file is not None:
        message_format = message_format + ' for file {args.file}'
    print(message_format.format(args=args, message=message.upper()))

def __add_project(args):
    if args.projectdir is None:
        args.projectdir = Path.cwd().parent
    else:
        args.projectdir = Path(args.project)
    args.projectname = args.projectdir.stem
    args.docoolpath = Path(__file__).parent.parent

    if args.verbose:
        print('{args.projectname}: {args.projectdir}'.format(args=args))
    if args.debug:
        print('docool path: {0}'.format(args.docoolpath))

    return args

if __name__ == '__main__':
    print('docool: START\n')

    parser = argparse.ArgumentParser(prog='docool', description='Documentation tools')
    parser.add_argument('-pd', '--projectdir', help='set project explicitly')
    parser.add_argument('-v', '--verbose', help='to be more verbose', action='store_true')
    parser.add_argument('-d', '--debug', help='add debug info, very low level', action='store_true')
    subparsers = parser.add_subparsers(help='command help')

    parser_clean = subparsers.add_parser('clean', help='clean all generated files and folders')
    # parser_clean.add_argument('-v', '--verbose', help='to be more verbose', action='store_true')
    # parser_clean.add_argument('-d', '--debug', help='add debug info, very low level', action='store_true')
    parser_clean.set_defaults(command='clean')

    parser_img = subparsers.add_parser('img', help='export & convert images')
    # parser_img.add_argument('-v', '--verbose', help='to be more verbose', action='store_true')
    # parser_img.add_argument('-d', '--debug', help='add debug info, very low level', action='store_true')
    parser_img.add_argument('-a', '--all', help='export images from archimate tool', action='store_true')
    parser_img.add_argument('--archi', help='export images from archimate tool', action='store_true')
    parser_img.add_argument('--svg', help='svg -> png', action='store_true')
    # parser_img.add_argument('--umlet', help='umlet -> png', action='store_true')
    # parser_img.add_argument('--mm', help='mermaid -> png', action='store_true')
    parser_img.set_defaults(command='dimg')

    parser_decorate = subparsers.add_parser('decorate', help='decorate images')
    # parser_decorate.add_argument('-v', '--verbose', help='to be more verbose', action='store_true')
    # parser_decorate.add_argument('-d', '--debug', help='add debug info, very low level', action='store_true')
    parser_decorate.add_argument('-a', '--all', help='add icons and areas to images', action='store_true')
    parser_decorate.add_argument('--icons', help='add icons to images based on src/docs/img/images.json', action='store_true')
    parser_decorate.add_argument('--areas', help='create image with focused area based on src/docs/img/img_focus.json', action='store_true')
    parser_decorate.add_argument('-f', '--file', help='process only this one file')
    parser_decorate.set_defaults(command='decorate')

    parser_spec = subparsers.add_parser('spec', help='create specification')
    # parser_spec.add_argument('-v', '--verbose', help='to be more verbose', action='store_true')
    # parser_spec.add_argument('-d', '--debug', help='add debug info, very low level', action='store_true')
    parser_spec.add_argument('-a', '--all', help='clean, build and generate specification', action='store_true')
    parser_spec.add_argument('-b', '--build', help='clean and build hugo site', action='store_true')
    parser_spec.add_argument('-c', '--content', help='copy and enrich content', action='store_true')
    parser_spec.add_argument('-req', '--requirements', help='generate requirements', action='store_true')
    parser_spec.set_defaults(command='spec')

    parser_publish = subparsers.add_parser('publish', help='publish images, specification as word')
    # parser_publish.add_argument('-v', '--verbose', help='to be more verbose', action='store_true')
    # parser_publish.add_argument('-d', '--debug', help='add debug info, very low level', action='store_true')
    parser_publish.add_argument('-i', '--images', help='publish images', action='store_true')
    parser_publish.add_argument('--doc', help='export to word document', action='store_true')
    # parser_publish.add_argument('-w', '--web', help='export for web', action='store_true')
    parser_publish.set_defaults(command='publish')

    args = parser.parse_args()
    args = __add_project(args)

    if args.command=='clean':
        log(args)
        clean.doit(args)
        log(args, 'done')

    if args.command=='dimg':
        log(args)
        dimg.doit(args)
        log(args, 'done')

    if args.command=='decorate':
        log(args)
        decorate.doit(args)
        log(args, 'done')

    if args.command=='publish':
        log(args)
        dpublish.doit(args)
        log(args, 'done')

    if args.command=='spec':
        log(args)
        dspec.doit(args)
        log(args, 'done')

    print('\ndocool: DONE')


