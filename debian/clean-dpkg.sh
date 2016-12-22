#!/usr/bin/env bash
#
#   This file is part of Dockershelf.
#   Copyright (C) 2016, Dockershelf Developers.
#
#   Please refer to AUTHORS.rst for a complete list of Copyright holders.
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

# Exit early if there are errors.
set -e

# Delete a lot of unnecessary files.
find /usr -name "*.py[co]" -print0 | xargs -0r rm -rf
find /usr -name "__pycache__" -type d -print0 | xargs -0r rm -rf
rm -rf /usr/share/doc/* /usr/share/locale/* /usr/share/man/* \
       /var/cache/debconf/* /var/cache/apt/*