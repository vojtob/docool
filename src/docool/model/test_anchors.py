import unittest
from types import SimpleNamespace
from pathlib import Path
# import docool.model.anchors as anchors
import anchors

class TestAnchors(unittest.TestCase):

    def test_get(self):
        args = SimpleNamespace(projectdir = Path('C:\\Projects_src\\Work\\MoJ\\cpp\\'))
        element = SimpleNamespace(name = 'Poskytovanie predbežnej konzultácie', type = 'archimate:BusinessService')
        a = anchors.getanchor(args, element)

        self.assertEqual(a, '/02-business_architecture/sluzby#BusinessService_poskytovaniepredbenejkonzultcie')        
    

if __name__ == '__main__':
    unittest.main()
