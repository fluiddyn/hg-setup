import shutil
from pathlib import Path

import pytest
from fluidsimfoam_cbox import Simul

from fluidsimfoam.testing import check_saved_case

here = Path(__file__).absolute().parent


@pytest.mark.parametrize("index_sim", [0, 1, 2])
def test_init_simul_sim0(index_sim):
    params = Simul.create_default_params()

    params.output.sub_directory = "tests_fluidsimfoam/cbox/sim0"

    if index_sim == 1:
        params.transport_properties.nu = 0.002
    elif index_sim == 2:
        params.transport_properties.nu = 0.003

    sim = Simul(params)

    path_saved_case = here / f"saved_cases/cbox/sim{index_sim}"
    check_saved_case(
        path_saved_case, sim.path_run, files_compare_tree=["blockMeshDict"]
    )


path_foam_executable = shutil.which("buoyantBoussinesqPimpleFoam")


@pytest.mark.skipif(
    path_foam_executable is None, reason="executable icoFoam not available"
)
def test_run():
    params = Simul.create_default_params()

    params.output.sub_directory = "tests_fluidsimfoam/cbox/"

    params.control_dict.end_time = 10

    sim = Simul(params)

    sim.make.exec("run")
