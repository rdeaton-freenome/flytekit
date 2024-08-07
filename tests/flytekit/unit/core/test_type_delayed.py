from __future__ import annotations

import dataclasses
import typing
from dataclasses import dataclass

from dataclasses_json import DataClassJsonMixin
from typing_extensions import Annotated  # type: ignore

from flytekit.core import context_manager
from flytekit.core.interface import transform_function_to_interface, transform_inputs_to_parameters
from flytekit.core.type_engine import TypeEngine


@dataclass
class Foo(DataClassJsonMixin):
    x: int
    y: str
    z: typing.Dict[str, str]


def test_jsondc_schemaize():
    lt = TypeEngine.to_literal_type(Foo)
    pt = TypeEngine.guess_python_type(lt)
    assert dataclasses.is_dataclass(pt)

def test_structured_dataset():
    ctx = context_manager.FlyteContext.current_context()

    def z(a: Annotated[int, "some annotation"]) -> Annotated[int, "some annotation"]:
        return a

    our_interface = transform_function_to_interface(z)
    params = transform_inputs_to_parameters(ctx, our_interface)
    assert params.parameters["a"].required
    assert params.parameters["a"].default is None
    assert our_interface.inputs == {"a": Annotated[int, "some annotation"]}
    assert our_interface.outputs == {"o0": Annotated[int, "some annotation"]}
