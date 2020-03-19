import unidecode
from pathlib import Path

import docool.model.model_processing as mp
import docool.model.model_formatting as mf

HUGO_FRONTMATTER = '---\ntitle: "{title}"\nweight: {weight}\n---\n\n\n'
MD_HEADER = '\n{headertag} {name}\n'

def onepage(projectdir):
    processor = mp.ArchiFileProcessor(projectdir)
    foldername = '05. Opis  projektu  nového IS CPP'
    headerlevel = 2

    mdpath = projectdir/'temp'/'spec_local'/'content'/'10-Requirements'/'_index.md'
    with open(mdpath, 'a', encoding='utf8') as fout:
        fout.write('\n')
        # top folder header
        fout.write(MD_HEADER.format(headertag=headerlevel*'#', name=foldername))
        # iterate over folders and add them as subchapters
        for f in processor.get_folders(foldername):
            # subfolder header
            fout.write(MD_HEADER.format(headertag=(headerlevel+1)*'#', name=f))
            # all requirements in folder as a one table
            fout.writelines('\n'.join(mf.requirements_as_table(processor.get_requirements(f))))

def page4chapter(args):
    processor = mp.ArchiFileProcessor(args.projectdir)
    foldername = 'Requirements'
    weight = 1
    for sectionfolder in processor.get_folders(foldername):
        weight = weight+1
        # create folder for a section
        if args.debug:
            print('create section', sectionfolder)
        sectionname = unidecode.unidecode('{0}.md'.format(sectionfolder.replace('.','-').replace(' ','-')))
        sectionpath = args.projectdir / 'temp' / 'spec_local' / 'content' / '10-Requirements' / sectionname
        sectionpath.mkdir(parents=True, exist_ok=True)
        # create index file
        indexpath =  sectionpath / '_index.md'
        with open(indexpath, 'w', encoding='utf8') as fout:
            HUGO_FRONTMATTER.format(title=sectionfolder, weight=weight)

        # process subfolder for chapter
        subweight = 1
        for chapterfolder in processor.get_folders(sectionfolder):
            # create page for folder
            if args.debug:
                print('    create chapter', chapterfolder)
            subweight = subweight+1
            chaptername = unidecode.unidecode('{0}.md'.format(chapterfolder.replace('.','-').replace(' ','-')))
            chapterpath =  sectionpath / chaptername
            with open(chapterpath, 'w', encoding='utf8') as fout:
                HUGO_FRONTMATTER.format(title=chapterfolder, weight=subweight)
                # insert table with requirements
                fout.writelines('\n'.join(mf.requirements_as_table(processor.get_requirements(chapterfolder))))

def page4chapter_separatedreqs(args):
    processor = mp.ArchiFileProcessor(args.projectdir)
    foldername = 'Requirements'
    weight = 1
    for sectionfolder in sorted(processor.get_folders(foldername)):
        weight = weight+1
        # create folder for a section
        if args.debug:
            print('create section', sectionfolder)
        sectionname = unidecode.unidecode('{0}.md'.format(sectionfolder.replace('.','-').replace(' ','-')))
        sectionpath =  args.projectdir / 'temp' / 'spec_local' / 'content' / '10-Requirements' / sectionname
        sectionpath.mkdir(parents=True, exist_ok=True)
        indexpath =  sectionpath / '_index.md'
        with open(indexpath, 'w', encoding='utf8') as fout:
            HUGO_FRONTMATTER.format(title=sectionfolder, weight=weight)
        # process subfolder for chapter
        subweight = 1
        for chapterfolder in sorted(processor.get_folders(sectionfolder)):
            # create page for folder
            if args.debug:
                print('  create chapter', chapterfolder)
            subweight = subweight+1
            chaptername = unidecode.unidecode('{0}.md'.format(chapterfolder.replace('.','-').replace(' ','-')))
            chapterpath =  sectionpath / chaptername
            with open(chapterpath, 'w', encoding='utf8') as fout:
                HUGO_FRONTMATTER.format(title=chapterfolder, weight=subweight)
                # process requirements
                for r in processor.get_requirements(chapterfolder):
                    # req header
                    if args.debug:
                        print('    process requirement', r.name)
                    # requirement header
                    fout.write(MD_HEADER.format(headertag=4*'#', name=r.name))
                    # requirement realization
                    if len(r.realizations) == 0:
                        fout.write('<font color="red">XXXXXX TODO: Ziadna realizacia poziadavky</font>\n\n')
                    else:
                        realization_format_string = '**{realization_name}:** {realization_description}\n\n'
                        for realization in r.realizations:
                            fout.write(realization_format_string.format(realization_name=realization.name, realization_description=realization.get_desc()))

                    