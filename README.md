# hg-setup: easily setup Mercurial with a tiny Python application

[![Latest version](https://badge.fury.io/py/hg-setup.svg)](https://pypi.python.org/pypi/hg-setup/)
![Supported Python versions](https://img.shields.io/pypi/pyversions/hg-setup.svg)
[![Heptapod CI](https://foss.heptapod.net/fluiddyn/hg-setup/badges/branch/default/pipeline.svg)](https://foss.heptapod.net/fluiddyn/hg-setup/-/pipelines)
[![Github Actions](https://github.com/fluiddyn/hg-setup/actions/workflows/ci.yml/badge.svg?branch=branch/default)](https://github.com/fluiddyn/hg-setup/actions)

hg-setup can be used to setup [Mercurial]. The main command provided by this package,
`hg-setup init` launches a simple Terminal User Interface (TUI) to initialize a
reasonable user configuration file and shell completion for bash and zsh.

With [UV], one can run it without installation with:

```sh
uvx hg-setup init
```

## Background

[Mercurial] is a Python application using C and Rust extensions. It is extendable with
Mercurial extensions and two Python packages provide very useful Mercurial extensions
that most users should use : [hg-git] (Mercurial extension hggit) and [hg-evolve]
(Mercurial extensions topic and evolve).

These things are packaged in 3 PyPI packages (associated with their equivalent
conda-forge packages): mercurial, hg-git, hg-evolve. Moreover, to use Mercurial
extensions, one has to write few lines in a configuration file (~/.hgrc).

Mercurial with hg-git and hg-evolve is great but it is a bit difficult to setup for
beginners. hg-setup is there to help people to start with Mercurial and finalize its
installation.

## Install

Here, we give commands to install altogether and in an isolated environment Mercurial,
its more useful extensions ([hg-git] and [hg-evolve]) and hg-setup.

### From the package on PyPI

- With [pipx]

```sh
pipx install mercurial
pipx inject mercurial hg-git hg-evolve hg-setup
```

- With [UV]

```sh
uv tool install mercurial --with hg-git --with hg-evolve --with hg-setup
```

### From the conda-forge package

**Soon**, there will be a conda-forge package, and one will be able to install Mercurial,
hg-git, hg-evolve and hg-setup by running:

- with [Miniforge] and [conda-app]

```sh
conda activate base
pip install conda-app
conda-app install mercurial
```

- With [Pixi]

```sh
pixi global install mercurial-app
# or (equivalent)
pixi global install mercurial --with hg-git --with hg-evolve --with hg-setup
```

### From source

```sh
pipx install hg-setup@hg+https://foss.heptapod.net/fluiddyn/hg-setup
```

For development installation, see the file [CONTRIBUTING.md](./CONTRIBUTING.md).

### My plans

I hope that ultimately hg-setup can be installed automatically with Mercurial when
running install commands like:

```sh
# from PyPI
pipx install mercurial[full]
uv tool install mercurial[full]
# with Miniforge (conda-forge) and conda-app
conda-app install mercurial
# this would require optional deps on conda-forge
pixi global install mercurial[full]
```

## User interfaces

The ~/.hgrc file and shell completion for bash and zsh can be initialized with a simple
Terminal User Interface (TUI):

```sh
hg-setup init
```

We can also avoid the TUI with

```sh
hg-setup init --name "Alice Lastname" --email alice.lastname@proton.me --auto
```

The shell completion for bash and zsh can be initialized with:

```sh
hg-setup init-shell-completion bash
hg-setup init-shell-completion zsh
```

[conda-app]: https://foss.heptapod.net/fluiddyn/conda-app
[hg-evolve]: https://foss.heptapod.net/mercurial/evolve
[hg-git]: https://foss.heptapod.net/mercurial/hg-git
[mercurial]: https://www.mercurial-scm.org
[miniforge]: https://github.com/conda-forge/miniforge
[pipx]: https://pipx.pypa.io
[pixi]: https://pixi.sh
[uv]: https://docs.astral.sh/uv/
