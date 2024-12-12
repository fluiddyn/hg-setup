"""hgrc interactions"""

import os
import subprocess

from textwrap import dedent
from shutil import which


def create_hgrc_text(name, email, editor, tweakdefaults):
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

    # get pythonexe to be able to check installation of
    pythonexe = subprocess.run(
        ["hg", "debuginstall", "-T", "{pythonexe}"],
        capture_output=True,
        check=True,
        text=True,
    ).stdout

    def check_ext_installed(ext):
        process = subprocess.run([pythonexe, "-c", f"import {ext}"], check=False)
        return process.returncode == 0

    enable_hggit = check_ext_installed("hggit")

    add_ext_line(
        "hggit", enable_hggit, comment="only to use Mercurial with GitHub and Gitlab"
    )

    add_line()
    for ext in ["churn", "shelve"]:
        add_ext_line(ext)

    add_line()
    enable_topic = check_ext_installed("hgext3rd.topic")

    add_ext_line("topic", enable_topic, comment="lightweight feature branches")

    ext_lines.append("# history edition")
    for ext in ["evolve", "rebase", "absorb", "uncommit"]:
        add_ext_line(ext, enable_topic)

    add_line()
    add_ext_line("histedit", False, "advanced history edition")

    diff_tools = ["meld", "kdiff3", "difft"]
    diff_tools_avail = [
        diff_tool for diff_tool in diff_tools if which(diff_tool) is not None
    ]
    if diff_tools_avail:
        diff_tool = diff_tools_avail[0]
    else:
        diff_tool = False

    add_line()
    add_ext_line("hgext.extdiff", diff_tool, "external diff tools")

    add_line("\n[extdiff]")
    add_ext_line(f"cmd.{diff_tool}", diff_tool)

    hgrc_text += "\n".join(ext_lines) + "\n"

    return hgrc_text
