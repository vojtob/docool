import re
from pathlib import Path

def __anchorname(element):
    return element.type[len('archimate:'):] + '_' + re.compile('[^a-z0-9]').sub('', element.name.lower())

def __anchorpath(pagepath):
    return pagepath

def deleteanchors(args):
    anchorfile = args.projectdir / 'temp' / 'anchors.txt'
    if anchorfile.exists():
        anchorfile.unlink()

def saveanchor(args, element, pagepath):
    """save anchor into file"""
    aname = __anchorname(element)
    apath = __anchorpath(pagepath)
    # apath = 'aaa'
    if apath.endswith('.md'):
        apath = apath[:-len('.md')]
    if apath.endswith('_index'):
        apath = apath[:-len('_index')]
    apath = str(Path(apath.lower()).as_posix())
    anchorfile = args.projectdir / 'temp' / 'anchors.txt'

    with open(anchorfile, 'a', encoding='utf8') as fout:
        fout.write('{0} -> {1}\n'.format(aname, apath))
    return '<a name="{0}"></a>'.format(aname)

def getanchor(args, element):
    """get anchor from file"""
    aname = __anchorname(element)
    anchorfile = args.projectdir / 'temp' / 'anchors.txt'

    with open(anchorfile, 'r', encoding='utf8') as fin:
        for line in fin:
            a = line.split(' -> ') 
            if a[0] == aname:
                # return a[1][:-1]+'#'+a[0]
                return '{{{{< ref "{0}#{1}" >}}}}'.format(a[1][:-1], a[0])

    return ''