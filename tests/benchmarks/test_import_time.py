import importlib
from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    from pytest_codspeed import BenchmarkFixture

import aitells


@pytest.mark.benchmark
def test_import_time(benchmark: "BenchmarkFixture") -> None:
    def reload_aitells() -> None:
        _ = importlib.reload(aitells)

    benchmark(reload_aitells)
