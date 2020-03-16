import sys
import os
import unidecode

import model_processing as mp
import model_formatting as mf


def onepage(projectdir):
    processor = mp.ArchiFileProcessor(projectdir)
    foldername = '05. Opis  projektu  nového IS CPP'
    headerlevel = 2

    mdpath =  os.path.join(projectdir, 'temp', 'spec_local', 'content', '10-Requirements', '_index.md')       
    with open(mdpath, 'a', encoding='utf8') as fout:
        fout.write('\n')
        # top folder header
        fout.write('{headertag} {name}\n'.format(headertag=headerlevel*'#', name=foldername))
        # iterate over folders and add them as subchapters
        for f in processor.get_folders(foldername):
            # subfolder header
            fout.write('{headertag} {name}\n'.format(headertag=(headerlevel+1)*'#', name=f))
            # all requirements in folder as a one table
            fout.writelines('\n'.join(mf.requirements_as_table(processor.get_requirements(f))))

def page4chapter(projectdir):
    processor = mp.ArchiFileProcessor(projectdir)
    foldername = 'Requirements'
    weight = 1
    for sectionfolder in processor.get_folders(foldername):
        weight = weight+1
        # create folder for a section
        sectionname = unidecode.unidecode('{0}.md'.format(sectionfolder.replace('.','-').replace(' ','-')))
        sectionpath =  os.path.join(projectdir, 'temp', 'spec_local', 'content', '10-Requirements', sectionname)
        if not os.path.exists(sectionpath):
            os.makedirs(sectionpath)
        # create index file
        indexpath =  os.path.join(sectionpath, '_index.md')
        with open(indexpath, 'w', encoding='utf8') as fout:
            fout.write('---\n')
            fout.write('title: "{0}"\n'.format(sectionfolder))
            fout.write('weight: {0}\n'.format(weight))
            fout.write('---\n')
            fout.write('\n\n')

        # process subfolder for chapter
        subweight = 1
        for chapterfolder in processor.get_folders(sectionfolder):
            # create page for folder
            subweight = subweight+1
            chaptername = unidecode.unidecode('{0}.md'.format(chapterfolder.replace('.','-').replace(' ','-')))
            chapterpath =  os.path.join(sectionpath, chaptername)
            with open(chapterpath, 'w', encoding='utf8') as fout:
                fout.write('---\n')
                fout.write('title: "{0}"\n'.format(chapterfolder))
                fout.write('weight: {0}\n'.format(subweight))
                fout.write('---\n')
                fout.write('\n\n')
                # insert table with requirements
                fout.writelines('\n'.join(mf.requirements_as_table(processor.get_requirements(chapterfolder))))

def page4chapter_separatedreqs(projectdir):
    processor = mp.ArchiFileProcessor(projectdir)
    foldername = 'Requirements'
    weight = 1
    for sectionfolder in sorted(processor.get_folders(foldername)):
        weight = weight+1
        # create folder for a section
        sectionname = unidecode.unidecode('{0}.md'.format(sectionfolder.replace('.','-').replace(' ','-')))
        sectionpath =  os.path.join(projectdir, 'temp', 'spec_local', 'content', '10-Requirements', sectionname)
        if not os.path.exists(sectionpath):
            os.makedirs(sectionpath)
        # create index file
        indexpath =  os.path.join(sectionpath, '_index.md')
        with open(indexpath, 'w', encoding='utf8') as fout:
            fout.write('---\n')
            fout.write('title: "{0}"\n'.format(sectionfolder))
            fout.write('weight: {0}\n'.format(weight))
            fout.write('---\n\n')
            fout.write('{{% children  %}}\n')

        # process subfolder for chapter
        subweight = 1
        for chapterfolder in sorted(processor.get_folders(sectionfolder)):
            # create page for folder
            subweight = subweight+1
            chaptername = unidecode.unidecode('{0}.md'.format(chapterfolder.replace('.','-').replace(' ','-')))
            chapterpath =  os.path.join(sectionpath, chaptername)
            with open(chapterpath, 'w', encoding='utf8') as fout:
                fout.write('---\n')
                fout.write('title: "{0}"\n'.format(chapterfolder))
                fout.write('weight: {0}\n'.format(subweight))
                fout.write('---\n\n\n')
                # process requirements
                for r in processor.get_requirements(chapterfolder):
                    # req header
                    fout.write('{headertag} {name}\n\n'.format(headertag=4*'#', name=r.name))
                    fout.writelines('\n'.join(mf.requirement_as_text(r)))

    
if __name__ == '__main__':
    # read project dir from arguments
    if (len(sys.argv) < 2):
        print('usage: process_requirements.py projectPath')
        # exit(1)
        projectdir = 'C:\\Projects_src\\Work\\MoJ\\cpp'
    else:
        projectdir = os.path.normpath(sys.argv[1])

    # onepage(projectdir)
    # page4chapter(projectdir)
    page4chapter_separatedreqs(projectdir)

    print('requirements processing DONE')