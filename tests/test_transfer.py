import io

import pytest

from file_operators import get_file
from transfer import PDFToJPEG


def test_pdf_to_jpeg():
    file = get_file("tests/test_sample/2003.00744v1_image_pdf.pdf")
    count = 0
    for image_file in PDFToJPEG().iterate_transform(file):
        count += 1
        assert type(image_file) == io.BytesIO
    assert count == 3


