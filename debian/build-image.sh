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

# Exit early if there are errors and be verbose
set -exuo pipefail

# Some initial configuration
ARCH="amd64"
VARIANT="minbase"
DEBIAN_RELEASE="${1}"
MIRROR="http://deb.debian.org/debian"
SECMIRROR="http://deb.debian.org/debian-security"
BASEDIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
TARGET="${BASEDIR}/base"

# Packages to install at the end
DPKG_DEPENDS="iproute inetutils-ping locales curl ca-certificates \
    bash-completion"

# Load helper functions
source "${BASEDIR}/library.sh"

# We need a Debian Release
if [ -z "${DEBIAN_RELEASE}" ]; then
    msgerror "No Debian Release was given. Aborting."
    exit 1
fi

# Exit if we are not root
if [ "$( id -u )" != "0" ]; then
    msgerror "This script must be run as root. Aborting."
    exit 1
fi

msginfo "Downloading packages for base filesystem ..."
cmdretry debootstrap --verbose --variant "${VARIANT}" --arch "${ARCH}" \
    --download-only --no-check-gpg --no-check-certificate --merged-usr \
        "${DEBIAN_RELEASE}" "${TARGET}" "${MIRROR}"

msginfo "Building base filesystem ..."
cmdretry debootstrap --verbose --variant "${VARIANT}" --arch "${ARCH}" \
    --no-check-gpg --no-check-certificate --merged-usr \
        "${DEBIAN_RELEASE}" "${TARGET}" "${MIRROR}"

msginfo "Configuring base filesystem ..."
cat > "${TARGET}/etc/resolv.conf" << EOF
# Dockershelf configuration for resolv.conf
nameserver 8.8.8.8
nameserver 8.8.4.4
EOF

cat > "${TARGET}/etc/locale.gen" << EOF
# Dockershelf configuration for locale
en_US.UTF-8 UTF-8
EOF

if [ "${DEBIAN_RELEASE}" == "sid" ]; then
cat > "${TARGET}/etc/apt/sources.list" << EOF
# Dockershelf configuration for apt sources
deb ${MIRROR} ${DEBIAN_RELEASE} main
EOF
elif [ "${DEBIAN_RELEASE}" == "experimental" ]; then
cat > "${TARGET}/etc/apt/sources.list" << EOF
# Dockershelf configuration for apt sources
deb ${MIRROR} sid main
deb ${MIRROR} ${DEBIAN_RELEASE} main
EOF
else
cat > "${TARGET}/etc/apt/sources.list" << EOF
# Dockershelf configuration for apt sources
deb ${MIRROR} ${DEBIAN_RELEASE} main
deb ${MIRROR} ${DEBIAN_RELEASE}-updates main
deb ${SECMIRROR} ${DEBIAN_RELEASE}/updates main
EOF
fi

cat > "${TARGET}/etc/dpkg/dpkg.cfg.d/dockershelf" << EOF
# Dockershelf configuration for Dpkg

# If a conffile has been deleted by the user and a new version of the
# package wants to install it, let it do it.
force-confmiss

# If a package has a new version of a conffile but the user has modified it,
# answer the question with the default option.
force-confdef

# If a package has a new version of a conffile but the user has modified it,
# and there's no default option, replace the conffile with the new one.
force-confnew

# If a package tries to overwrite a file that exists in another package,
# let it do it.
force-overwrite

# Don't call sync() for every IO operation.
force-unsafe-io
EOF

cat > "${TARGET}/etc/apt/apt.conf.d/dockershelf" << EOF
# Dockershelf configuration for Apt

# Disable creation of pkgcache.bin and srcpkgcache.bin to save space.
Dir::Cache::pkgcache "";
Dir::Cache::srcpkgcache "";

# If there's a network error, retry up to 3 times.
Acquire::Retries "3";

# Don't download translations.
Acquire::Languages "none";

# Prefer download of gzipped indexes.
Acquire::CompressionTypes::Order:: "gz";

# Keep indexes gzipped.
Acquire::GzipIndexes "true";

# Don't install Suggests or Recommends.
Apt::Install-Suggests "false";
Apt::Install-Recommends "false";

# Don't ask questions, assume 'yes'.
Apt::Get::Assume-Yes "true";

# Allow installation of unauthenticated packages.
Apt::Get::AllowUnauthenticated "true";

