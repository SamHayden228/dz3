import unittest
import xml.etree.ElementTree as ET
import re
from io import StringIO
import sys
import os
import dz3
import tempfile
class TestDz3(unittest.TestCase):
    def setUp(self):


        self.filepath='C:/Users/vlaso_n8/PycharmProjects/pythonProject/konfig/dz3/konfig.xml'


    def test_prog_1(self):
        with open("konfig.xml", "w", encoding="utf-8") as f:
            f.write("""
            <konfig>
                <program>
                    def AAAAA=1;
                    def BBBBB=@"Это строка";
            
                    def DDDD=#(1 2 @"Это тоже строка" #(1 2));
                    def AAA={A:1,
                    B:2,
                    C:#(1 2)};
                    def IMKMS=?[2 3 AAA[C][1] ^ +]
                </program>
            </konfig>
            """)
        f.close()
        captured_output=dz3.main()


        expected_output = """AAAAA, type <class 'int'>, val 1
BBBBB, type <class 'str'>, val Это строка
DDDD, type <class 'list'>, val [1, 2, 'Это тоже строка', [1, 2]]
AAA, type <class 'dict'>, val {'A': 1, 'B': 2, 'C': [1, 2]}
IMKMS, type <class 'int'>, val 11
"""

        self.assertEqual(captured_output, expected_output)

    def test_prog_2(self):
        with open(self.filepath, "w", encoding="utf-8") as f:
            f.write("""
                <konfig>
                    <program>
                        def AAAAA=1;
                        def BBBBB=@"Это строка";

                        def DDDD=#(1 2 @"Это тоже строка" #(1 2));
                        def AAAAA={A:1,
                        B:2,
                        C:#(1 2)};
                        def IMKMS=?[2 3 AAA[C][1] ^ +]
                    </program>
                </konfig>
                """)
        f.close()
        captured_output = dz3.main()

        expected_output = """Variable is already defined"""
        self.assertEqual(captured_output, expected_output)

    def test_prog_3(self):
        with open(self.filepath, "w", encoding="utf-8") as f:
            f.write("""
                <konfig>
                    <program>
                        def AAAAA=1;
                        def BBBBB=@"Это строка";

                        def DDDD=#(1 2 @"Это тоже строка" #(1 2));
                        AAAAA={A:1,
                        B:2,
                        C:#(1 2)};
                        def IMKMS=?[2 3 AAAAA[C][1] ^ +]
                    </program>
                </konfig>
                """)
        f.close()
        captured_output = dz3.main()

        expected_output = """Type redefinition is not allowed"""
        self.assertEqual(captured_output, expected_output)

if __name__ == "__main__":
    unittest.main()
