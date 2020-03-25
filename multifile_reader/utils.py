from urllib.parse import urlparse


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
