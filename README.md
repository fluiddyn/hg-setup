# hg-setup: easily setup Mercurial with a tiny Python application

Warning: in early development.

## Background

Mercurial is a Python application using C and Rust extensions. It is extendable with
Mercurial extensions and two Python packages provide very useful Mercurial extensions
that most users should use : hg-git (Mercurial extension hggit) and hg-evolve (Mercurial
extensions topic and evolve).

These things are packaged in 3 PyPI packages (associated with their equivalent
conda-forge packages): mercurial, hg-git, hg-evolve.

To use Mercurial extensions, one has to write few lines in a configuration file
(~/.hgrc).

Mercurial with hg-git and hg-evolve is great but it is a bit difficult to setup. hg-setup
is there to help people to start with Mercurial and finalize its installation.

## Install

Currently, only installation from source works.

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
# with Miniforge (conda-forge) and conda-app (https://foss.heptapod.net/fluiddyn/conda-app)
conda-app install mercurial
# this requires optional deps on conda-forge
pixy global install mercurial[full]
```

However, we are not yet there. Nevertheless, this will work very soon (once hg-setup is
on PyPI)

```sh
pipx install mercurial
pipx inject mercurial hg-git hg-evolve hg-setup
# or
uv tool install mercurial --with hg-git --with hg-evolve --with hg-setup
```

and this will work soon (once hg-setup is on conda-forge and mercurial-app has been
modified).

```sh
conda-app install mercurial
pixy global install mercurial-app
pixi global install mercurial --with hg-git --with hg-evolve --with hg-setup
```

## User interfaces

Warning: in early development. This is still completely unstable!

The ~/.hgrc file can be initialize with a simple Terminal User Interface (TUI):

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
