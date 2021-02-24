import os
from typing import Union
from pathlib import Path, PosixPath, WindowsPath
import shutil
import urllib3


def create(pathname: str):
    """ Creates the directory structure of pathname given in the current directory """
    datapath = Path(pathname)
    datapath.mkdir(parents=True, exist_ok=True)

    return datapath


def get_filename_from_url(url: str):
    return os.path.basename(url)


def download(url: str, filepath: Union[PosixPath, WindowsPath]):
    """ Downloads file at url and saves it at the filepath Concrete Path Object"""
    http = urllib3.PoolManager()
    with http.request("GET", url, preload_content=False) as r, open(
        filepath, "wb"
    ) as datafile:
        if r.status == 200:
            size = "UNKNOWN"
            if "Content-Length" in r.headers:
                size = int(r.headers["Content-Length"]) / (1024 * 1024)
            print(
                f"Downloading {get_filename_from_url(url)} - File Size: {size:.3f} MB"
            )
            shutil.copyfileobj(r, datafile)
            print("Download Successful")
        else:
            print(f"{r.status}: Bad request")
            filepath = None

    return filepath


def grab_from_url(url: str, pathname: str, filename: str = None, update: bool = False):
    """ Downloads the file at the URL and saves it at the pathname """
    path = create(pathname)
    if filename is None:
        filename = get_filename_from_url(url)
    filepath = path / filename
    if update or not (filepath).exists():
        filepath = download(url, filepath)
    else:
        print(f"File Already Downloaded at {filepath}")
    return filepath
