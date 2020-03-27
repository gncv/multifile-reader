"""Tests for multifile reader object."""
from multifile_reader.multifile_reader import MultiFileReader

from pyfakefs.fake_filesystem_unittest import TestCase


class MultiFileReaderTestCase(TestCase):
    """MultiFileReader test case."""

    def setUp(self):  # pylint: disable=invalid-name
        """Test setup logic."""
        self.setUpPyfakefs()
        self.files = [
            "test_files/foo_1.txt",
            "test_files/foo_2.txt",
            "test_files/foo_3.txt",
        ]
        self.fs.create_file(self.files[0], contents="hello ")
        self.fs.create_file(self.files[1], contents="world")
        self.fs.create_file(self.files[2], contents="!")

    def test_read_no_size_supplied(self):
        """Test that MultiFileReader by default reads all files."""
        with MultiFileReader(self.files) as file_obj:
            content_binary = file_obj.read()
            self.assertEqual(len(content_binary), file_obj.get_size())
            self.assertEqual(content_binary, b"hello world!")

    def test_read_no_size_supplied_without_with(self):
        """Test that MultiFileReader by default reads all files."""
        file_obj = MultiFileReader(self.files)
        content_binary = file_obj.read()
        self.assertEqual(len(content_binary), file_obj.get_size())
        file_obj.close()
        self.assertEqual(content_binary, b"hello world!")

    def test_reader_can_read_one_file_too(self):
        """Test that MultiFileReader can read one file as well."""
        with MultiFileReader(self.files[0]) as file_obj:
            content_binary = file_obj.read()
            self.assertEqual(len(content_binary), file_obj.get_size())
            self.assertEqual(content_binary, b"hello ")

    def test_reader_can_read_in_chunks(self):
        """Test iter read of MultiFileReader."""
        with MultiFileReader(self.files) as file_obj:
            chunk = file_obj.read(1)
            content_binary = chunk
            while chunk:
                chunk = file_obj.read(1)
                content_binary += chunk
            self.assertEqual(len(content_binary), file_obj.get_size())
            self.assertEqual(content_binary, b"hello world!")

    def test_reader_fileno(self):
        """Test that fileno works."""

        with MultiFileReader(self.files) as file_obj:
            self.assertEqual(file_obj.fileno(), -1)
            file_obj.nextfile()
            self.assertGreater(file_obj.fileno(), 2)
