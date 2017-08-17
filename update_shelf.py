#!/usr/bin/env python3
#
#   This file is part of Dockershelf.
#   Copyright (C) 2016-2017, Dockershelf Developers.
#
#   Please refer to AUTHORS.md for a complete list of Copyright holders.
#
#   Dockershelf is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   Dockershelf is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program. If not, see http://www.gnu.org/licenses.

import os
import re
import sys
import json
import fnmatch
import shutil
from contextlib import closing

try:
    from urllib2 import urlopen, Request
except ImportError:
    from urllib.request import urlopen, Request

try:
    from HTMLParser import HTMLParser
except ImportError:
    from html.parser import HTMLParser

from pkg_resources import parse_version

if not sys.version_info < (3,):
    unicode = str
    basestring = str


def find_dirs(path=None, pattern='*'):
    assert isinstance(path, basestring)
    assert isinstance(pattern, basestring)

    dirlist = []
    for directory, subdirs, files in os.walk(os.path.normpath(path)):
        for subdir in fnmatch.filter(subdirs, pattern):
            if os.path.isdir(os.path.join(directory, subdir)):
                dirlist.append(os.path.join(directory, subdir))
    return dirlist


class MongoVersionParser(HTMLParser):
    def handle_starttag(self, tag, attrs):
        if attrs:
            dlstr = attrs[0][1]
            # dlstr = dlstr.replace('http://downloads.mongodb.org/src/mongodb-src-v', '')
            # dlstr = dlstr.replace('http://downloads.mongodb.org/src/mongodb-src-r', '')
            # dlstr = dlstr.replace('http://downloads.mongodb.org/src/mongodb-src-', '')
            # dlstr = dlstr.replace('.tar.gz.sig', '')
            # dlstr = dlstr.replace('.tar.gz.md5', '')
            # dlstr = dlstr.replace('.tar.gz.sha1', '')
            # dlstr = dlstr.replace('.tar.gz.sha256', '')
            # dlstr = dlstr.replace('.tar.gz', '')
            # dlstr = dlstr.replace('.tgz.sig', '')
            # dlstr = dlstr.replace('.tgz.md5', '')
            # dlstr = dlstr.replace('.tgz.sha1', '')
            # dlstr = dlstr.replace('.tgz.sha256', '')
            # dlstr = dlstr.replace('.tgz', '')
            # dlstr = dlstr.replace('.zip.sig', '')
            # dlstr = dlstr.replace('.zip.md5', '')
            # dlstr = dlstr.replace('.zip.sha1', '')
            # dlstr = dlstr.replace('.zip.sha256', '')
            # dlstr = dlstr.replace('.zip', '')
            # dlstr = dlstr.replace('-cut', '')
            # dlstr = dlstr.replace('-latest', '')
            # dlstr = dlstr.replace('latest', '')
            # dlstr = re.sub('-rc.*', '', dlstr)
            # dlstr = re.sub('_rc.*', '', dlstr)
            dlstr = dlstr.replace('..', '')
            dlstr = dlstr.replace('development', '')
            dlstr = dlstr.replace('testing', '')
            self.dlstr = dlstr


