import schemathesis
import pytest
from hypothesis import settings
from schemathesis import DataGenerationMethod

schema = schemathesis.from_uri(
    "http://127.0.0.1:8000/openapi.json",
    data_generation_methods=[DataGenerationMethod.positive, DataGenerationMethod.negative],
)


@pytest.mark.xfail(reason="experimental")
@schema.parametrize()
@settings(max_examples=1000)
def test_api(case):
    case.call_and_validate()
