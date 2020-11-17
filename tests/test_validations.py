import pytest
from click import BadParameter

from validations import validation_input_path, validation_output_path


@pytest.mark.parametrize(
    "input,expected",
    [
        (("tests/test_sample/2003.00744v1_image_pdf.pdf", []), BadParameter),
        (("tests/test_sample/no_exist.png", ["png"]), BadParameter),
        (("tests/test_sample/not_file", ["png", "pdf"]), BadParameter),
    ]
)
def test_validation_input_ng(input, expected):
    input_path, support_input = input
    with pytest.raises(expected):
        validation_input_path(input_path, support_input)


def test_validation_input_ok():
    input_path = "tests/test_sample/2003.00744v1_image_pdf.pdf"
    support = ["pdf"]
    assert validation_input_path(input_path, support) is None


@pytest.mark.parametrize(
    "input,expected",
    [
        (("tests/test_sample/test.txt", ["txt"]), BadParameter),
        (("tests/test_sample/ok.txt", []), BadParameter),
        (("tests/test_sample/not_file", ["txt"]), BadParameter),
    ]
)
def test_validation_output_ng(input, expected):
    input_path, support_input = input
    with pytest.raises(expected):
        validation_output_path(input_path, support_input)


def test_validation_output_ok():
    input_path = "tests/test_sample/ok.txt"
    support = ["txt"]
    assert validation_output_path(input_path, support) is None