if __name__ == '__main__':

    travis_matrixlist = []
    basedir = os.path.dirname(os.path.realpath(__file__))
    travis_template = os.path.join(basedir, '.travis.yml.template')
    travis = os.path.join(basedir, '.travis.yml')
    readme_template = os.path.join(basedir, 'README.md.template')
    readme = os.path.join(basedir, 'README.md')

    debian_readme_tablelist = []
    debiandir = os.path.join(basedir, 'debian')
    debian_dockerfile_template = os.path.join(debiandir, 'Dockerfile.template')
    debian_readme_template = os.path.join(debiandir, 'README.md.template')
    debian_readme = os.path.join(debiandir, 'README.md')
    debian_suites = ['oldoldstable', 'oldstable', 'stable', 'testing', 'unstable']

    for deldir in find_dirs(debiandir):
        shutil.rmtree(deldir)

    for debian_suite in debian_suites:
        base_image = 'scratch'
        debian_release_url = 'https://deb.debian.org/debian/dists/{0}/Release'.format(debian_suite)

        r = Request(debian_release_url)
        r.add_header('Range', 'bytes={0}-{1}'.format(0, 256))

        with closing(urlopen(r)) as d:
            debian_releases_content = d.read()

        debian_codename = re.findall('Codename: (.*)', debian_releases_content)[0]
        debian_codename_dir = os.path.join(debiandir, debian_codename)
        debian_dockerfile = os.path.join(debian_codename_dir, 'Dockerfile')
        docker_tag = 'dockershelf/debian:{0}'.format(debian_codename)
        docker_url = 'https://hub.docker.com/r/dockershelf/debian'
        dockerfile_badge = 'https://img.shields.io/badge/-debian%2F{0}%2FDockerfile-blue.svg'.format(debian_codename)
        dockerfile_url = 'https://github.com/LuisAlejandro/dockershelf/blob/master/debian/{0}/Dockerfile'.format(debian_codename)
        microbadger_badge = 'https://images.microbadger.com/badges/image/dockershelf/debian:{0}.svg'.format(debian_codename)
        microbadger_url = 'https://microbadger.com/images/dockershelf/debian:{0}'.format(debian_codename)

        travis_matrixlist.append('        - DOCKER_IMAGE_NAME="dockershelf/debian:{0}" DOCKER_IMAGE_EXTRA_TAGS="dockershelf/debian:{1}"'.format(debian_codename, debian_suite))
        debian_readme_tablelist.append('|[`{0}`][{1}]|`{2}`|[![][{3}]][{4}]|[![][{5}]][{6}]|'.format(
            docker_tag, docker_url, debian_codename, dockerfile_badge, dockerfile_url, microbadger_badge, microbadger_url))

        os.makedirs(debian_codename_dir)

        with open(debian_dockerfile_template, 'r') as dct:
            debian_dockerfile_template_content = dct.read()

        debian_dockerfile_content = debian_dockerfile_template_content
        debian_dockerfile_content = re.sub('%%BASE_IMAGE%%', base_image, debian_dockerfile_content)
        debian_dockerfile_content = re.sub('%%DEBIAN_RELEASE%%', debian_codename, debian_dockerfile_content)

        with open(debian_dockerfile, 'w') as dd:
            dd.write(debian_dockerfile_content)

    with open(debian_readme_template, 'r') as drt:
        debian_readme_template_content = drt.read()

    debian_readme_table = '\n'.join(debian_readme_tablelist)

    debian_readme_content = debian_readme_template_content
    debian_readme_content = re.sub('%%DEBIAN_TABLE%%', debian_readme_table, debian_readme_content)

    with open(debian_readme, 'w') as dr:
        dr.write(debian_readme_content)

    versions = {'cpython': {}}
    python_versions = []
    python_readme_tablelist = []
    pythondir = os.path.join(basedir, 'python')
    python_dockerfile_template = os.path.join(pythondir, 'Dockerfile.template')
    python_readme_template = os.path.join(pythondir, 'README.md.template')
    python_readme = os.path.join(pythondir, 'README.md')
    python_versions_list_file = 'https://raw.githubusercontent.com/saghul/pythonz/master/pythonz/installer/versions.py'

    with closing(urlopen(python_versions_list_file)) as p:
        exec(p.read())

    python_versions_pre = versions['cpython'].keys()
    python_versions_sel = set(map(lambda x: '.'.join(x.split('.')[:2]), python_versions_pre))
    python_versions_sel = python_versions_sel - set(['2.4', '2.5', '3.0', '3.1', '3.3'])

    for vsel in python_versions_sel:
        psel = set(filter(lambda x: '.'.join(x.split('.')[:2]) == vsel, python_versions_pre))
        psel = [parse_version(x) for x in psel]
        psel.sort()
        python_versions.append(str(psel[-1]))

    for deldir in find_dirs(pythondir):
        shutil.rmtree(deldir)

    for python_version in python_versions:
        python_version_short = '.'.join(python_version.split('.')[:2])

        for python_os in ['stable', 'unstable']:
            base_image = 'dockershelf/debian:{0}'.format(python_os)
            python_os_version = '{0}-{1}'.format(python_version_short, python_os)
            python_os_version_dir = os.path.join(pythondir, python_os_version)
            python_dockerfile = os.path.join(python_os_version_dir, 'Dockerfile')

            docker_tag = 'dockershelf/python:{0}'.format(python_os_version)
            docker_url = 'https://hub.docker.com/r/dockershelf/python'
            dockerfile_badge = 'https://img.shields.io/badge/-python%2F{0}%2FDockerfile-blue.svg'.format(python_os_version)
            dockerfile_url = 'https://github.com/LuisAlejandro/dockershelf/blob/master/python/{0}/Dockerfile'.format(python_os_version)
            microbadger_badge = 'https://images.microbadger.com/badges/image/dockershelf/python:{0}.svg'.format(python_os_version)
            microbadger_url = 'https://microbadger.com/images/dockershelf/python:{0}'.format(python_os_version)

            if python_os == 'unstable':
                if python_version_short == '2.7':
                    travis_matrixlist.append('        - DOCKER_IMAGE_NAME="dockershelf/python:{0}" DOCKER_IMAGE_EXTRA_TAGS="dockershelf/python:{1} dockershelf/python:2"'.format(python_os_version, python_version_short))
                elif python_version_short == '3.5':
                    travis_matrixlist.append('        - DOCKER_IMAGE_NAME="dockershelf/python:{0}" DOCKER_IMAGE_EXTRA_TAGS="dockershelf/python:{1} dockershelf/python:3"'.format(python_os_version, python_version_short))
                else:
                    travis_matrixlist.append('        - DOCKER_IMAGE_NAME="dockershelf/python:{0}" DOCKER_IMAGE_EXTRA_TAGS="dockershelf/python:{1}"'.format(python_os_version, python_version_short))
            else:
                travis_matrixlist.append('        - DOCKER_IMAGE_NAME="dockershelf/python:{0}"'.format(python_os_version))

            python_readme_tablelist.append('|[`{0}`][{1}]|`{2}`|[![][{3}]][{4}]|[![][{5}]][{6}]|'.format(
                docker_tag, docker_url, python_os_version, dockerfile_badge, dockerfile_url, microbadger_badge, microbadger_url))

            os.makedirs(python_os_version_dir)

            with open(python_dockerfile_template, 'r') as pdt:
                python_dockerfile_template_content = pdt.read()

            python_dockerfile_content = python_dockerfile_template_content
            python_dockerfile_content = re.sub('%%BASE_IMAGE%%', base_image, python_dockerfile_content)
            python_dockerfile_content = re.sub('%%DEBIAN_RELEASE%%', python_os, python_dockerfile_content)
            python_dockerfile_content = re.sub('%%PYTHON_VERSION%%', python_version, python_dockerfile_content)
            python_dockerfile_content = re.sub('%%PYTHON_VERSION_SHORT%%', python_version_short, python_dockerfile_content)

            with open(python_dockerfile, 'w') as pd:
                pd.write(python_dockerfile_content)

    with open(python_readme_template, 'r') as prt:
        python_readme_template_content = prt.read()

    python_readme_table = '\n'.join(python_readme_tablelist)

    python_readme_content = python_readme_template_content
    python_readme_content = re.sub('%%PYTHON_TABLE%%', python_readme_table, python_readme_content)

    with open(python_readme, 'w') as pr:
        pr.write(python_readme_content)

    latex_readme_tablelist = []
    latexdir = os.path.join(basedir, 'latex')
    latex_dockerfile_template = os.path.join(latexdir, 'Dockerfile.template')
    latex_readme_template = os.path.join(latexdir, 'README.md.template')
    latex_readme = os.path.join(latexdir, 'README.md')
    latex_os_versions = ['stable', 'unstable']

    for deldir in find_dirs(latexdir):
        shutil.rmtree(deldir)

    for latex_os_version in latex_os_versions:
        base_image = 'dockershelf/debian:{0}'.format(latex_os_version)
        latex_os_version_dir = os.path.join(latexdir, latex_os_version)
        latex_dockerfile = os.path.join(latex_os_version_dir, 'Dockerfile')

        docker_tag = 'dockershelf/latex:{0}'.format(latex_os_version)
        docker_url = 'https://hub.docker.com/r/dockershelf/latex'
        dockerfile_badge = 'https://img.shields.io/badge/-latex%2F{0}%2FDockerfile-blue.svg'.format(latex_os_version)
        dockerfile_url = 'https://github.com/LuisAlejandro/dockershelf/blob/master/latex/{0}/Dockerfile'.format(latex_os_version)
        microbadger_badge = 'https://images.microbadger.com/badges/image/dockershelf/latex:{0}.svg'.format(latex_os_version)
        microbadger_url = 'https://microbadger.com/images/dockershelf/latex:{0}'.format(latex_os_version)

        if latex_os_version == 'unstable':
            travis_matrixlist.append('        - DOCKER_IMAGE_NAME="dockershelf/latex:{0}" DOCKER_IMAGE_EXTRA_TAGS="dockershelf/latex:sid"'.format(latex_os_version))
        else:
            travis_matrixlist.append('        - DOCKER_IMAGE_NAME="dockershelf/latex:{0}"'.format(latex_os_version))

        latex_readme_tablelist.append('|[`{0}`][{1}]|`{2}`|[![][{3}]][{4}]|[![][{5}]][{6}]|'.format(
            docker_tag, docker_url, latex_os_version, dockerfile_badge, dockerfile_url, microbadger_badge, microbadger_url))

        os.makedirs(latex_os_version_dir)

        with open(latex_dockerfile_template, 'r') as ldt:
            latex_dockerfile_template_content = ldt.read()

        latex_dockerfile_content = latex_dockerfile_template_content
        latex_dockerfile_content = re.sub('%%DEBIAN_RELEASE%%', latex_os_version, latex_dockerfile_content)

        with open(latex_dockerfile, 'w') as ld:
            ld.write(latex_dockerfile_content)

    with open(latex_readme_template, 'r') as lrt:
        latex_readme_template_content = lrt.read()

    latex_readme_table = '\n'.join(latex_readme_tablelist)

    latex_readme_content = latex_readme_template_content
    latex_readme_content = re.sub('%%LATEX_TABLE%%', latex_readme_table, latex_readme_content)

    with open(latex_readme, 'w') as lr:
        lr.write(latex_readme_content)

    node_readme_tablelist = []
    nodedir = os.path.join(basedir, 'node')
    node_dockerfile_template = os.path.join(nodedir, 'Dockerfile.template')
    node_readme_template = os.path.join(nodedir, 'README.md.template')
    node_readme = os.path.join(nodedir, 'README.md')
    node_versions_list_file = 'https://raw.githubusercontent.com/nodesource/distributions/master/deb/src/build.sh'

    with closing(urlopen(node_versions_list_file)) as n:
        node_versions = set(re.findall('node_(\d).x:_\d.x:nodejs:Node.js v\d.x.*', n.read()))

    for deldir in find_dirs(nodedir):
        shutil.rmtree(deldir)

    for node_version in node_versions:
        for node_os in ['stable', 'unstable']:
            base_image = 'dockershelf/debian:{0}'.format(node_os)
            node_os_version = '{0}-{1}'.format(node_version, node_os)
            node_os_version_dir = os.path.join(nodedir, node_os_version)
            node_dockerfile = os.path.join(node_os_version_dir, 'Dockerfile')

            docker_tag = 'dockershelf/node:{0}'.format(node_os_version)
            docker_url = 'https://hub.docker.com/r/dockershelf/node'
            dockerfile_badge = 'https://img.shields.io/badge/-node%2F{0}%2FDockerfile-blue.svg'.format(node_os_version)
            dockerfile_url = 'https://github.com/LuisAlejandro/dockershelf/blob/master/node/{0}/Dockerfile'.format(node_os_version)
            microbadger_badge = 'https://images.microbadger.com/badges/image/dockershelf/node:{0}.svg'.format(node_os_version)
            microbadger_url = 'https://microbadger.com/images/dockershelf/node:{0}'.format(node_os_version)

            if node_os == 'unstable':
                travis_matrixlist.append('        - DOCKER_IMAGE_NAME="dockershelf/node:{0}" DOCKER_IMAGE_EXTRA_TAGS="dockershelf/node:{1}"'.format(node_os_version, node_version))
            else:
                travis_matrixlist.append('        - DOCKER_IMAGE_NAME="dockershelf/node:{0}"'.format(node_os_version))

            node_readme_tablelist.append('|[`{0}`][{1}]|`{2}`|[![][{3}]][{4}]|[![][{5}]][{6}]|'.format(
                docker_tag, docker_url, node_os_version, dockerfile_badge, dockerfile_url, microbadger_badge, microbadger_url))

            os.makedirs(node_os_version_dir)

            with open(node_dockerfile_template, 'r') as pdt:
                node_dockerfile_template_content = pdt.read()

            node_dockerfile_content = node_dockerfile_template_content
            node_dockerfile_content = re.sub('%%BASE_IMAGE%%', base_image, node_dockerfile_content)
            node_dockerfile_content = re.sub('%%DEBIAN_RELEASE%%', node_os, node_dockerfile_content)
            node_dockerfile_content = re.sub('%%NODE_VERSION%%', node_version, node_dockerfile_content)

            with open(node_dockerfile, 'w') as pd:
                pd.write(node_dockerfile_content)

    with open(node_readme_template, 'r') as prt:
        node_readme_template_content = prt.read()

    node_readme_table = '\n'.join(node_readme_tablelist)

    node_readme_content = node_readme_template_content
    node_readme_content = re.sub('%%NODE_TABLE%%', node_readme_table, node_readme_content)

    with open(node_readme, 'w') as pr:
        pr.write(node_readme_content)

    mongo_versions = []
    mongo_readme_tablelist = []
    mongodir = os.path.join(basedir, 'mongo')
    mongo_dockerfile_template = os.path.join(mongodir, 'Dockerfile.template')
    mongo_readme_template = os.path.join(mongodir, 'README.md.template')
    mongo_readme = os.path.join(mongodir, 'README.md')
    mongo_versions_list_file = 'http://repo.mongodb.org/apt/debian/dists/jessie/mongodb-org/'

    with closing(urlopen(mongo_versions_list_file)) as n:
        mongo_versions_pre_html = re.findall("<a href='.*'>.*</a>", n.read())

    for mongo_version_string in mongo_versions_pre_html:
        mongo_version_parser = MongoVersionParser()
        mongo_version_parser.feed(mongo_version_string)
        mongo_versions.append(mongo_version_parser.dlstr)

    mongo_versions = set(filter(None, mongo_versions))

    for deldir in find_dirs(mongodir):
        shutil.rmtree(deldir)

    for mongo_version in mongo_versions:
        for mongo_os in ['stable', 'unstable']:
            base_image = 'dockershelf/debian:{0}'.format(mongo_os)
            mongo_os_version = '{0}-{1}'.format(mongo_version, mongo_os)
            mongo_os_version_dir = os.path.join(mongodir, mongo_os_version)
            mongo_dockerfile = os.path.join(mongo_os_version_dir, 'Dockerfile')

            docker_tag = 'dockershelf/mongo:{0}'.format(mongo_os_version)
            docker_url = 'https://hub.docker.com/r/dockershelf/mongo'
            dockerfile_badge = 'https://img.shields.io/badge/-mongo%2F{0}%2FDockerfile-blue.svg'.format(mongo_os_version)
            dockerfile_url = 'https://github.com/LuisAlejandro/dockershelf/blob/master/mongo/{0}/Dockerfile'.format(mongo_os_version)
            microbadger_badge = 'https://images.microbadger.com/badges/image/dockershelf/mongo:{0}.svg'.format(mongo_os_version)
            microbadger_url = 'https://microbadger.com/images/dockershelf/mongo:{0}'.format(mongo_os_version)

            if mongo_os == 'unstable':
                travis_matrixlist.append('        - DOCKER_IMAGE_NAME="dockershelf/mongo:{0}" DOCKER_IMAGE_EXTRA_TAGS="dockershelf/mongo:{1}"'.format(mongo_os_version, mongo_version))
            else:
                travis_matrixlist.append('        - DOCKER_IMAGE_NAME="dockershelf/mongo:{0}"'.format(mongo_os_version))

            mongo_readme_tablelist.append('|[`{0}`][{1}]|`{2}`|[![][{3}]][{4}]|[![][{5}]][{6}]|'.format(
                docker_tag, docker_url, mongo_os_version, dockerfile_badge, dockerfile_url, microbadger_badge, microbadger_url))

            os.makedirs(mongo_os_version_dir)

            with open(mongo_dockerfile_template, 'r') as pdt:
                mongo_dockerfile_template_content = pdt.read()

            mongo_dockerfile_content = mongo_dockerfile_template_content
            mongo_dockerfile_content = re.sub('%%BASE_IMAGE%%', base_image, mongo_dockerfile_content)
            mongo_dockerfile_content = re.sub('%%DEBIAN_RELEASE%%', mongo_os, mongo_dockerfile_content)
            mongo_dockerfile_content = re.sub('%%MONGO_VERSION%%', mongo_version, mongo_dockerfile_content)

            with open(mongo_dockerfile, 'w') as pd:
                pd.write(mongo_dockerfile_content)

    with open(mongo_readme_template, 'r') as prt:
        mongo_readme_template_content = prt.read()

    mongo_readme_table = '\n'.join(mongo_readme_tablelist)

    mongo_readme_content = mongo_readme_template_content
    mongo_readme_content = re.sub('%%MONGO_TABLE%%', mongo_readme_table, mongo_readme_content)

    with open(mongo_readme, 'w') as pr:
        pr.write(mongo_readme_content)

    with open(travis_template, 'r') as tt:
        travis_template_content = tt.read()

    travis_matrix = '\n'.join(travis_matrixlist)

    travis_content = travis_template_content
    travis_content = re.sub('%%MATRIX%%', travis_matrix, travis_content)

    with open(travis, 'w') as t:
        t.write(travis_content)

    with open(readme_template, 'r') as rt:
        readme_template_content = rt.read()

    readme_content = readme_template_content
    readme_content = re.sub('%%DEBIAN_TABLE%%', debian_readme_table, readme_content)
    readme_content = re.sub('%%PYTHON_TABLE%%', python_readme_table, readme_content)
    readme_content = re.sub('%%LATEX_TABLE%%', latex_readme_table, readme_content)
    readme_content = re.sub('%%NODE_TABLE%%', node_readme_table, readme_content)

    with open(readme, 'w') as t:
        t.write(readme_content)
