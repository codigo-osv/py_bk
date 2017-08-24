import funciones
import os
import subprocess
import unittest


class TestBack(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        subprocess.call(["mkdir", "testdir", "testdir2", "testdir3"])
        subprocess.call(["touch", "testdir2/testfile"])
        subprocess.call(['touch', '-m', '-d', "8 days ago", 'testdir3/testfile'''])

    def test_empty_dir(self):
        res = funciones.older_than("testdir/", 666)
        self.assertFalse(res)

    def test_no_older_files(self):
        res = funciones.older_than("testdir2/", 666)
        self.assertFalse(res)

    def test_older_files(self):
        res = funciones.older_than("testdir3/", 7)
        self.assertEqual(res, ["testdir3/testfile"])

    @classmethod
    def tearDownClass(self):
        subprocess.call(["rm", "-rf", "testdir", "testdir2", "testdir3"])