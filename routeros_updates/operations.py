from __future__ import unicode_literals
try:
    # Python 2
    from urllib2 import build_opener
except ImportError:
    # Python 3
    from urllib.request import build_opener
try:
    from urlparse import urlparse
except ImportError:
    # Python 3
    from urllib.parse import urlparse
import logging
import os
import re
import shutil
import zipfile

from . import constants, __VERSION__


# protect against weird zip files with paths embedded in them
ZIP_CONTENTS_REGEX = re.compile(r"^[\w\-.]+$")


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


def _get_channel_latest_url(channel, scheme="https"):
    url = constants.LATEST_CHANNEL_URL[channel].format(channel=channel, scheme=scheme)
    return url


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

    try:
        # ensure download path exists
        os.makedirs(os.path.dirname(filepath))
    except (OSError, IOError):
        pass  # it's ok if these directories exist

    conn = urlopen(url)
    num_bytes = 0
    with open(filepath, 'wb') as fp:
        log.debug("Downloaded %s bytes so far...", num_bytes)
        shutil.copyfileobj(conn, fp, chunksize)
        num_bytes = fp.tell()
    log.debug("Finished. Downloaded %0.2f MiB.", num_bytes / 1048576.0)


def _download_latest_info_file(path, channel, scheme):
    url = _get_channel_latest_url(channel, scheme)
    url_path = urlparse(url).path
    url_path = url_path.lstrip("/").replace("/", os.path.sep)
    latest_path = os.path.join(path, url_path)
    text = _get_http_text_content(url)
    with open(latest_path, "w") as outfile:
        outfile.write(text)
    return latest_path


def _unzip_file(path, delete=False):
    """
    Unzips a zip file downloaded from upgrade.mikrotik.com
    If there is a file name not usually associated with Mikrotik packages, the file will not be unzipped.

    :param path: the path to the zip file to unzip
    :param delete: whether or not to delete the zip file when finished
    :return: the list of filenames extracted
    """
    directory = os.path.dirname(path)
    zip_file = zipfile.ZipFile(path)
    try:
        filenames = zip_file.namelist()
        for name in filenames:
            if not name.endswith(".npk") or not ZIP_CONTENTS_REGEX.match(name):
                raise IOError("Unexpected zip file downloaded. Contains a file called '%s'" % name)
        zip_file.extractall(path=directory)
    finally:
        zip_file.close()
    if delete:
        os.remove(path)
    return filenames


def download_file(arch, path="./", channel="stable", package="main", force=False, scheme="https", mirror=False,
                  unzip=True):
    """
    Downloads the Mikrotik update package for a given Mikrotik device architecture.

    :param arch: the update's target architecture (i.e. mipsbe, arm, mmips, x86)
    :param path: the filename or path to download to. If mirror is True, this will be treated as a directory
    :param channel: the version branch to download from (i.e. stable, testing, lts)
    :param package: can be either main or all
    :param force: overwrite existing files
    :param scheme: can be either http or https (default is https)
    :param mirror: if True, append the upgrade site's folder path to path (i.e. <path>/routeros/6.45.5/<package>.npk)
    :param unzip: automatically unzip the downloaded file if it was a zip file
    :return: the path that the files were ultimately downloaded to
    """
    url = get_download_url(arch=arch, channel=channel, package=package, scheme=scheme)
    log.debug("Downloading %s to %s", url, path)
    fullpath = os.path.abspath(path)
    if mirror:
        url_path = urlparse(url).path

        # remove leading / so it isn't absolute anymore
        # replace / with OS separator (which is a \ for Windows)
        url_path = url_path.lstrip('/').replace("/", os.path.sep)
        fullpath = os.path.join(fullpath, url_path)

        # for a mirror, we will also grab the "LATEST" file that tells routers there is an update available
        _download_latest_info_file(os.path.abspath(path), channel, scheme)
    else:
        _, extension = os.path.splitext(url)
        if os.path.isdir(fullpath):
            basename = os.path.basename(url)  # this is the filename to download
            fullpath = os.path.join(fullpath, basename)
        if not fullpath.lower().endswith(extension.lower()):
            fullpath = "%s%s" % (fullpath, extension)
    if fullpath != path:
        log.debug("Download path %s changed to %s", path, fullpath)
    _download_http_content_to_file(url, fullpath, force=force)
    if unzip and fullpath.lower().endswith(".zip"):
        _unzip_file(fullpath)
    return fullpath


def get_channel_latest_version(channel, scheme="https"):
    log.debug("Getting latest version for channel %s...", channel)
    # url = constants.LATEST_CHANNEL_URL[channel].format(channel=channel, scheme=scheme)
    url = _get_channel_latest_url(channel, scheme)
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
