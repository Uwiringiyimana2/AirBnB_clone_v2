#!/usr/bin/python3
"""generates a .tgz archive from the contents of the web_static folder"""
from fabric.api import local, run, put, env
from datetime import datetime
import os.path


env.hosts = ["3.85.41.66", "34.207.120.36"]


def do_pack():
    """Fabric script that generates a .tgz archive"""
    dt = datetime.utcnow()
    filename = "versions/web_static_{}{}{}{}{}{}.tgz".format(dt.year,
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


def do_deploy(archive_path):
    """distributes an archive to your web servers"""
    if os.path.isfile(archive_path) is False:
        return False

    file = archive_path.split("/")[-1]
    name = file.split(".")[0]

#    if run("chown -R ubuntu:ubuntu
    if put(archive_path, "/tmp/{}".format(file)).failed is True:
        return False
    if run("rm -rf /data/web_static/releases/{}".format(name)).failed is True:
        return False
    if run("mkdir -p /data/web_static/releases/{}".
           format(name)).failed is True:
        return False
    if run("tar -xzf /tmp/{} -C /data/web_static/releases/{}".
            format(file, name)).failed is True:
        return False
    if run("rm /tmp/{}".format(file)).failed is True:
        return False
    if run("mv /data/web_static/releases/{}/web_static/* "
           "/data/web_static/releases/{}".format(name, name)).failed is True:
        return False
    if run("rm -rf /data/web_static/releases/{}/web_static".
           format(name)).failed is True:
        return False
    if run("rm -rf /data/web_static/current").failed is True:
        return False
    if run("ln -s /data/web_static/releases/{} /data/web_static/current".
           format(name)).failed is True:
        return False
    return True


def deploy():
    """creates and distributes an archive to your web server"""
    file = do_pack()
    if file is None:
        return False
    return do_deploy(file)
