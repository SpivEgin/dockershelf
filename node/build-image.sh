#!/usr/bin/env bash
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

# Exit early if there are errors and be verbose.
set -exuo pipefail

# Some default values.
BASEDIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PY_VER_NUM_MAJOR="$( echo ${PY_VER_NUM} | awk -F'.' '{print $1}')"
PY_VER_NUM_MAJOR_STR="python${PY_VER_NUM_MAJOR}"
PY_VER_STR="python${PY_VER_NUM}"

# Some tools are needed.
DPKG_TOOLS_DEPENDS="aptitude deborphan debian-keyring dpkg-dev"
DPKG_BUILD_DEPENDS="build-essential zlib1g-dev libbz2-dev libssl-dev \
    libreadline-dev libncurses5-dev libsqlite3-dev libgdbm-dev libdb-dev \
    libexpat-dev libpcap-dev liblzma-dev libpcre3-dev"

# These options are passed to make because we need to speedup the build.
DEB_BUILD_OPTIONS="parallel=$( nproc ) nocheck nobench"

# Load helper functions
source "${BASEDIR}/library.sh"

# Apt: Install tools
# ------------------------------------------------------------------------------
# We need to install the packages defined at ${DPKG_TOOLS_DEPENDS} because
# some commands are needed to download the source code before installing the
# build dependencies.

msginfo "Installing tools and upgrading image ..."
cmdretry apt-get update
cmdretry apt-get -d upgrade
cmdretry apt-get upgrade
cmdretry apt-get -d install ${DPKG_TOOLS_DEPENDS} ${DPKG_BUILD_DEPENDS}
cmdretry apt-get install ${DPKG_TOOLS_DEPENDS} ${DPKG_BUILD_DEPENDS}

# Python: Compilation
# ------------------------------------------------------------------------------
# This is the tricky part: we will use the "clean" and "install" targets of the
# debian/rules makefile (which are used to build a debian package) to compile
# our python source code. This will generate a python build tree in the 
# debian folder which we will later process.

msginfo "Compiling python ..."
curl -fsSL "https://raw.github.com/saghul/pythonz/master/pythonz-install" | bash
pythonz install --verbose ${PY_VER_NUM}
pythonz cleanup

# Apt: Remove build depends
# ------------------------------------------------------------------------------
# We need to clear the filesystem of unwanted packages before installing python
# because some files might be confused with already installed python packages.

msginfo "Removing unnecessary packages ..."
cmdretry apt-get purge $( echo ${DPKG_BUILD_DEPENDS} \
    | sed "$( printf 's/\s%s\s/ /g;' ${DPKG_RUN_DEPENDS} )" )
cmdretry apt-get autoremove

# This is clever uh? Figure it out myself, ha!
cmdretry apt-get purge $( apt-mark showauto $( deborphan -a -n \
                                --no-show-section --guess-all --libdevel \
                                -p standard ) )
cmdretry apt-get autoremove

# This too
cmdretry apt-get purge $( aptitude search -F%p ~c ~g )
cmdretry apt-get autoremove

cmdretry apt-get purge ${DPKG_TOOLS_DEPENDS}
cmdretry apt-get autoremove

# Linking to make this the default version of python
PY_BIN_PATH="$( pythonz locate ${PY_VER_NUM} )"
ln -sfv ${PY_BIN_PATH} /usr/bin/python
ln -sfv ${PY_BIN_PATH} /usr/bin/${PY_VER_STR}
ln -sfv ${PY_BIN_PATH} /usr/bin/${PY_VER_NUM_MAJOR_STR}

# Pip: Installation
# ------------------------------------------------------------------------------
# Let's bring in the old reliable pip guy.

msginfo "Installing pip ..."
if [ "${PY_VER_NUM}" == "3.2" ]; then
    curl -fsSL "https://bootstrap.pypa.io/3.2/get-pip.py" | ${PY_VER_STR} - 'setuptools<30'
else
    curl -fsSL "https://bootstrap.pypa.io/get-pip.py" | ${PY_VER_STR}
fi

# Final cleaning
# ------------------------------------------------------------------------------
# Buncha files we won't use.

msginfo "Removing unnecessary files ..."
find /usr -name "*.py[co]" -print0 | xargs -0r rm -rfv
find /usr -name "__pycache__" -type d -print0 | xargs -0r rm -rfv
rm -rfv /tmp/* /usr/share/doc/* /usr/share/locale/* /usr/share/man/* \
        /var/cache/debconf/* /var/cache/apt/* /var/tmp/* /var/log/* \
        /var/lib/apt/lists/*