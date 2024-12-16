"""hgrc interactions"""

import os
import subprocess

from pathlib import Path

from textwrap import dedent
from shutil import which


name_default = ".hgrc" if os.name != "nt" else "mercurial.ini"


def check_hg_conf_file():
    """Check if a config file exists"""

    path_default = Path.home() / name_default
    exists = path_default.exists()

    if os.name != "nt" or exists:
        return exists, path_default

    # on windows, we also need to check for .hgrc
    path_hgrc = Path.home() / ".hgrc"
    if path_hgrc.exists():
        return True, path_hgrc
    else:
        return False, path_default


class HgrcCodeMaker:
    def __init__(self):
        # get pythonexe to be able to check installation of
        process = subprocess.run(
            ["hg", "debuginstall", "-T", "{pythonexe}"],
            capture_output=True,
            # cannot use check=True
            check=False,
            text=True,
        )
        pythonexe = process.stdout
        if not Path(pythonexe).exists():
            raise ValueError(str(process))

        if pythonexe.endswith("hg.exe"):
            # this can happen on Windows!
            self.enable_hggit = self.enable_topic = True
        else:

            def check_ext_installed(ext):
                process = subprocess.run(
                    [pythonexe, "-c", f"import {ext}"], check=False
                )
                return process.returncode == 0

            self.enable_hggit = check_ext_installed("hggit")
            self.enable_topic = check_ext_installed("hgext3rd.topic")

        diff_tools = ["meld", "kdiff3", "difft"]
        diff_tools_avail = [
            diff_tool for diff_tool in diff_tools if which(diff_tool) is not None
        ]
        if diff_tools_avail:
            self.diff_tool = diff_tools_avail[0]
        else:
            self.diff_tool = False

    def make_text(
        self,
        name,
        email,
        editor,
        tweakdefaults=True,
        simple_history_edition=True,
        advanced_history_edition=False,
    ):
        if not name:
            name = "???"

        if not email:
            email = "???"

        tweakdefaults = "True" if tweakdefaults else "False"

        paginate = "# paginate = never"
        if os.name == "nt":
            paginate = "# avoid a bug on Windows if no pager is avail\npaginate = never"

        hgrc_text = dedent(
            f"""
            # File created by hg-setup init
            # (see 'hg help config' for more info)
            # One can delete the character '#' to activate some lines

            [ui]
            # name and email, e.g.
            # username = Jane Doe <jdoe@example.com>
            username = {name} <{email}>

            # light weight editor for edition of commit messages
            # popular choices are vim, nano, emacs -nw -Q, etc.
            editor = {editor}

            # We recommend enabling tweakdefaults to get slight improvements to
            # the UI over time. Make sure to set HGPLAIN in the environment when
            # writing scripts!
            tweakdefaults = {tweakdefaults}

            # uncomment to disable color in command output
            # (see 'hg help color' for details)
            # color = never

            # uncomment to disable command output pagination
            # (see 'hg help pager' for details)
            {paginate}

            [alias]
            lg = log -G
            up = up -v

            [extensions]
            # uncomment the lines below to enable some popular extensions
            # (see 'hg help extensions' for more info)

        """
        )

        ext_lines = []

        def add_ext_line(module, enable=True, comment=None):
            if comment is not None:
                ext_lines.append("# " + comment)
            begin = "" if enable else "# "
            ext_lines.append(f"{begin}{module} =")

        def add_line(line=""):
            ext_lines.append(line)

        add_ext_line(
            "hggit",
            self.enable_hggit,
            comment="to use Mercurial with GitHub and Gitlab",
        )

        add_line()
        for ext in ["churn", "shelve"]:
            add_ext_line(ext)

        add_line()

        add_ext_line("topic", self.enable_topic, comment="lightweight feature branches")

        if not self.enable_topic:
            enable_hist_edition = False
        else:
            enable_hist_edition = simple_history_edition

        ext_lines.append("# history edition")
        for ext in ["evolve", "rebase", "absorb"]:
            add_ext_line(ext, enable_hist_edition)

        add_line()
        add_ext_line("histedit", advanced_history_edition, "advanced history edition")

        add_line()
        add_ext_line("hgext.extdiff", self.diff_tool, "external diff tools")

        add_line("\n[extdiff]")
        add_ext_line(f"cmd.{self.diff_tool}", self.diff_tool)

        hgrc_text += "\n".join(ext_lines) + "\n"

        return hgrc_text
