import unidecode
from pathlib import Path

import docool.model.model_processing as mp
import docool.model.model_formatting as mf

def write_frontmatter(fout, title, weight):
    fout.write('---\ntitle: "{0}"\nweight: {1}\n---\n\n\n'.format(title, weight))

def write_header(fout, title, level):
    fout.write('\n{0} {1}\n'.format(level*'#', title))

def get_mdname(name):
    return unidecode.unidecode('{0}.md'.format(name.replace('.','-').replace(' ','-')))

def generatereqs(args):
    processor = mp.ArchiFileProcessor(args.projectdir)
    foldername = 'Requirements'
    weight = 1
    for sectionfolder in sorted(processor.get_folders(foldername)):
        weight = weight+1
        # create folder for a section
        if args.debug:
            print('create section', sectionfolder)
        sectionname = get_mdname(sectionfolder)
        sectionpath =  args.projectdir / 'temp' / 'spec_local' / 'content' / '10-Requirements' / sectionname
        sectionpath.mkdir(parents=True, exist_ok=True)
        indexpath =  sectionpath / '_index.md'
        with open(indexpath, 'w', encoding='utf8') as fout:
            write_frontmatter(fout, sectionfolder, weight)
            fout.write('{{% children  %}}\n')
        # process subfolder for chapter
        subweight = 1
        for chapterfolder in sorted(processor.get_folders(sectionfolder)):
            # create page for folder
            if args.debug:
                print('  create chapter', chapterfolder)
            subweight = subweight+1
            chaptername = get_mdname(chapterfolder)
            chapterpath =  sectionpath / chaptername
            with open(chapterpath, 'w', encoding='utf8') as fout:
                write_frontmatter(fout, chapterfolder, subweight)
                # process requirements
                for r in processor.get_requirements(chapterfolder):
                    # req header
                    if args.debug:
                        print('    process requirement', r.name)
                    # requirement header
                    write_header(fout, r.name, 4)
                    # requirement realization
                    if len(r.realizations) == 0:
                        fout.write('<font color="red">XXXXXX TODO: Ziadna realizacia poziadavky</font>\n\n')
                    else:
                        realization_format_string = '**{realization_name}:** {realization_description}\n\n'
                        product_format_string = '{realization_description}\n\n'
                        for realization in r.realizations:
                            if(mp.ArchiFileProcessor.isproduct(realization.type)):
                                fout.write(product_format_string.format(realization_description=realization.get_desc()))
                            else:
                                fout.write(realization_format_string.format(realization_name=realization.name, realization_description=realization.get_desc()))