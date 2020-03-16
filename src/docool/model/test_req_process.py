import unittest
import model_processing as mp
import model_formatting as mf

class TestReqProcessing(unittest.TestCase):

    def test_folders(self):
        projectdir = 'C:\\Projects_src\\Work\\MoJ\\cpp'
        modelprocessor = mp.ArchiFileProcessor(projectdir)
        foldername = '05. Opis  projektu  nového IS CPP'
        folders = modelprocessor.get_folders(foldername)
        self.assertEqual(len(folders), 25)        
    
    def test_reqfolder(self):
        projectdir = 'C:\\Projects_src\\Work\\MoJ\\cpp'
        modelprocessor = mp.ArchiFileProcessor(projectdir)
        foldername = '5.01. Kľúčové ukazovatele projektu'
        reqs = modelprocessor.get_requirements(foldername)

        self.assertEqual(4, len(reqs))
        self.assertEqual('P5.01.01 Modulárny systém', reqs[0].name)
        self.assertEqual('P5.01.04 Vytvorenie návrhov', reqs[3].name)
        self.assertEqual(len(reqs[0].realizations), 1)
        self.assertEqual(len(reqs[1].realizations), 5)
        self.assertEqual(len(reqs[2].realizations), 1)
        self.assertEqual(len(reqs[3].realizations), 0)


if __name__ == '__main__':
    unittest.main()