# Remove suggested and recommended packages on autoremove.
Apt::AutoRemove::SuggestsImportant "false";
Apt::AutoRemove::RecommendsImportant "false";

# Cleaning post-hooks for dpkg and apt.
Apt::Update::Post-Invoke { "/usr/share/dockershelf/clean-apt.sh"; };
Dpkg::Post-Invoke { "/usr/share/dockershelf/clean-dpkg.sh"; };
EOF

mkdir -p "${TARGET}/usr/share/dockershelf"
touch "${TARGET}/usr/share/dockershelf/clean-apt.sh"
chmod +x "${TARGET}/usr/share/dockershelf/clean-apt.sh"
cat > "${TARGET}/usr/share/dockershelf/clean-apt.sh" << 'EOF'
#!/usr/bin/env bash
# Dockershelf post hook for apt
rm -rf /var/cache/apt/*
EOF

touch "${TARGET}/usr/share/dockershelf/clean-dpkg.sh"
chmod +x "${TARGET}/usr/share/dockershelf/clean-dpkg.sh"
cat > "${TARGET}/usr/share/dockershelf/clean-dpkg.sh" << 'EOF'
#!/usr/bin/env bash
# Dockershelf post hook for dpkg
find /usr -name "*.py[co]" -print0 | xargs -0r rm -rf
find /usr -name "__pycache__" -type d -print0 | xargs -0r rm -rf
rm -rf /usr/share/doc/* /usr/share/locale/* /usr/share/man/* \
       /var/cache/debconf/* /var/cache/apt/* 
EOF

cat >> "${TARGET}/etc/bash.bashrc" << 'EOF'
# Enable bash auto completion
if ! shopt -oq posix; then
    if [ -f /usr/share/bash-completion/bash_completion ]; then
        . /usr/share/bash-completion/bash_completion
    elif [ -f /etc/bash_completion ]; then
        . /etc/bash_completion
    fi
fi

# Show motd on login
if [ -n "${TERM}" ] && [ -r /etc/motd ]; then
    cat /etc/motd
fi

# Changing prompt
PROMPT_RED="\[\033[38;5;167m\]"
PROMPT_DARK_RED="\[\033[38;5;088m\]"
PROMPT_OFF="\[\033[0m\]"
PS1="${PROMPT_RED}[\u@${PROMPT_DARK_RED}\h]${PROMPT_OFF}:\w\$ "
EOF

cat > "${TARGET}/etc/motd" << 'EOF'

         This image was built using         
 ,-.          .               .       .     
 |  \         |               |       |  ,- 
 |  | ,-. ,-. | , ,-. ;-. ,-. |-. ,-. |  |  
 |  / | | |   |<  |-´ |   `-. | | |-´ |  |- 
 `-´  `-´ `-´ ‘ ` `-´ ‘   `-´ ‘ ‘ `-´ ‘  |  
                                        -´  
        For more information, visit         
https://github.com/LuisAlejandro/dockershelf

EOF

# Export some configuration variables before chrooting
export LANG="en_US.UTF-8" LANGUAGE="en_US.UTF-8" LC_ALL="en_US.UTF-8" \
    DEBIAN_FRONTEND="noninteractive"

msginfo "Installing dependencies and upgrading packages ..."
cmdretry chroot "${TARGET}" apt-get update
cmdretry chroot "${TARGET}" apt-get -d upgrade
cmdretry chroot "${TARGET}" apt-get upgrade
cmdretry chroot "${TARGET}" apt-get -d install ${DPKG_DEPENDS}
cmdretry chroot "${TARGET}" apt-get install ${DPKG_DEPENDS}

msginfo "Configuring locales ..."
cmdretry chroot "${TARGET}" update-locale LANG="en_US.UTF-8" \
    LANGUAGE="en_US.UTF-8" LC_ALL="en_US.UTF-8"

msginfo "Shrinking base filesystem ..."
rm -rfv "${TARGET}/tmp/"* "${TARGET}/usr/share/doc/"* \
        "${TARGET}/usr/share/locale/"* "${TARGET}/usr/share/man/"* \
        "${TARGET}/var/cache/debconf/"* "${TARGET}/var/cache/apt/"* \
        "${TARGET}/var/tmp/"* "${TARGET}/var/log/"* \
        "${TARGET}/var/lib/apt/lists/"*