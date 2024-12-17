# How to contribute to hg-setup

The repository is currently hosted here https://foss.heptapod.net/fluiddyn/hg-setup.

We use a topic/MR based workflow as explained
[here](https://fluidhowto.readthedocs.io/en/latest/mercurial/heptapod-workflow.html).

For local development, you need `make` and [PDM](https://pdm-project.org). To install the
package, deactivate all unrelated virtual environments and run `make`.

- The tests use pytest and can be run with `make test`.

- `make format` can be used to format the code.

- `make lock` resolve the dev environment.

You will see that hg-setup is based on [Click] (for the command line interface) and
[Textual] (for the terminal user interfaces).

Note also that we require Python >=3.11, to ease the development and because hg-setup is
going to be installed with tools (UV, Pixi) for which is not difficult to get a recent
Python.

[click]: https://click.palletsprojects.com
[textual]: https://textual.textualize.io/
