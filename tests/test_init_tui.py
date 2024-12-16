import os

from hg_setup.init_cmd import InitHgrcApp
from hg_setup.hgrcs import name_default

from time import sleep


async def test_init_tui(tmp_path, monkeypatch):
    """Test pressing keys has the desired result."""

    tmp_dir = tmp_path / "home_test"
    tmp_dir.mkdir()

    name_home_envvar = "HOME" if os.name != "nt" else "UserProfile"
    monkeypatch.setenv(name_home_envvar, str(tmp_dir))

    name = "Toto Lastname"
    email = "toto.lastname@proton.me"
    app = InitHgrcApp(name, email)
    async with app.run_test() as pilot:
        await pilot.click(app.vert_hgrc_params.inputs["name"])
        await pilot.press("hello")
        await pilot.click(app.vert_hgrc_params)
        await pilot.click("#button_save")
        while not (tmp_dir / name_default).exists():
            sleep(0.05)
        assert len(list(tmp_dir.glob(name_default + "*"))) == 1
        await pilot.press("s")
        await pilot.click("#no")
        await pilot.click(app.vert_hgrc_params.checkboxs["tweakdefaults"])
        await pilot.click("#button_save")
        await pilot.click("#yes")
        while not len(list(tmp_dir.glob(name_default + "*"))) == 2:
            sleep(0.05)
        await pilot.press("q")
