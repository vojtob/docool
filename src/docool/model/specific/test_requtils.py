import unittest
from types import SimpleNamespace
from pathlib import Path
import requtils

class TestRequirements(unittest.TestCase):

    def test_generate(self):
        generated = requtils.generate_requirements(2, 3, 4)
        check = [
            '"ID-req-P2-03-01";"Requirement";"P2.03.01";""\n',
            '"ID-req-P2-03-02";"Requirement";"P2.03.02";""\n',
            '"ID-req-P2-03-03";"Requirement";"P2.03.03";""\n',
            '"ID-req-P2-03-04";"Requirement";"P2.03.04";""\n',
            ]
        self.assertEqual(generated, check)


if __name__ == '__main__':
    unittest.main()
