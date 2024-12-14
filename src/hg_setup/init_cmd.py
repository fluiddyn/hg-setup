"""hg-setup init"""

from pathlib import Path

from textual.app import App, ComposeResult
from textual import on
from textual.containers import Horizontal, VerticalScroll
from textual.widgets import (
    Label,
    Log,
    Input,
    Header,
    Footer,
    Checkbox,
    SelectionList,
    Markdown,
)

import rich_click as click

from textual.binding import Binding

from .hgrcs import HgrcCodeMaker

inputs = {
    "name": dict(placeholder="Firstname Lastname"),
    "email": dict(placeholder="Email"),
    "editor": dict(placeholder="nano", value="nano"),
}

checkboxs = {
    "tweakdefaults": True,
    "basic history edition": True,
    "advanced history edition": False,
}


class Frame(VerticalScroll):
    pass


class VerticalHgrcParams(Frame):
    inputs: dict
    checkboxs: dict

    def compose(self) -> ComposeResult:
        self.inputs = {key: Input(**kwargs) for key, kwargs in inputs.items()}
        self.checkboxs = {
            key.replace(" ", "_"): Checkbox(key, value=value)
            for key, value in checkboxs.items()
        }

        yield Label("Enter your name and email")
        for key in ["name", "email"]:
            yield self.inputs[key]
        yield Label("Enter your preferred editor")
        yield self.inputs["editor"]
        yield Label("To get slight improvements to the UI over time (recommended)")

        yield self.checkboxs["tweakdefaults"]

        yield Label("Do you plan to use history edition?")
        for key in tuple(self.checkboxs.keys())[1:]:
            yield self.checkboxs[key]


class VerticalCompletionParams(Frame):
    def compose(self) -> ComposeResult:
        yield Label("For which shells do you want to initialize autocompletion?")

        shells_ = [("bash", 1, True), ("zsh", 2, True), ("tcsh", 3, False)]
        self.selected_shells = SelectionList(*shells_)
        yield self.selected_shells


class InitHgrcApp(App):
    _hgrc_text: str
    log_hgrc: Markdown
    _label_feedback: Label

    CSS_PATH = "init_app.tcss"

    BINDINGS = [
        Binding(key="q", action="quit", description="Quit the app"),
        Binding(
            key="s",
            action="save_hgrc",
            description="Save ~/.hgrc",
        ),
        Binding(
            key="a",
            action="init_completion",
            description="Init autocompletion",
        ),
    ]

    def __init__(self, name, email):
        if name is not None:
            inputs["name"]["value"] = name
        if email is not None:
            inputs["email"]["value"] = email
        self.hgrc_maker = HgrcCodeMaker()
        super().__init__()

    def _create_hgrc_code(self):
        kwargs = {key: inp.value for key, inp in self.vert_hgrc_params.inputs.items()}
        kwargs.update(
            {
                key: checkbox.value
                for key, checkbox in self.vert_hgrc_params.checkboxs.items()
            }
        )
        self._hgrc_text = self.hgrc_maker.make_text(**kwargs)
        return self._hgrc_text

    def compose(self) -> ComposeResult:
        yield Header()

        with Horizontal():
            with VerticalScroll():
                self.vert_hgrc_params = VerticalHgrcParams()
                yield self.vert_hgrc_params

                self.vert_compl_params = VerticalCompletionParams()
                yield self.vert_compl_params

            with VerticalScroll():
                self.log_hgrc = Log("", auto_scroll=False)
                yield self.log_hgrc
                self.log_feedback = Log()
                yield self.log_feedback

        yield Footer()

    def on_mount(self) -> None:
        self.title = "Initialize Mercurial user configuration"

        widget = self.log_hgrc
        widget.styles.height = "4fr"
        widget.border_title = "Read the resulting ~/.hgrc (press on the 's' key to save)"

        widget = self.log_feedback
        widget.styles.height = "1fr"
        widget.border_title = "log"

        widget = self.vert_hgrc_params
        widget.styles.height = "2fr"
        widget.border_title = "Enter few parameters"

        widget = self.vert_compl_params
        widget.styles.height = "1fr"
        widget.border_title = "Autocompletion (press on the 'a' key to initialize)"

    def action_save_hgrc(self) -> None:
        path_hgrc = Path.home() / ".hgrc"
        if path_hgrc.exists():
            self.log_feedback.write_line(f"{path_hgrc} already exists. Nothing to do.")
            return
        self._create_hgrc_code()
        path_hgrc.write_text(self._hgrc_text)
        self.log_feedback.write_line(f"configuration written in {path_hgrc}.")

    def action_init_completion(self) -> None:
        self.log_feedback.write_line("not implemented.")

    @on(Input.Changed)
    def on_input_changed(self, event: Input.Changed) -> None:
        self.on_user_inputs_changed()

    @on(Checkbox.Changed)
    def on_checkbox_changed(self, event: Input.Changed) -> None:
        self.on_user_inputs_changed()

    def on_user_inputs_changed(self):
        self.log_hgrc.clear()
        self.log_hgrc.write(self._create_hgrc_code())


def init_tui(name, email):
    """main TUI function for command init"""
    app = InitHgrcApp(name, email)
    app.run()


def init_auto(name, email):
    """init without user interaction"""

    # TODO: good default editor depending on what is available
    editor = "nano"

    path_hgrc = Path.home() / ".hgrc"

    if path_hgrc.exists():
        click.echo(f"{path_hgrc} already exists. Nothing to do.")
        return

    text = HgrcCodeMaker().make_text(name, email, editor)
    path_hgrc.write_text(text)

    click.echo(f"configuration written in {path_hgrc}.")
