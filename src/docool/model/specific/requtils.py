import sys
import fileinput

def generate_requirements(chapter, subchapter, reqcount):
    reqID_format = 'ID-req-P{chapter:0>1}-{subchapter:0>2}-{reqOrder:0>2}'
    reqname_format = 'P{chapter:0>1}.{subchapter:0>2}.{reqOrder:0>2}'
    reqline_format = '"{reqID}";"Requirement";"{reqname}";""\n'

    requirements = []
    for c in range(1, reqcount+1):
        reqID = reqID_format.format(chapter=chapter, subchapter=subchapter, reqOrder=c)
        reqname = reqname_format.format(chapter=chapter, subchapter=subchapter, reqOrder=c)
        requirements.append(reqline_format.format(reqID=reqID, reqname=reqname))
    return requirements

def generate_chapter(chapter, listofsizes):
    r = []
    for i,s in enumerate(listofsizes):
        r.extend(generate_requirements(chapter, 1+i, s))
    return r

if __name__ == "__main__":
    outfile_elements_name = 'C:/Projects_src/Work/temp/reqelements.csv'
    r = generate_chapter(8, [8, 12, 13, 1])
    # requirements9 = generate_requirements(9, 1, 1)
    # r.extend(requirements9)
    with open(outfile_elements_name, mode="w", encoding='utf-8') as outfile_elements:
        outfile_elements.writelines(r)
    print('DONE: requirements file {0} generated'.format(outfile_elements_name))
