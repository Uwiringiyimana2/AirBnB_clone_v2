#!/usr/bin/python3
"""that distributes an archive to your web servers,
using the function do_deploy"""
import os.path
from fabric.api import run, put, env, sudo


env.hosts = ["3.85.41.66", "34.207.120.36"]


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
    sudo("service nginx restart")
    return True
