"""Helper to create field files

"""

import re
from abc import ABC, abstractmethod
from io import StringIO
from numbers import Number
from pathlib import Path

import numpy as np

from fluidsimfoam.foam_input_files import parse
from fluidsimfoam.foam_input_files.ast import (
    Code,
    CodeStream,
    Dict,
    DimensionSet,
    FoamInputFile,
    List,
    Value,
    str2foam_units,
)

DEFAULT_CODE_INCLUDE = '#include "fvCFD.H"'
DEFAULT_CODE_OPTIONS = (
    "-I$(LIB_SRC)/finiteVolume/lnInclude \\\n-I$(LIB_SRC)/meshTools/lnInclude"
)
DEFAULT_CODE_LIBS = "-lmeshTools \\\n-lfiniteVolume"


class FieldABC(ABC):
    cls: str

    @classmethod
    def from_code(cls, code: str):
        if "nonuniform" not in code:
            tree = parse(code)
            return cls(None, None, tree=tree)

        index_nonuniform = code.index("nonuniform")
        index_boundaryField = code.rindex("boundaryField", index_nonuniform)
        index_opening_par = code.index("(", index_nonuniform, index_boundaryField)
        index_closing_par = code.rindex(
            ")", index_nonuniform, index_boundaryField
        )

        code_to_parse = (
            code[:index_nonuniform] + ";\n\n" + code[index_boundaryField:]
        )

        tree = parse(code_to_parse)
        code_data = code[index_opening_par + 1 : index_closing_par].strip()

        if code_data.startswith("("):
            code_data = re.sub("[()]", "", code_data)

        data = np.loadtxt(StringIO(code_data))

        tree.data = data
        return cls("", "", tree=tree, values=data)

    @classmethod
    def from_path(cls, path: str or Path):
        return cls.from_code(Path(path).read_text())

    def __init__(self, name, dimension, tree=None, values=None):
        if tree is not None:
            self.tree = tree
        else:
            info = {
                "version": "2.0",
                "format": "ascii",
                "class": self.cls,
                "object": name,
            }

            if not isinstance(dimension, DimensionSet):
                dimension = DimensionSet(str2foam_units(dimension))

            self.tree = FoamInputFile(
                info, children={"dimensions": dimension, "internalField": None}
            )

            self.tree.set_child("boundaryField", {})

        if values is not None:
            self.set_values(values)

    def dump(self):
        return self.tree.dump()

    @abstractmethod
    def set_values(self, values):
        """Set internalField with value(s)"""

    def set_codestream(
        self,
        code,
        include=DEFAULT_CODE_INCLUDE,
        options=DEFAULT_CODE_OPTIONS,
        libs=DEFAULT_CODE_LIBS,
    ):
        data = {
            "codeInclude": include,
            "codeOptions": options,
            "codeLibs": libs,
            "code": code,
        }
        data = {key: Code(key, value.strip()) for key, value in data.items()}
        self.tree.children["internalField"] = CodeStream(
            data, name="internalField", directive="#codeStream"
        )

    def set_boundary(self, name, type_, value=None, gradient=None):
        boundaries = self.tree.children["boundaryField"]
        data = {"type": type_}
        if value is not None:
            data["value"] = value
        if gradient is not None:
            data["gradient"] = gradient
        boundaries[name] = Dict(data, name=name)

    def set_name(self, name):
        self.tree.info["object"] = name

    def get_array(self):
        return np.array(self.tree.children["internalField"])


class VolScalarField(FieldABC):
    cls = "volScalarField"

    def set_values(self, values):
        if isinstance(values, Number):
            value = Value(values, name="uniform")
        else:
            value = List(
                list(values),
                name=f"internalField nonuniform\nList<scalar>\n{len(values)}",
            )
        self.tree.children["internalField"] = value


class VolVectorField(FieldABC):
    cls = "volVectorField"

    def set_values(self, values, vy=None, vz=None):
        if vy is not None:
            if vz is None:
                raise ValueError
            if not isinstance(values, np.ndarray):
                raise ValueError
            if values.ndim != 1 or values.size != vy.size != vz.size:
                raise ValueError
            vx = values
            values = np.stack([vx, vy, vz]).T

        if isinstance(values, np.ndarray):
            if values.ndim != 2:
                raise ValueError
            values = [list(arr) for arr in values]

        n_elem = len(values)
        if n_elem == 3 and isinstance(values[0], Number):
            value = Value(
                "(" + " ".join(str(value) for value in values) + ")",
                name="uniform",
            )
        else:
            value = List(
                [List(value) for value in values],
                name=f"internalField nonuniform\nList<vector>\n{n_elem}",
            )
        self.tree.children["internalField"] = value
