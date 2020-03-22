import sys
import fileinput

# print('Number of arguments:', len(sys.argv), 'arguments.')
# print('Argument List:', str(sys.argv))

if (len(sys.argv) < 5):
    print('usage: replace.py inFileName outFile text_to_search replacement_text')
else:
    inFile = sys.argv[1]
    outFile = sys.argv[2]
    text_to_search = sys.argv[3]
    replacement_text = sys.argv[4]
    with open(inFile, mode="r", encoding="utf-8") as fin:
        with open(outFile, mode="w", encoding='utf-8') as fout:
            for line in fin:
                fout.write(line.replace(text_to_search, replacement_text))
    print ("replace done")
