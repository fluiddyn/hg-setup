from textual.app import App, ComposeResult
from textual import on
from textual.containers import Horizontal, VerticalScroll
from textual.widgets import (
    Static,
    Label,
    Input,
    Header,
    Footer,
    Checkbox,
    Button,
    Pretty,
    Markdown,
)


from textual.binding import Binding

from .hgrcs import create_hgrc_text

inputs = {
    "name": dict(placeholder="Firstname Lastname"),
    "email": dict(placeholder="Email"),
    "editor": dict(placeholder="nano", value="nano"),
}


class InitHgrcApp(App):
    _hgrc_text: str

    BINDINGS = [
        Binding(key="q", action="quit", description="Quit the app"),
        Binding(
            key="question_mark",
            action="help",
            description="Show help screen",
            key_display="?",
        ),
    ]

    def __init__(self):
        super().__init__()

    def _create_markdown_code(self):
        args = [inp.value for inp in self._inputs.values()]
        args.append(self._checkbox_tweak.value)
        self._hgrc_text = create_hgrc_text(*args)
        return f"```{self._hgrc_text}```"

    def compose(self) -> ComposeResult:
        self._inputs = {key: Input(**kwargs) for key, kwargs in inputs.items()}
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
                self._checkbox_tweak = Checkbox("tweakdefaults", value=True)
                yield self._checkbox_tweak

            with VerticalScroll():
                yield Button("Regenerate .hgrc code")
                self._markdown = Markdown(self._create_markdown_code())
                yield self._markdown
                yield Button.success("Save ~/.hgrc")

        yield Footer()

    def on_mount(self) -> None:
        self.title = "Initialize Mercurial user configuration"
        self.sub_title = "written in ~/.hgrc"

    @on(Button.Pressed)
    def act(self, event: Button.Pressed) -> None:
        self._markdown.update(self._create_markdown_code())


def init_tui():
    app = InitHgrcApp()
    app.run()
