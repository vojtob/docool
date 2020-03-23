import sys
import fileinput

def realize_requirements(chapter, count, reqID):
    with open(outfile_relations_name, mode="w", encoding='utf-8') as outfile_relations:
        outfile_relations.write('"ID";"Type";"Name";"Documentation";"Source";"Target"\n')
        for idAss in range(count):
            outfile_relations.write('"";"RealizationRelationship";"";"";"{reqID}";"ID-req-P5-{chapter:0>2}-{idAss:0>2}"\n'.format(chapter=chapter,idAss=idAss+1,reqID=reqID))
    print("assesment generation DONE")

outfile_relations_name = 'C:/Projects_src/Work/MoJ/cpp/temp/reqrelations.csv'

realize_requirements(6,8, '4400f733-12fe-46ee-b82d-7d9adbb21073')