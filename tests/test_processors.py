import io

import pytest

from file_operators import get_file
from processors import PreProcessor, OCRTesseractProcessor, PostProcessor, PDFToJPEG


def test_pdf_to_jpeg():
    file = get_file("tests/test_sample/2003.00744v1_image_pdf.pdf")
    count = 0
    for image_file in PDFToJPEG().iterate_transform(file):
        count += 1
        assert type(image_file) == io.BytesIO
    assert count == 3


def test_pre_processor():
    file = get_file("tests/test_sample/82251504.png")
    new_file = PreProcessor(100).transform(file)
    assert type(new_file) == io.BytesIO


def test_ocr_tesseract_processor():
    file = get_file("tests/test_sample/82251504.png")
    text = OCRTesseractProcessor().transform(file)
    assert type(text) == str


def test_post_processor():
    text1 = "asb√sss"
    text2 = "asb-sss"
    new_text1 = PostProcessor().transform(text1)
    new_text2 = PostProcessor().transform(text2)
    assert new_text1 == "asbsss"
    assert new_text2 == "asb-sss"
