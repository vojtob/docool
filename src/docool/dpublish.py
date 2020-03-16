import os
import pathlib
import argparse
import subprocess

from pathlib import PureWindowsPath, Path
import docool

def publish_images(args):
    # publish images to release dir
    imgspath = args.

def parse_args():
    parser = argparse.ArgumentParser(description='Documentation tools - publish')
    parser.add_argument('-v', '--verbose', help='to be more verbose', action='store_true')
    parser.add_argument('-pd', '--projectdir', help='set project explicitly')
    parser.add_argument('-i', '--images', help='publish images', action='store_true')
    parser.add_argument('-u', '--update', help='update only', action='store_true')
    parser.add_argument('--word', help='export to word', action='store_true')
    parser.add_argument('--web', help='export for web', action='store_true')

    args = parser.parse_args()
    args = docool.add_project(args)

    return args

if __name__ == '__main__':
    args = parse_args()
    if args.images:
        docool.log(args, 'publish images')
        publish_images(args)
        docool.log(args, 'publish images', 'done')
