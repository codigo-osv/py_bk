import classes
import funciones
import subprocess
import unittest


class TestBack(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        subprocess.call(["mkdir", "testdir", "testdir2", "testdir3"])
        subprocess.call(["touch", "testdir2/testfile"])
        subprocess.call(['touch', '-m', '-d', "8 days ago", 'testdir3/testfile'])
        subprocess.call(['touch', '-m', '-d', "2 days ago", 'testdir3/testfile1'])
        self.td = classes.TimedDirectory("testdir3")

    def test_empty_dir(self):
        res = funciones.older_than_list("testdir/", 666)
        self.assertFalse(res)

    def test_no_older_files(self):
        res = funciones.older_than_list("testdir2/", 666)
        self.assertFalse(res)

    def test_older_and_newer_files(self):
        res = funciones.older_than_list("testdir3/", 7)
        self.assertEqual(res, ["testdir3/testfile"])

    def test_oldest_files_list(self):
        res = self.td.oldest_files_list(4)
        res1 = self.td.oldest_files_list(1)
        res2 = self.td.oldest_files_list(100)
        self.assertEqual(res, ["testdir3/testfile"])
        self.assertEqual(res1, ["testdir3/testfile", "testdir3/testfile1"])
        self.assertEqual(res2, [])

    def test_newest_file_older_than(self):
        self.assertTrue(self.td.newest_file_older_than(1))
        self.assertFalse(self.td.newest_file_older_than(100))

    @classmethod
    def tearDownClass(self):
        subprocess.call(["rm", "-rf", "testdir", "testdir2", "testdir3"])