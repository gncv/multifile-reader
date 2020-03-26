"""File like object that reads multiple files as if they are one file."""
import os
from .utils import get_online_file_size, get_streamed_online_file, is_url


# pylint: disable=R0205
class MultiFileReader(object):
    """File-like object that reads multi-files as if they are one file.

    Args:
        files (list): list of local file paths or urls
        request_headers (dict): headers used when fetching online files
    """

    def __init__(self, files, request_headers=None):
        if isinstance(files, str):
            self._files = (files,)
        else:
            self._files = files

        self._request_headers = request_headers
        self._file = None
        self._url = None
        self._file_idx = 0
        self._map_sizes = self._get_map_sizes()
        self._read_files_offset = {file_path: 0 for file_path in self._files}

    def __del__(self):
        self.close()

    def __enter__(self):
        return self

    def __exit__(self, *args, **kwargs):
        self.close()

    def __iter__(self):  # pylint: disable=E0301
        return self

    def _get_map_sizes(self):
        """Get size of each file.

        Returns:
            dict: file path as key, file size in bytes as value
        """
        file_sizes = {}

        for file_path in self._files:
            if is_url(file_path):
                file_sizes[file_path] = get_online_file_size(
                    file_path, self._request_headers
                )
            else:
                file_sizes[file_path] = os.path.getsize(file_path)

        return file_sizes

    def close(self):
        """Close file and clear state."""
        if self._file:
            self._file.close()
            self._file = None
            self._file_idx = 0

    def nextfile(self):
        """Get next file if there is one and set it to self._file attribute."""
        prev_file = self._file
        self._file = None
        if prev_file:
            prev_file.close()
            self._file_idx += 1

        try:
            current_file_path = self._files[self._file_idx]
            if is_url(current_file_path):
                self._url = current_file_path
                self._file = get_streamed_online_file(current_file_path, self._request_headers)
            else:
                self._url = None
                self._file = open(current_file_path, "rb")
        except IndexError:
            pass

    @property
    def filename(self):
        """Returns filename of the current file.

        Returns:
            str: for local files this is full local path, for online files it
                 is the original url
        """
        if self._url:
            return self._url
        else:
            return self._file.name

    def fileno(self):
        """Returns fileno of the current file."""
        if self._file:
            try:
                return self._file.fileno()
            except ValueError:
                return -1
        else:
            return -1

    def get_size(self):
        """Returns combined size of all files provided.

        Returns:
            int: size of all files provided in bytes
        """
        return sum(self._map_sizes.values())

    def read(self, size=None):
        """Read a chunk of the file.

        If the size is not provided, will read all files at once.

        Args:
            size (int): number of bytes to read

        Returns:
            bytes: the chunk
        """
        if not size:
            size = self.get_size()

        buf = b""
        while size > 0:
            if not self._file and self._file_idx == len(self._files):
                break

            # pylint: disable=C0330
            if (
                not self._file
                or self._read_files_offset[self.filename]
                == self._map_sizes[self.filename]
            ):
                self.nextfile()
                continue

            chunk = self._read(size)
            buf += chunk
            size -= len(chunk)
        return buf

    def _read(self, size):
        unread = (
            self._map_sizes[self.filename]
            - self._read_files_offset[self.filename]
        )
        length = min(size, unread)

        if self._url:
            buf = self._file.read()
        else:
            self._file.seek(self._read_files_offset[self.filename])
            buf = self._file.read(length)

        self._read_files_offset[self.filename] += length
        return buf
