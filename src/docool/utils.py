import os
import shutil
from pathlib import Path

def mycopy(source_directory, destination_directory, debug=False):
    if debug:
        print('copy {0} -> {1}'.format(str(source_directory), str(destination_directory)))
    # walk over files in from directory
    for (dirpath, _, filenames) in os.walk(source_directory):
        # create destination directory
        d = Path(dirpath.replace(str(source_directory), str(destination_directory)))
        d.mkdir(parents=True, exist_ok=True)
        
        # convert files with specific extension
        for f in filenames:
            sourcefile = Path(dirpath, f)
            destfile = str(sourcefile).replace(str(source_directory), str(destination_directory))
            shutil.copy(str(sourcefile), destfile)


