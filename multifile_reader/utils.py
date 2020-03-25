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
    try:
        response = requests.get(url, headers=headers, allow_redirects=True, stream=True)
    except requests.exceptions.HTTPError:
        raise MultiFileReaderException(
            "Unable to determine size of file at %s Server returned status %s"
            % (url, response.status_code)
        )
    except requests.exceptions.RequestException:
        raise MultiFileReaderException(
            "Unable to determine size of file at %s Server failed to respond." % url
        )

    return response.headers.get("Content-Length")
