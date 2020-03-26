from urllib.parse import urlparse

import requests

from .exceptions import MultiFileReaderException


def is_url(url):
    """Check if given string is a valid url or not.

    Args:
        url (str): string to check

    Returns.
        bool: True if valid, False if not
    """
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False


def make_streamed_get_request(url, headers=None):
    """Helper function to make a request to given url in stream mode (without
    immediate download).

    Args:
        url (str): location of the file
        headers (dict): headers used when fetching files

    Returns:
        requests.Response: successful response from the server

    Raises:
        MultiFileReaderException: error communicating with the server
    """
    try:
        response = requests.get(
            url, headers=headers, allow_redirects=True, stream=True
        )
        response.raise_for_status()
    except requests.exceptions.HTTPError:
        raise MultiFileReaderException(
            "Unable to determine size of file at %s Server returned status %s"
            % (url, response.status_code)
        )
    except requests.exceptions.RequestException:
        raise MultiFileReaderException(
            "Unable to determine size of file at %s Server failed to respond."
            % url
        )

    return response


def get_online_file_size(url, headers=None):
    """Read file size from Content-Length header for given url.

    Args:
        url (str): location of the file
        headers (dict): headers used when fetching files

    Returns:
        int: file size in bytes

    Raises:
        MultiFileReaderException: error communicating with the server
    """
    response = make_streamed_get_request(url, headers)

    size = response.headers.get("Content-Length")
    try:
        return int(size)
    except (TypeError, ValueError):
        raise MultiFileReaderException(
            "Size %s returned for file %s was not a valid number."
            % (size, url)
        )


def get_streamed_online_file(url, headers=None):
    """Get online file without loading it whole in to memory.

    Only starts accessing it once .read() method is called on the result of
    this function.

    Args:
        url (str): location of the file
        headers (dict): headers used when fetching files

    Returns:
        urllib3.response.HTTPResponse: raw response from provided url
    """
    response = make_streamed_get_request(url, headers)

    # note: .raw does not handle decoding, but that is not an issue with
    # binary data
    return response.raw
