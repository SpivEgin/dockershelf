![](https://gitcdn.xyz/repo/LuisAlejandro/dockershelf/master/banner.svg)

---

[![](https://img.shields.io/github/release/LuisAlejandro/dockershelf.svg)](https://github.com/LuisAlejandro/dockershelf/releases) [![](https://img.shields.io/travis/LuisAlejandro/dockershelf.svg)](https://travis-ci.org/LuisAlejandro/dockershelf) [![](https://img.shields.io/github/issues-raw/LuisAlejandro/dockershelf/in%20progress.svg?label=in%20progress)](https://github.com/LuisAlejandro/dockershelf/issues?q=is%3Aissue+is%3Aopen+label%3A%22in+progress%22) [![](https://badges.gitter.im/LuisAlejandro/dockershelf.svg)](https://gitter.im/LuisAlejandro/dockershelf) [![](https://cla-assistant.io/readme/badge/LuisAlejandro/dockershelf)](https://cla-assistant.io/LuisAlejandro/dockershelf)

Current version: 0.1.5

*Dockershelf* is a repository that serves as a collector for docker recipes that I've found useful for specific cases and personal applications. However, I've designed them for universal purposes, so that they can serve for other applications as well.

All docker images are updated, tested and published *daily* via a Travis cron job.

## Shelves

### Debian

These images are similar to the official ones, but with some improved configurations. Check out [debian/README.md](https://github.com/LuisAlejandro/dockershelf/blob/master/debian/README.md) for more details.

![](https://gitcdn.xyz/repo/LuisAlejandro/dockershelf/master/table.svg)

|Image                                    |Release  |Dockerfile                |Layers                    |
|-----------------------------------------|---------|--------------------------|--------------------------|
|[`dockershelf/debian:wheezy`][https://hub.docker.com/r/dockershelf/debian]|`wheezy`|[![][https://img.shields.io/badge/-debian%2Fwheezy%2FDockerfile-blue.svg]][https://github.com/LuisAlejandro/dockershelf/blob/master/debian/wheezy/Dockerfile]|[![][https://images.microbadger.com/badges/image/dockershelf/debian:wheezy.svg]][https://microbadger.com/images/dockershelf/debian:wheezy]|
|[`dockershelf/debian:jessie`][https://hub.docker.com/r/dockershelf/debian]|`jessie`|[![][https://img.shields.io/badge/-debian%2Fjessie%2FDockerfile-blue.svg]][https://github.com/LuisAlejandro/dockershelf/blob/master/debian/jessie/Dockerfile]|[![][https://images.microbadger.com/badges/image/dockershelf/debian:jessie.svg]][https://microbadger.com/images/dockershelf/debian:jessie]|
|[`dockershelf/debian:stretch`][https://hub.docker.com/r/dockershelf/debian]|`stretch`|[![][https://img.shields.io/badge/-debian%2Fstretch%2FDockerfile-blue.svg]][https://github.com/LuisAlejandro/dockershelf/blob/master/debian/stretch/Dockerfile]|[![][https://images.microbadger.com/badges/image/dockershelf/debian:stretch.svg]][https://microbadger.com/images/dockershelf/debian:stretch]|
|[`dockershelf/debian:buster`][https://hub.docker.com/r/dockershelf/debian]|`buster`|[![][https://img.shields.io/badge/-debian%2Fbuster%2FDockerfile-blue.svg]][https://github.com/LuisAlejandro/dockershelf/blob/master/debian/buster/Dockerfile]|[![][https://images.microbadger.com/badges/image/dockershelf/debian:buster.svg]][https://microbadger.com/images/dockershelf/debian:buster]|
|[`dockershelf/debian:sid`][https://hub.docker.com/r/dockershelf/debian]|`sid`|[![][https://img.shields.io/badge/-debian%2Fsid%2FDockerfile-blue.svg]][https://github.com/LuisAlejandro/dockershelf/blob/master/debian/sid/Dockerfile]|[![][https://images.microbadger.com/badges/image/dockershelf/debian:sid.svg]][https://microbadger.com/images/dockershelf/debian:sid]|

![](https://gitcdn.xyz/repo/LuisAlejandro/dockershelf/master/table.svg)

### Python

These are python images compiled from source, using the `debian/rules` makefile from debian's python source. These images are then updated to Debian Sid. Check out [python/README.md](https://github.com/LuisAlejandro/dockershelf/blob/master/python/README.md) for more details.

![](https://gitcdn.xyz/repo/LuisAlejandro/dockershelf/master/table.svg)

|Image                                    |Release  |Dockerfile                |Layers                    |
|-----------------------------------------|---------|--------------------------|--------------------------|
|[`dockershelf/python:2.6-stable`][https://hub.docker.com/r/dockershelf/python]|`2.6-stable`|[![][https://img.shields.io/badge/-python%2F2.6-stable%2FDockerfile-blue.svg]][https://github.com/LuisAlejandro/dockershelf/blob/master/python/2.6-stable/Dockerfile]|[![][https://images.microbadger.com/badges/image/dockershelf/python:2.6-stable.svg]][https://microbadger.com/images/dockershelf/python:2.6-stable]|
|[`dockershelf/python:2.6-unstable`][https://hub.docker.com/r/dockershelf/python]|`2.6-unstable`|[![][https://img.shields.io/badge/-python%2F2.6-unstable%2FDockerfile-blue.svg]][https://github.com/LuisAlejandro/dockershelf/blob/master/python/2.6-unstable/Dockerfile]|[![][https://images.microbadger.com/badges/image/dockershelf/python:2.6-unstable.svg]][https://microbadger.com/images/dockershelf/python:2.6-unstable]|
|[`dockershelf/python:2.7-stable`][https://hub.docker.com/r/dockershelf/python]|`2.7-stable`|[![][https://img.shields.io/badge/-python%2F2.7-stable%2FDockerfile-blue.svg]][https://github.com/LuisAlejandro/dockershelf/blob/master/python/2.7-stable/Dockerfile]|[![][https://images.microbadger.com/badges/image/dockershelf/python:2.7-stable.svg]][https://microbadger.com/images/dockershelf/python:2.7-stable]|
|[`dockershelf/python:2.7-unstable`][https://hub.docker.com/r/dockershelf/python]|`2.7-unstable`|[![][https://img.shields.io/badge/-python%2F2.7-unstable%2FDockerfile-blue.svg]][https://github.com/LuisAlejandro/dockershelf/blob/master/python/2.7-unstable/Dockerfile]|[![][https://images.microbadger.com/badges/image/dockershelf/python:2.7-unstable.svg]][https://microbadger.com/images/dockershelf/python:2.7-unstable]|
|[`dockershelf/python:3.2-stable`][https://hub.docker.com/r/dockershelf/python]|`3.2-stable`|[![][https://img.shields.io/badge/-python%2F3.2-stable%2FDockerfile-blue.svg]][https://github.com/LuisAlejandro/dockershelf/blob/master/python/3.2-stable/Dockerfile]|[![][https://images.microbadger.com/badges/image/dockershelf/python:3.2-stable.svg]][https://microbadger.com/images/dockershelf/python:3.2-stable]|
|[`dockershelf/python:3.2-unstable`][https://hub.docker.com/r/dockershelf/python]|`3.2-unstable`|[![][https://img.shields.io/badge/-python%2F3.2-unstable%2FDockerfile-blue.svg]][https://github.com/LuisAlejandro/dockershelf/blob/master/python/3.2-unstable/Dockerfile]|[![][https://images.microbadger.com/badges/image/dockershelf/python:3.2-unstable.svg]][https://microbadger.com/images/dockershelf/python:3.2-unstable]|
|[`dockershelf/python:3.4-stable`][https://hub.docker.com/r/dockershelf/python]|`3.4-stable`|[![][https://img.shields.io/badge/-python%2F3.4-stable%2FDockerfile-blue.svg]][https://github.com/LuisAlejandro/dockershelf/blob/master/python/3.4-stable/Dockerfile]|[![][https://images.microbadger.com/badges/image/dockershelf/python:3.4-stable.svg]][https://microbadger.com/images/dockershelf/python:3.4-stable]|
|[`dockershelf/python:3.4-unstable`][https://hub.docker.com/r/dockershelf/python]|`3.4-unstable`|[![][https://img.shields.io/badge/-python%2F3.4-unstable%2FDockerfile-blue.svg]][https://github.com/LuisAlejandro/dockershelf/blob/master/python/3.4-unstable/Dockerfile]|[![][https://images.microbadger.com/badges/image/dockershelf/python:3.4-unstable.svg]][https://microbadger.com/images/dockershelf/python:3.4-unstable]|
|[`dockershelf/python:3.5-stable`][https://hub.docker.com/r/dockershelf/python]|`3.5-stable`|[![][https://img.shields.io/badge/-python%2F3.5-stable%2FDockerfile-blue.svg]][https://github.com/LuisAlejandro/dockershelf/blob/master/python/3.5-stable/Dockerfile]|[![][https://images.microbadger.com/badges/image/dockershelf/python:3.5-stable.svg]][https://microbadger.com/images/dockershelf/python:3.5-stable]|
|[`dockershelf/python:3.5-unstable`][https://hub.docker.com/r/dockershelf/python]|`3.5-unstable`|[![][https://img.shields.io/badge/-python%2F3.5-unstable%2FDockerfile-blue.svg]][https://github.com/LuisAlejandro/dockershelf/blob/master/python/3.5-unstable/Dockerfile]|[![][https://images.microbadger.com/badges/image/dockershelf/python:3.5-unstable.svg]][https://microbadger.com/images/dockershelf/python:3.5-unstable]|
|[`dockershelf/python:3.6-stable`][https://hub.docker.com/r/dockershelf/python]|`3.6-stable`|[![][https://img.shields.io/badge/-python%2F3.6-stable%2FDockerfile-blue.svg]][https://github.com/LuisAlejandro/dockershelf/blob/master/python/3.6-stable/Dockerfile]|[![][https://images.microbadger.com/badges/image/dockershelf/python:3.6-stable.svg]][https://microbadger.com/images/dockershelf/python:3.6-stable]|
|[`dockershelf/python:3.6-unstable`][https://hub.docker.com/r/dockershelf/python]|`3.6-unstable`|[![][https://img.shields.io/badge/-python%2F3.6-unstable%2FDockerfile-blue.svg]][https://github.com/LuisAlejandro/dockershelf/blob/master/python/3.6-unstable/Dockerfile]|[![][https://images.microbadger.com/badges/image/dockershelf/python:3.6-unstable.svg]][https://microbadger.com/images/dockershelf/python:3.6-unstable]|
|[`dockershelf/python:3.7-stable`][https://hub.docker.com/r/dockershelf/python]|`3.7-stable`|[![][https://img.shields.io/badge/-python%2F3.7-stable%2FDockerfile-blue.svg]][https://github.com/LuisAlejandro/dockershelf/blob/master/python/3.7-stable/Dockerfile]|[![][https://images.microbadger.com/badges/image/dockershelf/python:3.7-stable.svg]][https://microbadger.com/images/dockershelf/python:3.7-stable]|
|[`dockershelf/python:3.7-unstable`][https://hub.docker.com/r/dockershelf/python]|`3.7-unstable`|[![][https://img.shields.io/badge/-python%2F3.7-unstable%2FDockerfile-blue.svg]][https://github.com/LuisAlejandro/dockershelf/blob/master/python/3.7-unstable/Dockerfile]|[![][https://images.microbadger.com/badges/image/dockershelf/python:3.7-unstable.svg]][https://microbadger.com/images/dockershelf/python:3.7-unstable]|

![](https://gitcdn.xyz/repo/LuisAlejandro/dockershelf/master/table.svg)

### Latex

This is an image based on [`dockershelf/debian:sid`](https://microbadger.com/images/dockershelf/debian:sid) with `texlive-fonts-recommended`, `texlive-latex-base`, `texlive-latex-extra` and `latex-xcolor` packages installed. It should be enough to use the `pdflatex` binary for basic Latex to PDF conversion. Check out [latex/README.md](https://github.com/LuisAlejandro/dockershelf/blob/master/latex/README.md) for more details.

[ilatexl]: https://hub.docker.com/r/dockershelf/latex
[dlatex]: https://img.shields.io/badge/-latex%2Fsid%2FDockerfile-blue.svg
[dlatexl]: https://github.com/LuisAlejandro/dockershelf/blob/master/latex/sid/Dockerfile
[llatex]: https://images.microbadger.com/badges/image/dockershelf/latex:sid.svg
[llatexl]: https://microbadger.com/images/dockershelf/latex:sid

![](https://gitcdn.xyz/repo/LuisAlejandro/dockershelf/master/table.svg)

|Image                             |Release|Dockerfile            |Layers                |
|----------------------------------|-------|----------------------|----------------------|
|[`dockershelf/latex:sid`][ilatexl]|`sid`  |[![][dlatex]][dlatexl]|[![][llatex]][llatexl]|

![](https://gitcdn.xyz/repo/LuisAlejandro/dockershelf/master/table.svg)

## How to download

Pull one of the available images and start hacking!

```bash
git pull [docker image name]
git run -it [docker image name] bash
```
<sup>[docker image name] is the desired image to download.</sup>

## How to build locally

Clone this repository to your machine.

```bash
git clone https://github.com/LuisAlejandro/dockershelf
```

Run the build script in the root folder of your local copy. Remember to have docker installed and make sure your user has proper privileges to execute `docker build`.

```bash
bash build-image.sh [docker image name]
```

<sup>[docker image name] is the desired image to build.</sup>

## Made with :heart: and :hamburger:

![Banner](http://huntingbears.com.ve/static/img/site/banner.svg)

My name is Luis ([@LuisAlejandro](https://github.com/LuisAlejandro)) and I'm a Free and Open-Source Software developer living in Maracay, Venezuela.

If you like what I do, please support me on [Patreon](https://www.patreon.com/luisalejandro),  [Flattr](https://flattr.com/profile/luisalejandro), or donate via [PayPal](https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=B8LPXHQY8QE8Y), so that I can continue doing what I love.

> Blog [huntingbears.com.ve](http://huntingbears.com.ve) · GitHub [@LuisAlejandro](https://github.com/LuisAlejandro) · Twitter [@LuisAlejandro](https://twitter.com/LuisAlejandro)