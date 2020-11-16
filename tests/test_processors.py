import io

import pytest

from ocr_processor.file_operators import get_file
from ocr_processor.processors import PreProcessor, OCRTesseractProcessor, PostProcessor, PDFToJPEG


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
    text = "asb√sss"
    new_text = PostProcessor().transform(text)
    assert new_text == "asbsss"
