MultiFile Reader
----------------

**Supported Python versions:** 2.7+, 3.7+

This module implements a helper class to quickly read multiple files in sequence
and treat them as if they are one file.

Especially useful in reading big files, which are split into multiple parts, such as FASTQ files.

Files are open and read in binary mode.


Installation
------------

.. code:: sh

    pip install multifile-reader


Example Usage
-------------

Then in your code:

.. code:: python

    from multifile_reader import MultiFileReader

    with MultiFileReader(files) as file_obj:
        content_binary = file_obj.read()


``files`` can be list or tuple.

Or to read big files in chunks:

.. code:: python

    from multifile_reader import MultiFileReader

    with MultiFileReader(files) as file_obj:
        chunk = file_obj.read(1)
        content_binary = chunk
        while chunk:
            chunk = file_obj.read(1)
            content_binary += chunk
            # or do something else with the chunk


Contributors
------------

Gencove_

.. _Gencove: https://gencove.com/
