#!/usr/bin/python3
"""generates a .tgz archive from the contents of the web_static folder"""
from fabric.api import local
from datetime import datetime
import os.path


def do_pack():
    """Fabric script that generates a .tgz archive"""
    dt = datetime.utcnow()
    filename = "versions/web_static_{}{}{}{}{}{}{}.tgz".format(dt.year,
                                                               dt.month,
                                                               dt.day,
                                                               dt.hour,
                                                               dt.minute,
                                                               dt.second)
    if os.path.isdir("versions") is False:
        if local("mkdir -p versions").failed is True:
            return None
    if local("tar -cvzf {} web_static".format(filename)).failed is True:
        return None
    return filename
