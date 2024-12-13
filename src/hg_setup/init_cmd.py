"""hg-setup init"""

from pathlib import Path

from textual.app import App, ComposeResult
from textual import on
from textual.containers import Horizontal, VerticalScroll
from textual.widgets import (
    Label,
    Input,
    Header,
    Footer,
    Checkbox,
    Button,
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


class InitHgrcApp(App):
    _hgrc_text: str
    _inputs: dict
    _checkboxs: dict
    _markdown: Markdown
    _label_feedback: Label

    BINDINGS = [
        Binding(key="q", action="quit", description="Quit the app"),
        Binding(
            key="question_mark",
            action="help",
            description="Show help screen",
            key_display="?",
        ),
    ]

    def __init__(self, name, email):
        if name is not None:
            inputs["name"]["value"] = name
        if email is not None:
            inputs["email"]["value"] = email
        self.hgrc_maker = HgrcCodeMaker()
        super().__init__()

    def _create_markdown_code(self):
        kwargs = {key: inp.value for key, inp in self._inputs.items()}
        kwargs.update(
            {key: checkbox.value for key, checkbox in self._checkboxs.items()}
        )
        self._hgrc_text = self.hgrc_maker.make_text(**kwargs)
        return f"```{self._hgrc_text}```"

    def compose(self) -> ComposeResult:
        self._inputs = {key: Input(**kwargs) for key, kwargs in inputs.items()}
        self._checkboxs = {
            key.replace(" ", "_"): Checkbox(key, value=value)
            for key, value in checkboxs.items()
        }
        yield Header()

        with Horizontal():
            with VerticalScroll():
                yield Label("Enter your name and email")
                for key in ["name", "email"]:
                    yield self._inputs[key]
                yield Label("Enter your preferred editor")
                yield self._inputs["editor"]
                yield Label(
                    "To get slight improvements to the UI over time (recommended)"
                )
                for checkbox in self._checkboxs.values():
                    yield checkbox

            with VerticalScroll():
                self._markdown = Markdown(self._create_markdown_code())
                yield self._markdown
                yield Button.success("Save ~/.hgrc")
                self._label_feedback = Label()
                yield self._label_feedback

        yield Footer()

    def on_mount(self) -> None:
        self.title = "Initialize Mercurial user configuration"
        self.sub_title = "written in ~/.hgrc"

    @on(Button.Pressed)
    def act(self, event: Button.Pressed) -> None:
        path_hgrc = Path.home() / ".hgrc"
        if path_hgrc.exists():
            self._label_feedback.update(f"{path_hgrc} already exists. Nothing to do.")
            return
        self._create_markdown_code()
        path_hgrc.write_text(self._hgrc_text)
        self._label_feedback.value = f"configuration written in {path_hgrc}."

    @on(Input.Changed)
    def on_input_changed(self, event: Input.Changed) -> None:
        self.on_user_inputs_changed()

    @on(Checkbox.Changed)
    def on_checkbox_changed(self, event: Input.Changed) -> None:
        self.on_user_inputs_changed()

    def on_user_inputs_changed(self):
        self._markdown.update(self._create_markdown_code())


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
