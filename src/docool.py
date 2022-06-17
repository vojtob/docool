import argparse
from pathlib import Path
import shutil

from docool import hugo, utils

# from docool import dimg, dspec, dres

def log(args, message):
    message_format = '{args.projectname}: {message}'
    if hasattr(args, 'file') and args.file is not None:
        message_format = message_format + ' for file {args.file}'
    print(message_format.format(args=args, message=message))

def __add_project(args):
    if args.projectdir is None:
        args.projectdir = Path.cwd().parent
    else:
        args.projectdir = Path(args.projectdir)

    args.localpath = args.projectdir / 'temp' / (args.name+'_local')
    args.onepagepath = args.projectdir / 'temp' / (args.name+'_1_local')
    args.imgsourcedir = args.projectdir / 'temp' / 'img_all'
    args.docsourcedir = args.projectdir / 'src_doc'
    args.projectname = args.projectdir.stem
    args.docoolpath = Path(__file__).parent.parent
    args.problems = []

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
    parser.add_argument('name', help='name of documentation')
    subparsers = parser.add_subparsers(help='command help')

    parser_clean = subparsers.add_parser('clean', help='clean all generated files and folders')
    parser_clean.set_defaults(command='clean')

    parser_site = subparsers.add_parser('site', help='build empty hugo site')
    parser_site.set_defaults(command='site')

    parser_content = subparsers.add_parser('content', help='copy content and images')
    parser_content.set_defaults(command='content')

    parser_word = subparsers.add_parser('word', help='create word from documentation')
    parser_word.set_defaults(command='word')

    # parser_spec = subparsers.add_parser('doc', help='create documentation')
    # parser_spec.add_argument('-u', '--update', help='update specification with new content and images', action='store_true')
    # parser_spec.add_argument('-g', '--generate', help='generate specification and requirements', action='store_true')
    # parser_spec.add_argument('-r', '--requirements', help='generate requirements realizations from model', action='store_true')
    # parser_spec.add_argument('-d', '--doc', help='export to word document', action='store_true')
    # parser_spec.add_argument('-w', '--web', help='export to web', action='store_true')
    # parser_spec.add_argument('-l', '--list', help='list unsolved requirements', action='store_true')

    args = parser.parse_args()
    args = __add_project(args)
    if args.debug:
        args.verbose = True
        print(args)

    if not hasattr(args, 'command'):
        print('NO COMMAND')
    #     args.command = 'all'
    log(args, 'starts with the command ' + args.command)

    if args.command=='clean':
        log(args, 'start cleaning')
        for dirname in [args.localpath, args.onepagepath]:
            p = args.projectdir / dirname
            if p.exists():
                shutil.rmtree(p)
                if args.verbose:
                    print('delete', p)
        log(args, 'done cleaning')

    if (args.command=='site'):
        log(args, 'start building site')
        hugo.build_site(args)
        log(args, 'done building site')
    
    if (args.command=='content'):
        log(args, 'start copy content')
        utils.mycopy(args.imgsourcedir, args. localpath / 'static' / 'img', args)
        utils.mycopy(args.docsourcedir / args.name, args. localpath / 'content', args)
        log(args, 'done copy content')

    if (args.command=='word'):
        log(args, 'start generating word')
        hugo.export_onepage(args)
        # args.problems.append('generating word not implemented')
        utils.generate_word_document(args)
        log(args, 'done generating word')


    if args.problems:
        print('\ndocool: DONE ... with PROBLEMS !!')
        for p in args.problems:
            print('  ', p)
    else:
        print('\ndocool: DONE ... OK')