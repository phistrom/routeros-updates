from __future__ import unicode_literals
try:
    # Python 2
    from urllib2 import build_opener
except ImportError:
    # Python 3
    from urllib.request import build_opener
import logging
import os
import re
import shutil

from . import constants, __VERSION__


log = logging.getLogger("routeros_update_check")

# add an identifying User-Agent header for our requests
_opener = build_opener()
_opener.addheaders = [
    ('User-Agent', 'routeros-update-checker v%s' % __VERSION__)
]
urlopen = _opener.open


def _get_http_text_content(url):
    log.debug("Connecting to %s ...", url)
    conn = urlopen(url)
    try:
        try:
            content_type = conn.info()['Content-Type']
            encoding = re.search(r"charset=([\w-]+)", content_type).group(1).lower()
        except (AttributeError, TypeError):
            encoding = constants.DEFAULT_ENCODING
        content = conn.read().decode(encoding, "ignore")
    finally:
        conn.close()

    return content


def _download_http_content_to_file(url, filepath, chunksize=1024*16, force=False):
    """
    https://stackoverflow.com/a/5397438/489667

    :param url: URL for the file to download
    :param filepath: the path to download the file to
    :param chunksize: the buffer to allocate for downloading the file
    :param force: overwrite existing files with this download
    """

    if os.path.isdir(filepath):
        raise OSError("%s is a directory" % filepath)

    if os.path.exists(filepath) and not force:
        raise OSError("%s already exists" % filepath)

    conn = urlopen(url)
    num_bytes = 0
    with open(filepath, 'wb') as fp:
        log.debug("Downloaded %s bytes so far...", num_bytes)
        shutil.copyfileobj(conn, fp, chunksize)
        num_bytes = fp.tell()
    log.debug("Finished. Downloaded %0.2f MiB.", num_bytes / 1048576.0)


def download_file(arch, path="./", channel="stable", package="main", force=False, scheme="https"):
    url = get_download_url(arch=arch, channel=channel, package=package, scheme=scheme)
    log.debug("Downloading %s to %s", url, path)
    fullpath = os.path.abspath(path)
    _, extension = os.path.splitext(url)
    if os.path.isdir(fullpath):
        basename = os.path.basename(url)
        fullpath = os.path.join(fullpath, basename)
    if not fullpath.lower().endswith(extension.lower()):
        fullpath = "%s%s" % (fullpath, extension)
    if fullpath != path:
        log.debug("Download path %s changed to %s", path, fullpath)
    _download_http_content_to_file(url, fullpath, force=force)
    return fullpath


def get_channel_latest_version(channel, scheme="https"):
    log.debug("Getting latest version for channel %s...", channel)
    url = constants.LATEST_CHANNEL_URL[channel].format(channel=channel, scheme=scheme)
    content = _get_http_text_content(url)
    version, _ = re.split(r"\s+", content, maxsplit=1)
    log.debug("Latest version is %s", version)
    return version


def get_download_url(arch, channel="stable", package="main", scheme="https"):
    version = get_channel_latest_version(channel=channel, scheme=scheme)
    url = constants.DOWNLOAD_URL[package].format(scheme=scheme, version=version, arch=arch)
    return url


def get_patch_notes(channel="stable", scheme="https"):
    version = get_channel_latest_version(channel, scheme)
    log.debug("Getting patch notes for version %s...", version)
    url = constants.CHANGELOG_URL.format(scheme=scheme, version=version)
    content = _get_http_text_content(url)
    return content
